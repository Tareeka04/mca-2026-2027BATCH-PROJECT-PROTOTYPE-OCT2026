/**
 * Pantry Solver Module
 * Handles ingredient selection, chip toggles, pantry matching, and result rendering
 */

const PantryModule = {
  selectedIngredients: new Set([
    "Onion", "Potato", "Green Chillies", "Turmeric", "Mustard Seeds", "Peanuts", "Poha"
  ]),

  init() {
    this.renderSelectedPills();
    this.bindEvents();
    // Trigger initial solve
    this.solve();
  },

  bindEvents() {
    const addInput = document.getElementById('pantry-input');
    const addBtn = document.getElementById('pantry-add-btn');
    const clearBtn = document.getElementById('pantry-clear-btn');
    const solveBtn = document.getElementById('pantry-solve-btn');

    if (addBtn && addInput) {
      const addItem = () => {
        const val = addInput.value.trim();
        if (val) {
          this.addIngredient(val);
          addInput.value = '';
        }
      };

      addBtn.addEventListener('click', addItem);
      addInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addItem();
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        this.selectedIngredients.clear();
        this.renderSelectedPills();
        this.updateQuickChips();
        this.solve();
      });
    }

    if (solveBtn) {
      solveBtn.addEventListener('click', () => this.solve());
    }

    // Filter changes
    ['pantry-diet', 'pantry-time', 'pantry-cuisine', 'pantry-meal'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.addEventListener('change', () => this.solve());
    });
  },

  addIngredient(name) {
    if (!name) return;
    const formatted = name.charAt(0).toUpperCase() + name.slice(1);
    this.selectedIngredients.add(formatted);
    this.renderSelectedPills();
    this.updateQuickChips();
    this.solve();
  },

  removeIngredient(name) {
    this.selectedIngredients.delete(name);
    this.renderSelectedPills();
    this.updateQuickChips();
    this.solve();
  },

  toggleQuickChip(name) {
    if (this.selectedIngredients.has(name)) {
      this.selectedIngredients.delete(name);
    } else {
      this.selectedIngredients.add(name);
    }
    this.renderSelectedPills();
    this.updateQuickChips();
    this.solve();
  },

  updateQuickChips() {
    document.querySelectorAll('.pantry-quick-chip').forEach(chip => {
      const name = chip.dataset.name;
      if (this.selectedIngredients.has(name)) {
        chip.classList.add('selected');
      } else {
        chip.classList.remove('selected');
      }
    });
  },

  renderSelectedPills() {
    const container = document.getElementById('pantry-pills-container');
    if (!container) return;

    if (this.selectedIngredients.size === 0) {
      container.innerHTML = `<span style="color: var(--text-dim); font-size: 13px;">No ingredients selected yet. Tap chips above or type your items!</span>`;
      return;
    }

    let html = '';
    this.selectedIngredients.forEach(item => {
      html += `
        <span class="pantry-pill">
          ${item}
          <span class="chip-remove" onclick="PantryModule.removeIngredient('${item}')">&times;</span>
        </span>
      `;
    });
    container.innerHTML = html;
  },

  async solve() {
    const resultsContainer = document.getElementById('pantry-results-grid');
    const countContainer = document.getElementById('pantry-match-count');
    if (!resultsContainer) return;

    resultsContainer.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px;"><div class="spinner"></div><p style="color: var(--text-muted); margin-top: 10px;">Finding best meals with your ingredients...</p></div>`;

    const ingredientsList = Array.from(this.selectedIngredients);
    if (ingredientsList.length === 0) {
      resultsContainer.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted);">Please add at least 1 ingredient to find matching recipes.</div>`;
      if (countContainer) countContainer.innerText = '0 recipes found';
      return;
    }

    const diet = document.getElementById('pantry-diet')?.value || 'All';
    const maxTime = document.getElementById('pantry-time')?.value || null;
    const cuisine = document.getElementById('pantry-cuisine')?.value || 'All';
    const meal = document.getElementById('pantry-meal')?.value || 'All';

    try {
      const res = await API.solvePantry({
        ingredients: ingredientsList,
        filters: {
          diet: diet !== 'All' ? diet : null,
          max_time_mins: maxTime ? parseInt(maxTime) : null,
          cuisine: cuisine !== 'All' ? cuisine : null,
          meal_type: meal !== 'All' ? meal : null
        },
        include_substitutes: true
      });

      if (countContainer) {
        countContainer.innerText = `${res.total_matches} recipes found (${res.ready_to_cook_count} ready to cook now)`;
      }

      const orderedResults = [...(res.results || [])].sort((a, b) => {
        const ar = a.recipe || a; const br = b.recipe || b;
        const af = typeof HouseholdConstraints !== 'undefined' ? HouseholdConstraints.explain(ar).ok : true;
        const bf = typeof HouseholdConstraints !== 'undefined' ? HouseholdConstraints.explain(br).ok : true;
        return Number(bf) - Number(af);
      });
      this.renderResults(orderedResults, resultsContainer);
    } catch (e) {
      resultsContainer.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--danger);">Failed to load matches. Ensure backend server is running.</div>`;
    }
  },

  renderResults(results, container) {
    if (!results || results.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 40px; background: var(--bg-card); border-radius: var(--radius-lg);">
          <div style="font-size: 36px; margin-bottom: 10px;">🔍</div>
          <h3>No exact matches found</h3>
          <p style="color: var(--text-muted); margin-top: 6px;">Try selecting a few more common ingredients or relaxing your diet/time filters.</p>
        </div>
      `;
      return;
    }

    let html = '';
    results.forEach(item => {
      const r = item.recipe;
      const matchPct = item.match_percentage;
      const readyBadgeClass = item.is_ready_to_cook ? 'ready' : (item.missing_ingredients.length === 1 ? 'missing-1' : 'missing-more');
      const progressClass = matchPct >= 75 ? 'high' : (matchPct >= 45 ? 'medium' : 'low');

      // Substitute text if any
      let subHtml = '';
      if (item.substitute_suggestions && Object.keys(item.substitute_suggestions).length > 0) {
        const subItems = Object.entries(item.substitute_suggestions).map(([k, v]) => `<b>${k}</b> ➔ ${v[0]}`).join(' | ');
        subHtml = `<div style="background: rgba(233, 196, 106, 0.1); border: 1px solid rgba(233, 196, 106, 0.3); padding: 6px 10px; border-radius: 6px; font-size: 11px; color: #FCD34D; margin: 8px 0;">💡 Substitutes available: ${subItems}</div>`;
      }

      html += `
        <div class="recipe-card">
          ${RecipeVisuals.card(r)}
<div class="recipe-header">
            <div class="badge-row">
              <span class="household-fit-badge ${HouseholdConstraints.explain(r).ok ? 'fit' : 'conflict'}">${HouseholdConstraints.explain(r).ok ? '✓ Household fit' : '⚠ Check household'}</span>
              <span class="cuisine-badge">${r.regional_cuisine}</span>
              <span class="ready-badge ${readyBadgeClass}">${item.ready_badge}</span>
            </div>
            <h3 class="recipe-title">${r.title}</h3>
            <div class="recipe-meta">
              <span class="meta-item">⏱️ ${r.total_time_mins}m</span>
              <span class="meta-item">🔥 ${r.difficulty}</span>
              <span class="meta-item">🌱 ${r.diet}</span>
            </div>
            <p class="recipe-summary">${r.summary}</p>
            
            <div class="progress-wrap">
              <div class="progress-label-row">
                <span>Pantry Match</span>
                <span>${matchPct}%</span>
              </div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill ${progressClass}" style="width: ${matchPct}%"></div>
              </div>
            </div>

            ${subHtml}
          </div>

          <div class="recipe-body">
            <div class="ingredients-preview">
              <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Ingredients Breakdown:</div>
              <div class="matched-tags">
                ${item.matched_ingredients.slice(0, 4).map(m => `<span class="mini-tag matched">✓ ${m}</span>`).join('')}
                ${item.missing_ingredients.slice(0, 3).map(m => `<span class="mini-tag missing">✗ ${m}</span>`).join('')}
              </div>
            </div>

            <div class="card-actions">
              <button class="btn-card-primary" onclick="RecipeModal.open('${r.id}')">
                🍳 View Recipe & Cook
              </button>
              ${item.missing_ingredients.length > 0 ? `
                <button class="btn-card-icon" title="Add missing items to shopping list" onclick="ShoppingListModule.addMissing('${r.id}', '${r.title.replace(/'/g, "\\'")}', ${JSON.stringify(item.missing_ingredients).replace(/"/g, '&quot;')})">
                  🛒
                </button>
              ` : ''}
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }
};
