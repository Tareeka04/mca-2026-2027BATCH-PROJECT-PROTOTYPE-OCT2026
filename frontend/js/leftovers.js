/**
 * Leftover Transformation Module
 * Maps household leftover staples to quick transformations and chef tips
 */

const LeftoversModule = {
  selectedStaples: new Set(["cooked rice"]),

  init() {
    this.bindEvents();
    this.solve();
  },

  bindEvents() {
    document.querySelectorAll('.leftover-choice-card').forEach(card => {
      card.addEventListener('click', () => {
        const staple = card.dataset.staple;
        this.toggleStaple(staple, card);
      });
    });

    ['leftover-diet', 'leftover-time'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.addEventListener('change', () => this.solve());
    });
  },

  toggleStaple(staple, cardEl) {
    if (this.selectedStaples.has(staple)) {
      this.selectedStaples.delete(staple);
      if (cardEl) cardEl.classList.remove('selected');
    } else {
      this.selectedStaples.add(staple);
      if (cardEl) cardEl.classList.add('selected');
    }
    this.solve();
  },

  async solve() {
    const container = document.getElementById('leftover-results-grid');
    const countContainer = document.getElementById('leftover-match-count');
    if (!container) return;

    const staplesList = Array.from(this.selectedStaples);
    if (staplesList.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 40px; background: var(--bg-card); border-radius: var(--radius-lg);">
          <div style="font-size: 36px; margin-bottom: 10px;">♻️</div>
          <h3>Select a leftover above to see delicious transformations</h3>
          <p style="color: var(--text-muted); margin-top: 6px;">E.g. Cooked Rice, Stale Roti/Chapati, Leftover Dal, Boiled Potatoes...</p>
        </div>
      `;
      if (countContainer) countContainer.innerText = '0 transformations found';
      return;
    }

    container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px;"><div class="spinner"></div><p style="color: var(--text-muted); margin-top: 10px;">Cooking up leftover magic...</p></div>`;

    const diet = document.getElementById('leftover-diet')?.value || 'All';
    const maxTime = document.getElementById('leftover-time')?.value || null;

    try {
      const res = await API.solveLeftovers({
        leftover_items: staplesList,
        filters: {
          diet: diet !== 'All' ? diet : null,
          max_time_mins: maxTime ? parseInt(maxTime) : null
        }
      });

      if (countContainer) {
        countContainer.innerText = `${res.total_transformations} leftover transformations found`;
      }

      const orderedResults = [...(res.results || [])].sort((a, b) => {
        const ar = a.recipe || a; const br = b.recipe || b;
        const af = typeof HouseholdConstraints !== 'undefined' ? HouseholdConstraints.explain(ar).ok : true;
        const bf = typeof HouseholdConstraints !== 'undefined' ? HouseholdConstraints.explain(br).ok : true;
        return Number(bf) - Number(af);
      });
      this.renderResults(orderedResults, container);
    } catch (e) {
      container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--danger);">Failed to load transformations.</div>`;
    }
  },

  renderResults(results, container) {
    if (!results || results.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 40px; background: var(--bg-card); border-radius: var(--radius-lg);">
          <div style="font-size: 36px; margin-bottom: 10px;">🍳</div>
          <h3>No matching transformations found for selected criteria</h3>
        </div>
      `;
      return;
    }

    let html = '';
    results.forEach(item => {
      const r = item.recipe;

      html += `
        <div class="recipe-card" style="border-top: 3px solid var(--secondary);">
          ${RecipeVisuals.card(r)}
<div class="recipe-header">
            <div class="badge-row">
              <span class="household-fit-badge ${HouseholdConstraints.explain(r).ok ? 'fit' : 'conflict'}">${HouseholdConstraints.explain(r).ok ? '✓ Household fit' : '⚠ Check household'}</span>
              <span class="cuisine-badge" style="background: rgba(42, 157, 143, 0.15); color: #2A9D8F; border-color: rgba(42, 157, 143, 0.4);">
                ♻️ Leftover: ${item.primary_leftover}
              </span>
              <span class="ready-badge ready">⚡ ${item.prep_speed_badge}</span>
            </div>
            <h3 class="recipe-title">${item.transformation_name}</h3>
            
            <div class="recipe-meta">
              <span class="meta-item">⏱️ ${r.total_time_mins}m</span>
              <span class="meta-item">🌱 ${r.diet}</span>
              <span class="meta-item">🚩 ${r.regional_cuisine}</span>
            </div>

            <div class="transformation-tip-box">
              <b>💡 Chef's Secret:</b> ${item.transformation_tip}
            </div>

            <p class="recipe-summary">${r.summary}</p>
          </div>

          <div class="recipe-body">
            <div class="ingredients-preview">
              <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">A Few Pantry Items Needed:</div>
              <div class="matched-tags">
                ${item.additional_needed.map(ing => `<span class="mini-tag matched">+ ${ing}</span>`).join('')}
              </div>
            </div>

            <div class="card-actions">
              <button class="btn-card-primary" style="background: linear-gradient(135deg, var(--secondary), #21867A);" onclick="RecipeModal.open('${r.id}')">
                🍳 Transform & Cook
              </button>
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }
};
