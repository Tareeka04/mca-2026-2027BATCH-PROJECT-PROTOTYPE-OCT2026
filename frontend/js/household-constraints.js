/* Global household constraint bridge.
 * The saved Household Solver profile is reused across every recipe discovery surface.
 * Strict food constraints are treated as hard filters; preferences remain visible as context.
 */
const HouseholdConstraints = {
  normalize(value) {
    return String(value || '')
      .toLowerCase()
      .replace(/[()]/g, ' ')
      .replace(/[^a-z0-9]+/g, ' ')
      .trim();
  },

  restrictionRules(member) {
    const raw = [];
    (member.avoid_ingredients || []).forEach(x => raw.push(String(x)));
    if (member.custom_preference) raw.push(...String(member.custom_preference).split(/[,;]+/));
    const avoid = [];
    const requirePresent = [];
    raw.forEach(item => {
      const text = String(item || '').trim();
      if (!text) return;
      const n = this.normalize(text);
      const noMatch = n.match(/^no\s+(.+)$/);
      if (noMatch) { avoid.push(noMatch[1].trim()); return; }
      const withoutMatch = n.match(/^(?:without|free\s+from)\s+(.+)$/);
      if (withoutMatch) { avoid.push(withoutMatch[1].trim()); return; }
      // A positive requirement such as “high salt” means the recipe should contain salt.
      if (/^(high|extra|more)\s+salt$/.test(n)) { requirePresent.push('salt'); return; }
      avoid.push(n);
    });
    return { avoid: [...new Set(avoid)], requirePresent: [...new Set(requirePresent)] };
  },

  containsIngredient(terms, ingredient) {
    const a = this.normalize(ingredient);
    if (!a) return false;
    const padded = ` ${terms} `;
    return padded.includes(` ${a} `) || (a.endsWith('s') && padded.includes(` ${a.slice(0,-1)} `)) || padded.includes(` ${a}s `);
  },

  recipeTerms(recipe) {
    const terms = [];
    (recipe.normalized_ingredients || []).forEach(x => terms.push(this.normalize(x)));
    (recipe.ingredients || []).forEach(x => terms.push(this.normalize(x.name)));
    return terms.join(' ');
  },

  getMembers() {
    try {
      const saved = JSON.parse(localStorage.getItem('mealsolver_household') || 'null');
      return Array.isArray(saved?.members) ? saved.members : [];
    } catch (e) {
      return [];
    }
  },

  isHardCompatible(recipe, members = this.getMembers()) {
    if (!members.length) return true;
    const terms = this.recipeTerms(recipe);
    const flavor = recipe.flavor_profile || {};
    const spice = Number(flavor.spicy ?? 0);

    for (const member of members) {
      const diet = this.normalize(member.diet);
      if (diet === 'vegetarian' && !['vegetarian', 'vegan'].includes(this.normalize(recipe.diet))) return false;
      if (diet === 'vegan' && !recipe.is_vegan) return false;
      if (diet === 'jain' && !recipe.is_jain) return false;
      if (diet === 'gluten free' && !recipe.is_gluten_free) return false;

      const tolerance = this.normalize(member.spice_tolerance);
      const maxSpice = { mild: 1, low: 2, medium: 3, spicy: 5 }[tolerance];
      if (maxSpice !== undefined && spice > maxSpice) return false;

      const rules = this.restrictionRules(member);
      for (const avoided of rules.avoid) {
        const a = this.normalize(avoided);
        if (!a) continue;
        if ((a === 'dairy' && /(^| )(milk|curd|yogurt|paneer|ghee|butter|cream|cheese)( |$)/.test(terms)) || this.containsIngredient(terms, a)) return false;
      }
      for (const required of rules.requirePresent) {
        if (!this.containsIngredient(terms, required)) return false;
      }

      const texture = this.normalize(member.texture_preference);
      if (texture && texture !== 'any' && recipe.texture) {
        const rt = this.normalize(recipe.texture);
        if (texture.includes('soft') && !['soft', 'very soft'].includes(rt)) return false;
      }
    }
    return true;
  },

  filterRecipes(recipes) {
    return (recipes || []).filter(r => this.isHardCompatible(r));
  },

  memberChecks(recipe, members = this.getMembers()) {
    const terms = this.recipeTerms(recipe);
    const flavor = recipe.flavor_profile || {};
    const spice = Number(flavor.spicy ?? 0);
    const checks = [];
    for (const member of members) {
      const checksForMember = [];
      const diet = this.normalize(member.diet);
      let dietOk = true;
      if (diet === 'vegetarian') dietOk = ['vegetarian', 'vegan'].includes(this.normalize(recipe.diet));
      else if (diet === 'vegan') dietOk = !!recipe.is_vegan;
      else if (diet === 'jain') dietOk = !!recipe.is_jain;
      else if (diet === 'gluten free') dietOk = !!recipe.is_gluten_free;
      checksForMember.push({label: 'Diet', ok: dietOk});

      const tolerance = this.normalize(member.spice_tolerance);
      const maxSpice = { mild: 1, low: 2, medium: 3, spicy: 5 }[tolerance];
      checksForMember.push({label: 'Spice', ok: maxSpice === undefined || spice <= maxSpice});

      const rules = this.restrictionRules(member);
      const avoidHits = rules.avoid.filter(a => (a === 'dairy' && /(^| )(milk|curd|yogurt|paneer|ghee|butter|cream|cheese)( |$)/.test(terms)) || this.containsIngredient(terms, a));
      const requiredMissing = rules.requirePresent.filter(a => !this.containsIngredient(terms, a));
      const avoidOk = avoidHits.length === 0 && requiredMissing.length === 0;
      const detailParts = [];
      rules.avoid.forEach(a => detailParts.push(`${avoidHits.includes(a) ? '✗' : '✓'} ${a} ${avoidHits.includes(a) ? 'is present' : 'not used'}`));
      rules.requirePresent.forEach(a => detailParts.push(`${requiredMissing.includes(a) ? '✗' : '✓'} ${a} requirement ${requiredMissing.includes(a) ? 'not met' : 'met'}`));
      checksForMember.push({label: 'Avoided / required ingredients', ok: avoidOk, detail: detailParts.length ? detailParts.join(' • ') : 'No ingredient restrictions'});

      const texture = this.normalize(member.texture_preference);
      const textureOk = !texture || texture === 'any' || !recipe.texture || !(texture.includes('soft') && !['soft', 'very soft'].includes(this.normalize(recipe.texture)));
      checksForMember.push({label: 'Texture', ok: textureOk});

      const prefs = (member.preferences || []).map(x => this.normalize(x));
      if (prefs.includes('healthy') || prefs.includes('wholesome') || prefs.includes('balanced')) {
        checksForMember.push({label: 'Lighter / balanced', ok: !!recipe.is_light, detail: recipe.is_light ? 'Recipe is marked as lighter / balanced' : 'Use the household adaptation shown by the solver'});
      }

      checks.push({name: member.name || 'Member', role: member.role || '', checks: checksForMember, ok: checksForMember.filter(x => ['Diet','Spice','Avoided / required ingredients','Texture'].includes(x.label)).every(x => x.ok)});
    }
    return checks;
  },

  explain(recipe) {
    const members = this.getMembers();
    if (!members.length) return { ok: true, reasons: [], conflicts: [], memberChecks: [] };
    const memberChecks = this.memberChecks(recipe, members);
    const reasons = [];
    const conflicts = [];
    const compatible = memberChecks.every(m => m.ok);
    if (compatible) reasons.push(`Checked all ${members.length} household member${members.length === 1 ? '' : 's'}`);
    else conflicts.push(`${memberChecks.filter(m => !m.ok).length} household member${memberChecks.filter(m => !m.ok).length === 1 ? '' : 's'} have at least one constraint conflict`);
    return { ok: compatible, reasons, conflicts, memberChecks };
  }
};
