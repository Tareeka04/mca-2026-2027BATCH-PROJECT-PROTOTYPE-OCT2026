/**
 * Household Meal Solver Frontend Module
 * "ONE HOUSEHOLD. DIFFERENT NEEDS. ONE MEAL."
 * Handles multi-member state, preset templates, constraint resolution,
 * member satisfaction visualization, and 1-pot family serving guidance.
 */

const HouseholdModule = {
  members: [
    {
      id: "m_1",
      name: "Mother (Sunita)",
      role: "Mother",
      diet: "Vegetarian",
      spice_tolerance: "Low",
      avoid_ingredients: ["peanuts"],
      preferences: ["quick"]
    },
    {
      id: "m_2",
      name: "Father (Rajesh)",
      role: "Father",
      diet: "Vegetarian",
      spice_tolerance: "Medium",
      avoid_ingredients: [],
      preferences: ["high_protein"]
    },
    {
      id: "m_3",
      name: "Aarav (6 yrs)",
      role: "Child",
      diet: "Vegetarian",
      spice_tolerance: "Mild",
      avoid_ingredients: ["capsicum"],
      preferences: ["kid_friendly"]
    },
    {
      id: "m_4",
      name: "Dadi (72 yrs)",
      role: "Grandmother",
      diet: "Vegetarian",
      spice_tolerance: "Low",
      avoid_ingredients: [],
      preferences: ["soft_food", "easy_digest"]
    }
  ],

  availableIngredients: new Set([
    "Rice", "Moong Dal", "Tomato", "Potato", "Turmeric", "Cumin Seeds", "Ghee", "Salt", "Coriander"
  ]),

  init() {
    this.restoreState();
    this.renderMembers();
    this.renderPantryPills();
    this.bindEvents();
    this.solve();
  },

  restoreState() {
    try {
      const saved = JSON.parse(localStorage.getItem('mealsolver_household') || 'null');
      if (saved && Array.isArray(saved.members) && saved.members.length) {
        this.members = saved.members;
        this.availableIngredients = new Set(saved.availableIngredients || []);
      }
    } catch (e) { /* ignore corrupt local state and use safe defaults */ }
  },

  persistState() {
    try {
      localStorage.setItem('mealsolver_household', JSON.stringify({members:this.members, availableIngredients:Array.from(this.availableIngredients)}));
    } catch (e) {}
  },

  bindEvents() {
    const addMemberBtn = document.getElementById('add-member-btn');
    const solveBtn = document.getElementById('household-solve-btn');
    const pantryInput = document.getElementById('household-pantry-input');
    const pantryAddBtn = document.getElementById('household-pantry-add-btn');

    if (addMemberBtn) {
      addMemberBtn.addEventListener('click', () => this.openMemberModal());
    }

    if (solveBtn) {
      solveBtn.addEventListener('click', () => this.solve());
    }

    if (pantryAddBtn && pantryInput) {
      const addPantry = () => {
        const val = pantryInput.value.trim();
        if (val) {
          this.addPantryItem(val);
          pantryInput.value = '';
        }
      };
      pantryAddBtn.addEventListener('click', addPantry);
      pantryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addPantry();
      });
    }

    // Modal Member Save / Cancel
    const memberModalBackdrop = document.getElementById('member-modal-backdrop');
    const memberModalClose = document.getElementById('member-modal-close');
    const memberForm = document.getElementById('member-form');

    if (memberModalClose && memberModalBackdrop) {
      memberModalClose.addEventListener('click', () => this.closeMemberModal());
      memberModalBackdrop.addEventListener('click', (e) => {
        if (e.target === memberModalBackdrop) this.closeMemberModal();
      });
    }

    if (memberForm) {
      memberForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.saveMemberFromForm();
      });
    }
  },

  getRoleAvatar(role) {
    const r = (role || "").toLowerCase();
    if (r.includes('mother') || r.includes('mom')) return '👩';
    if (r.includes('father') || r.includes('dad')) return '👨';
    if (r.includes('child') || r.includes('kid') || r.includes('baby') || r.includes('son') || r.includes('daughter')) return '👧';
    if (r.includes('grand') || r.includes('dadi') || r.includes('dada') || r.includes('nani') || r.includes('elder')) return '👵';
    if (r.includes('partner') || r.includes('wife') || r.includes('husband')) return '👫';
    return '👤';
  },

  renderMembers() {
    const container = document.getElementById('household-members-grid');
    const totalMembersDisplay = document.getElementById('total-members-display');
    const servingsInput = document.getElementById('household-servings-input');
    if (!container) return;

    if (totalMembersDisplay) {
      totalMembersDisplay.innerText = `${this.members.length} Family Members`;
    }

    if (servingsInput && (!servingsInput.value || servingsInput.value == this.members.length - 1 || servingsInput.value == this.members.length + 1)) {
      servingsInput.value = this.members.length;
    }

    let html = '';
    this.members.forEach((m, idx) => {
      const avatar = this.getRoleAvatar(m.role);
      const avoidStr = m.avoid_ingredients.length > 0 ? m.avoid_ingredients.join(', ') : 'None';
      const prefLabels = m.preferences.map(p => {
        if (p === 'soft_food') return '🥣 Soft Texture';
        if (p === 'high_protein') return '💪 High Protein';
        if (p === 'kid_friendly') return '🧸 Kid-Friendly';
        if (p === 'easy_digest') return '🌿 Light/Digestible';
        if (p === 'quick') return '⚡ Quick Meal';
        if (p === 'one_pot') return '🍲 One-Pot';
        return p;
      });

      html += `
        <div class="member-card">
          <div class="member-card-header">
            <div style="display: flex; align-items: center; gap: 10px;">
              <div class="member-avatar">${avatar}</div>
              <div>
                <h4 style="font-size: 16px; color: #fff; margin-bottom: 2px;">${m.name}</h4>
                <div style="font-size: 11px; color: var(--accent-gold); font-weight: 700; text-transform: uppercase;">${m.role}</div>
              </div>
            </div>
            <div style="display: flex; gap: 6px;">
              <button class="btn-member-action" title="Edit member" onclick="HouseholdModule.editMember('${m.id}')">✏️</button>
              <button class="btn-member-action" title="Remove member" onclick="HouseholdModule.removeMember('${m.id}')">&times;</button>
            </div>
          </div>

          <div class="member-traits-list">
            <div class="member-trait-item">
              <span class="trait-key">Diet:</span>
              <span class="trait-badge diet">${m.diet}</span>
            </div>
            <div class="member-trait-item">
              <span class="trait-key">Spice Tolerance:</span>
              <span class="trait-badge spice-${m.spice_tolerance.toLowerCase()}">🌶️ ${m.spice_tolerance}</span>
            </div>
            ${(m.avoid_ingredients.length > 0 || m.custom_preference) ? `
              <div class="member-trait-item">
                <span class="trait-key">Food constraints:</span>
                <span class="trait-badge avoid">🚫 ${[avoidStr !== 'None' ? avoidStr : '', m.custom_preference || ''].filter(Boolean).join(' • ')}</span>
              </div>
            ` : ''}
            ${prefLabels.length > 0 ? `
              <div style="margin-top: 6px; display: flex; flex-wrap: wrap; gap: 4px;">
                ${prefLabels.map(pl => `<span class="mini-tag" style="background: rgba(255,255,255,0.06); color: #A7F3D0; font-size: 10px;">${pl}</span>`).join('')}
              </div>
            ` : ''}
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  },

  loadPreset(presetId) {
    if (presetId === 'three_gen') {
      this.members = [
        { id: "m_1", name: "Mother (Sunita)", role: "Mother", diet: "Vegetarian", spice_tolerance: "Low", avoid_ingredients: ["peanuts"], preferences: ["quick"] },
        { id: "m_2", name: "Father (Rajesh)", role: "Father", diet: "Vegetarian", spice_tolerance: "Medium", avoid_ingredients: [], preferences: ["high_protein"] },
        { id: "m_3", name: "Aarav (6 yrs)", role: "Child", diet: "Vegetarian", spice_tolerance: "Mild", avoid_ingredients: ["capsicum"], preferences: ["kid_friendly"] },
        { id: "m_4", name: "Dadi (72 yrs)", role: "Grandmother", diet: "Vegetarian", spice_tolerance: "Low", avoid_ingredients: [], preferences: ["soft_food", "easy_digest"] }
      ];
      this.availableIngredients = new Set(["Rice", "Moong Dal", "Tomato", "Potato", "Turmeric", "Cumin Seeds", "Ghee", "Salt", "Coriander"]);
    } else if (presetId === 'jain_elder') {
      this.members = [
        { id: "m_1", name: "Dada Ji", role: "Grandfather", diet: "Jain", spice_tolerance: "Low", avoid_ingredients: ["onion", "garlic", "potato"], preferences: ["soft_food", "easy_digest"] },
        { id: "m_2", name: "Dadi Ji", role: "Grandmother", diet: "Jain", spice_tolerance: "Low", avoid_ingredients: ["onion", "garlic", "potato"], preferences: ["soft_food", "high_protein"] }
      ];
      this.availableIngredients = new Set(["Toor Dal", "Rice", "Ghee", "Turmeric", "Cumin Seeds", "Hing", "Salt", "Jaggery"]);
    } else if (presetId === 'working_couple') {
      this.members = [
        { id: "m_1", name: "Pooja", role: "Self", diet: "Vegan", spice_tolerance: "Medium", avoid_ingredients: ["dairy", "ghee", "paneer"], preferences: ["high_protein", "quick"] },
        { id: "m_2", name: "Aniket", role: "Partner", diet: "Vegetarian", spice_tolerance: "Spicy", avoid_ingredients: [], preferences: ["maharashtrian"] }
      ];
      this.availableIngredients = new Set(["Sprouted Matki", "Onion", "Tomato", "Garlic", "Ginger", "Goda Masala", "Oil", "Salt", "Coriander"]);
    }

    this.renderMembers();
    this.renderPantryPills();
    this.solve();
    App.showToast(`✨ Loaded preset: ${presetId.replace('_', ' ').toUpperCase()}!`);
  },

  openMemberModal(memberId = null) {
    const backdrop = document.getElementById('member-modal-backdrop');
    const form = document.getElementById('member-form');
    if (!backdrop || !form) return;

    if (memberId) {
      const m = this.members.find(x => x.id === memberId);
      if (m) {
        document.getElementById('member-form-id').value = m.id;
        document.getElementById('member-form-name').value = m.name;
        document.getElementById('member-form-role').value = m.role;
        document.getElementById('member-form-diet').value = m.diet;
        document.getElementById('member-form-spice').value = m.spice_tolerance;
        document.getElementById('member-form-avoid').value = m.avoid_ingredients.join(', ');
        document.getElementById('member-form-custom').value = m.custom_preference || '';

        // Preferences checkboxes
        ['soft_food', 'high_protein', 'kid_friendly', 'easy_digest', 'quick', 'one_pot', 'healthy'].forEach(pref => {
          const cb = document.getElementById(`pref-${pref}`);
          if (cb) cb.checked = m.preferences.includes(pref);
        });
      }
    } else {
      // New member defaults
      document.getElementById('member-form-id').value = '';
      document.getElementById('member-form-name').value = '';
      document.getElementById('member-form-role').value = 'Family Member';
      document.getElementById('member-form-diet').value = 'Vegetarian';
      document.getElementById('member-form-spice').value = 'Low';
      document.getElementById('member-form-avoid').value = '';
      document.getElementById('member-form-custom').value = '';
      ['soft_food', 'high_protein', 'kid_friendly', 'easy_digest', 'quick', 'one_pot', 'healthy'].forEach(pref => {
        const cb = document.getElementById(`pref-${pref}`);
        if (cb) cb.checked = false;
      });
    }

    backdrop.classList.add('show');
  },

  closeMemberModal() {
    const backdrop = document.getElementById('member-modal-backdrop');
    if (backdrop) backdrop.classList.remove('show');
  },

  editMember(memberId) {
    this.openMemberModal(memberId);
  },

  removeMember(memberId) {
    if (this.members.length <= 1) {
      App.showToast('Household must have at least 1 member.');
      return;
    }
    this.members = this.members.filter(m => m.id !== memberId);
    this.persistState();
    this.renderMembers();
    this.solve();
    App.showToast('Member removed.');
  },

  saveMemberFromForm() {
    const memberId = document.getElementById('member-form-id')?.value;
    const name = document.getElementById('member-form-name')?.value.trim() || 'Family Member';
    const role = document.getElementById('member-form-role')?.value || 'Family Member';
    const diet = document.getElementById('member-form-diet')?.value || 'Vegetarian';
    const spice = document.getElementById('member-form-spice')?.value || 'Medium';
    const avoidRaw = document.getElementById('member-form-avoid')?.value.trim() || '';
    const customPreference = document.getElementById('member-form-custom')?.value.trim() || '';
    const avoidList = avoidRaw ? avoidRaw.split(',').map(x => x.trim()).filter(Boolean) : [];

    const selectedPrefs = [];
    ['soft_food', 'high_protein', 'kid_friendly', 'easy_digest', 'quick', 'one_pot', 'healthy'].forEach(pref => {
      const cb = document.getElementById(`pref-${pref}`);
      if (cb && cb.checked) selectedPrefs.push(pref);
    });

    if (memberId) {
      // Update existing
      const m = this.members.find(x => x.id === memberId);
      if (m) {
        m.name = name;
        m.role = role;
        m.diet = diet;
        m.spice_tolerance = spice;
        m.avoid_ingredients = avoidList;
        m.custom_preference = customPreference;
        m.preferences = selectedPrefs;
      }
    } else {
      // Add new
      this.members.push({
        id: 'm_' + Date.now(),
        name: name,
        role: role,
        diet: diet,
        spice_tolerance: spice,
        avoid_ingredients: avoidList,
        custom_preference: customPreference,
        preferences: selectedPrefs
      });
    }

    this.closeMemberModal();
    this.persistState();
    this.renderMembers();
    this.solve();
    App.showToast(`✓ Saved profile for ${name}!`);
  },

  // Pantry Items
  addPantryItem(name) {
    if (!name) return;
    const formatted = name.charAt(0).toUpperCase() + name.slice(1);
    this.availableIngredients.add(formatted);
    this.persistState();
    this.renderPantryPills();
    this.updateQuickChips();
    this.solve();
  },

  removePantryItem(name) {
    this.availableIngredients.delete(name);
    this.persistState();
    this.renderPantryPills();
    this.updateQuickChips();
    this.solve();
  },

  togglePantryChip(name) {
    if (this.availableIngredients.has(name)) {
      this.availableIngredients.delete(name);
    } else {
      this.availableIngredients.add(name);
    }
    this.persistState();
    this.renderPantryPills();
    this.updateQuickChips();
    this.solve();
  },

  updateQuickChips() {
    document.querySelectorAll('.household-quick-chip').forEach(chip => {
      const name = chip.dataset.name;
      if (this.availableIngredients.has(name)) {
        chip.classList.add('selected');
      } else {
        chip.classList.remove('selected');
      }
    });
  },

  renderPantryPills() {
    const container = document.getElementById('household-pills-container');
    if (!container) return;

    if (this.availableIngredients.size === 0) {
      container.innerHTML = `<span style="color: var(--text-dim); font-size: 13px;">No ingredients selected. (All database meals will be evaluated)</span>`;
      return;
    }

    let html = '';
    this.availableIngredients.forEach(item => {
      html += `
        <span class="pantry-pill">
          ${item}
          <span class="chip-remove" onclick="HouseholdModule.removePantryItem('${item}')">&times;</span>
        </span>
      `;
    });
    container.innerHTML = html;
  },

  async solve() {
    const bestMealContainer = document.getElementById('household-best-meal-container');
    const runnerUpContainer = document.getElementById('household-runnerup-container');
    if (!bestMealContainer) return;

    bestMealContainer.innerHTML = `
      <div style="text-align: center; padding: 60px; background: var(--bg-card); border-radius: var(--radius-lg); border: 1px solid var(--border-light);">
        <div class="spinner"></div>
        <h3 style="margin-top: 16px; color: #fff;">Solving for ONE Shared Household Meal...</h3>
        <p style="color: var(--text-muted); font-size: 14px; margin-top: 6px;">Combining ${this.members.length} family members' diets, spice levels, and dietary constraints...</p>
      </div>
    `;
    if (runnerUpContainer) runnerUpContainer.innerHTML = '';

    const servings = parseInt(document.getElementById('household-servings-input')?.value || this.members.length);
    const maxTime = document.getElementById('household-max-time')?.value || null;
    const cuisine = document.getElementById('household-cuisine')?.value || 'All';
    const meal = document.getElementById('household-meal')?.value || 'All';
    const householdType = document.getElementById('household-type')?.value || 'family';
    const onePot = !!document.getElementById('household-one-pot')?.checked;

    if (!this.members.length) {
      bestMealContainer.innerHTML = '<div class="empty-state">Add at least one household member to continue.</div>';
      return;
    }

    try {
      const res = await API.solveHousehold({
        members: this.members,
        available_ingredients: Array.from(this.availableIngredients),
        servings: servings,
        max_time_mins: maxTime ? parseInt(maxTime) : null,
        cuisine: cuisine !== 'All' ? cuisine : null,
        meal_type: meal !== 'All' ? meal : null,
        household_type: householdType,
        one_pot: onePot
      });

      this.lastBestMeal = res.best_shared_meal;
      this.renderBestMeal(res.best_shared_meal, bestMealContainer, res);
      if (runnerUpContainer) {
        this.renderRunnerUps(res.runner_up_meals, runnerUpContainer);
      }
    } catch (e) {
      bestMealContainer.innerHTML = `
        <div style="text-align: center; padding: 40px; color: var(--danger); background: var(--bg-card); border-radius: var(--radius-lg);">
          Failed to solve household meal. Please check server connection.
        </div>
      `;
    }
  },

  addBestMealToShoppingList() {
    const meal = this.lastBestMeal;
    if (!meal) return;
    ShoppingListModule.addScaledIngredients(meal.recipe.id, meal.recipe.title, meal.scaled_ingredients || []);
  },

  addBestMealMissingToShoppingList() {
    const meal = this.lastBestMeal;
    if (!meal) return;
    ShoppingListModule.addMissing(meal.recipe.id, meal.recipe.title, meal.missing_ingredient_details || []);
  },

  renderBestMeal(bestMeal, container, response = null) {
    if (!bestMeal) {
      container.innerHTML = `
        <div style="text-align: center; padding: 50px; background: var(--bg-card); border-radius: var(--radius-lg); border: 1px solid var(--border-light);">
          <div style="font-size: 44px; margin-bottom: 12px;">🥘</div>
          <h3 style="color: #fff; margin-bottom: 8px;">No Single Meal Satisfied Every Strict Constraint</h3>
          <p style="color: var(--text-muted); max-width: 500px; margin: 0 auto; font-size: 14px;">
            The combined constraints of your household (e.g. strict diets + avoided ingredients + time limit) were too restrictive. Try relaxing one of the avoided ingredients or time ceilings!
          </p>
        </div>
      `;
      return;
    }

    const r = bestMeal.recipe;
    const harmonyPct = bestMeal.household_harmony_percentage;
    const harmonyClass = harmonyPct >= 90 ? 'high' : (harmonyPct >= 75 ? 'medium' : 'low');

    container.innerHTML = `
      <div class="household-hero-card">
        <!-- Crown Banner Header -->
        <div class="household-hero-header">
          <div>
            <span class="hero-crown-badge">👑 ONE SHARED MEAL FOR YOUR ENTIRE HOUSEHOLD</span>
            <h2 class="hero-meal-title">${r.title}</h2>
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 8px;">
              <span class="cuisine-badge">${r.regional_cuisine}</span>
              ${bestMeal.dietary_badges.map(b => `<span class="ready-badge ready">${b}</span>`).join('')}
              <span class="mini-tag" style="background: rgba(255,255,255,0.08); color: #fff;">⏱️ ${bestMeal.total_time_mins} mins</span>
              <span class="mini-tag" style="background: rgba(255,255,255,0.08); color: #fff;">🍽️ Serves ${bestMeal.total_household_servings} People</span>
            </div>
          </div>

          <!-- Harmony Meter Circle/Badge -->
          <div class="harmony-score-box">
            <div class="harmony-score-val">${harmonyPct}%</div>
            <div class="harmony-score-label">Household Harmony</div>
          </div>
        </div>

        <!-- Honest solver status -->
        <div class="household-verdict-bar">
          <b>${bestMeal.summary_verdict}</b>
          ${bestMeal.strict_constraints_failed?.length ? `<div style="margin-top:6px;font-size:12px;color:#FCD34D;">Constraint to adjust: ${bestMeal.strict_constraints_failed.join(' • ')}</div>` : ''}
        </div>
        ${bestMeal.explanation ? `<div class="why-meal-box"><b>Why we chose this</b><p>${bestMeal.explanation}</p></div>` : ''}

        <!-- Summary Description -->
        <p style="color: var(--text-muted); font-size: 15px; margin: 16px 0; line-height: 1.6;">
          ${r.summary}
        </p>

        <!-- MEMBER-BY-MEMBER SATISFACTION BREAKDOWN -->
        <div style="margin: 24px 0;">
          <h3 style="font-size: 18px; color: #fff; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
            <span>👨‍👩‍👧‍👦 Why This 1 Meal Works for Everyone:</span>
          </h3>
          <div class="member-breakdown-grid">
            ${bestMeal.member_explanations.map(exp => `
              <div class="member-explain-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                  <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 20px;">${this.getRoleAvatar(exp.role)}</span>
                    <span style="font-weight: 700; color: #fff; font-size: 14px;">${exp.member_name}</span>
                  </div>
                  <span class="mini-tag" style="background: ${exp.is_fully_satisfied ? 'rgba(16,185,129,0.2)' : 'rgba(245,158,11,0.2)'}; color: ${exp.is_fully_satisfied ? '#4ADE80' : '#FCD34D'};">
                    ${exp.satisfaction_score}% Fit
                  </span>
                </div>

                <ul style="list-style: none; display: flex; flex-direction: column; gap: 4px; font-size: 12px; color: #A7F3D0;">
                  ${exp.satisfied_aspects.map(asp => `<li>${asp}</li>`).join('')}
                </ul>

                ${exp.compromises_or_tips.length > 0 ? `
                  <div style="margin-top: 6px; padding-top: 6px; border-top: 1px dashed rgba(255,255,255,0.1); font-size: 11px; color: #FCD34D;">
                    ${exp.compromises_or_tips.map(tip => `<div>${tip}</div>`).join('')}
                  </div>
                ` : ''}
              </div>
            `).join('')}
          </div>
        </div>

        <!-- FINAL ONE-RECIPE HOUSEHOLD PLAN -->
        ${r.household_adapted ? `
        <div style="margin:18px 0;background:var(--bg-input);border:1px solid rgba(74,222,128,.25);border-radius:var(--radius-md);padding:18px;">
          <div style="font-size:13px;font-weight:800;color:#86EFAC;text-transform:uppercase;margin-bottom:8px;">✓ Final Recipe Adapted for Everyone</div>
          <p style="font-size:14px;color:#fff;line-height:1.6;margin:0 0 10px;">This is still <b>one recipe for the whole household</b>. The solver has changed only the ingredients or finishing steps needed to satisfy the household constraints.</p>
          ${r.household_global_swaps?.length ? `<div style="display:grid;gap:7px;">${r.household_global_swaps.map(x => `<div style="font-size:12px;color:#D1FAE5;"><b>${x.original} → ${x.replacement}</b><br>${x.instruction}</div>`).join('')}</div>` : ''}
          ${r.household_portion_steps?.length ? `<div style="margin-top:10px;display:grid;gap:7px;">${r.household_portion_steps.map(x => `<div style="font-size:12px;color:#D1FAE5;"><b>${x.member}:</b> ${x.instruction}</div>`).join('')}</div>` : ''}
        </div>` : ''}

        <!-- ONE-POT DESI FAMILY CUSTOMIZATION TIP -->
        <div class="one-pot-hack-box">
          <div style="font-size: 13px; font-weight: 800; color: #FFD8A8; text-transform: uppercase; margin-bottom: 6px; display: flex; align-items: center; gap: 6px;">
            <span>💡 How to Serve Everyone From 1 Recipe:</span>
          </div>
          <p style="font-size: 14px; color: #FFFFFF; line-height: 1.6; margin:0;">
            ${bestMeal.family_customization_tip}
          </p>
        </div>

        ${bestMeal.member_adaptations?.length ? `
        <div style="margin:18px 0; background:var(--bg-input); border:1px solid var(--border-light); border-radius:var(--radius-md); padding:18px;">
          <div style="font-size:13px;font-weight:800;color:#FFD8A8;text-transform:uppercase;margin-bottom:10px;">🍽️ Individual Adaptations — Same Recipe, Different Needs</div>
          <div style="display:grid;gap:10px;">
            ${bestMeal.member_adaptations.map(a => `
              <div style="padding:12px;border:1px solid rgba(255,255,255,.08);border-radius:10px;background:rgba(255,255,255,.025);">
                <div style="font-weight:800;color:#fff;margin-bottom:7px;">${a.member_name}</div>
                ${a.adjustments.map(x => `
                  <div style="font-size:12px;color:#D1FAE5;margin:5px 0;">
                    <b>${x.original_ingredient || 'Adjustment'} → ${x.replacement}</b><br>${x.instruction}
                  </div>`).join('')}
              </div>`).join('')}
          </div>
          <div style="font-size:11px;color:var(--text-dim);margin-top:10px;">The solver uses recipe-specific substitutions when available. For strict allergies or medically prescribed diets, verify every replacement before cooking.</div>
        </div>` : ''}

        <!-- SCALED INGREDIENTS FOR THE HOUSEHOLD -->
        <div style="margin: 24px 0; background: var(--bg-input); border: 1px solid var(--border-light); border-radius: var(--radius-md); padding: 20px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <div>
              <h4 style="font-size: 16px; color: #fff;">Exact Quantities for Your Household of ${bestMeal.total_household_servings}</h4>
              <div style="font-size: 12px; color: var(--text-muted);">
                ${bestMeal.missing_ingredients.length === 0 ? '✓ You have all ingredients available!' : `Missing ${bestMeal.missing_ingredients.length} items`}
              </div>
            </div>
            ${bestMeal.missing_ingredients.length > 0 ? `
              <button class="btn-secondary" style="font-size: 12px; padding: 6px 12px;" onclick="HouseholdModule.addBestMealMissingToShoppingList()">
                🛒 Add Missing to Shopping List
              </button>
            ` : ''}
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 8px;">
            ${bestMeal.scaled_ingredients.map(ing => `
              <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-light); border-radius: var(--radius-sm); padding: 8px 12px; font-size: 13px; display: flex; justify-content: space-between;">
                <span style="color: #fff;">${ing.name}${ing.household_replaced_from ? `<small style="display:block;color:#86EFAC;font-size:11px;">↳ replaces ${ing.household_replaced_from}</small>` : ''}</span>
                <b style="color: var(--accent-gold);">${ing.display_quantity} ${ing.unit}</b>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- ACTIONS -->
        <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-top: 20px;">
          <button class="btn-primary" style="flex: 2; padding: 14px 24px; font-size: 16px; justify-content: center;" onclick="RecipeModal.open('${r.id}')">
            🍳 Launch Cooking Mode for ${r.title}
          </button>
          <button class="btn-secondary" style="flex: 1; justify-content: center;" onclick="HouseholdModule.addBestMealToShoppingList()">
            📋 Save Entire Grocery List
          </button>
        </div>
      </div>
    `;
  },

  renderRunnerUps(runnerUps, container) {
    if (!runnerUps || runnerUps.length === 0) {
      container.innerHTML = '';
      return;
    }

    let html = `
      <div style="margin-top: 36px;">
        <h3 style="font-size: 20px; color: #fff; margin-bottom: 16px;">
          🥈 Alternative Shared Meals for Your Household
        </h3>
        <div class="results-grid">
    `;

    runnerUps.forEach(item => {
      const r = item.recipe;
      html += `
        <div class="recipe-card">
          ${RecipeVisuals.card(r)}
<div class="recipe-header">
            <div class="badge-row">
              <span class="cuisine-badge">${r.regional_cuisine}</span>
              <span class="ready-badge ready">${item.household_harmony_percentage}% Harmony</span>
            </div>
            <h3 class="recipe-title">${r.title}</h3>
            <div class="recipe-meta">
              <span class="meta-item">⏱️ ${r.total_time_mins}m</span>
              <span class="meta-item">🌱 ${r.diet}</span>
              <span class="meta-item">🍽️ Serves ${item.total_household_servings}</span>
            </div>
            <p class="recipe-summary">${r.summary}</p>
          </div>

          <div class="recipe-body">
            <div style="font-size: 12px; color: #A7F3D0; margin-bottom: 12px; background: rgba(16,185,129,0.1); padding: 8px 10px; border-radius: 6px;">
              <b>Family Fit:</b> ${item.summary_verdict}
            </div>

            <div class="card-actions">
              <button class="btn-card-primary" onclick="RecipeModal.open('${r.id}')">
                🍳 View Recipe
              </button>
            </div>
          </div>
        </div>
      `;
    });

    html += `</div></div>`;
    container.innerHTML = html;
  }
};
