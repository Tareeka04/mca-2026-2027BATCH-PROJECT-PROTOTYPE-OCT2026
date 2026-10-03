/**
 * Craving & Mood Recommender Module
 * Combines free-text semantic IR, mood pills, and 4 taste sliders
 */

const CravingModule = {
  activeMood: null,

  init() {
    this.bindEvents();
    this.solve();
  },

  bindEvents() {
    const searchInput = document.getElementById('craving-search-input');
    const searchBtn = document.getElementById('craving-search-btn');

    if (searchBtn && searchInput) {
      searchBtn.addEventListener('click', () => this.solve());
      searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') this.solve();
      });
    }

    // Sliders
    ['slider-spicy', 'slider-tangy', 'slider-sweet', 'slider-comfort'].forEach(id => {
      const el = document.getElementById(id);
      const valDisplay = document.getElementById(`${id}-val`);
      if (el) {
        el.addEventListener('input', () => {
          if (valDisplay) valDisplay.innerText = el.value;
        });
        el.addEventListener('change', () => this.solve());
      }
    });

    // Reset Sliders
    const resetSlidersBtn = document.getElementById('reset-sliders-btn');
    if (resetSlidersBtn) {
      resetSlidersBtn.addEventListener('click', () => {
        ['slider-spicy', 'slider-tangy', 'slider-sweet', 'slider-comfort'].forEach(id => {
          const el = document.getElementById(id);
          const valDisplay = document.getElementById(`${id}-val`);
          if (el) {
            el.value = 2;
            if (valDisplay) valDisplay.innerText = 2;
          }
        });
        this.solve();
      });
    }
  },

  selectMood(mood) {
    if (this.activeMood === mood) {
      this.activeMood = null;
    } else {
      this.activeMood = mood;
    }

    // Update UI chips
    document.querySelectorAll('.craving-mood-chip').forEach(chip => {
      if (chip.dataset.mood === this.activeMood) {
        chip.classList.add('selected');
      } else {
        chip.classList.remove('selected');
      }
    });

    this.solve();
  },

  setPresetQuery(text) {
    const input = document.getElementById('craving-search-input');
    if (input) {
      input.value = text;
      this.solve();
    }
  },

  async solve() {
    const container = document.getElementById('craving-results-grid');
    const countContainer = document.getElementById('craving-match-count');
    if (!container) return;

    container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px;"><div class="spinner"></div><p style="color: var(--text-muted); margin-top: 10px;">Finding recipes tailored to your craving...</p></div>`;

    const queryText = document.getElementById('craving-search-input')?.value.trim() || '';
    const spicy = parseInt(document.getElementById('slider-spicy')?.value || 2);
    const tangy = parseInt(document.getElementById('slider-tangy')?.value || 2);
    const sweet = parseInt(document.getElementById('slider-sweet')?.value || 1);
    const comfort = parseInt(document.getElementById('slider-comfort')?.value || 3);

    const diet = document.getElementById('craving-diet')?.value || 'All';
    const maxTime = document.getElementById('craving-time')?.value || null;
    const cuisine = document.getElementById('craving-cuisine')?.value || 'All';

    try {
      const res = await API.solveCraving({
        query: queryText,
        spice_level: spicy,
        tangy_level: tangy,
        sweet_level: sweet,
        comfort_level: comfort,
        mood: this.activeMood,
        filters: {
          diet: diet !== 'All' ? diet : null,
          max_time_mins: maxTime ? parseInt(maxTime) : null,
          cuisine: cuisine !== 'All' ? cuisine : null
        },
        top_k: 18
      });

      if (countContainer) {
        countContainer.innerText = `${res.total_results} matching recipes found`;
      }

      const orderedResults = [...(res.results || [])].sort((a, b) => {
        const ar = a.recipe || a; const br = b.recipe || b;
        const af = typeof HouseholdConstraints !== 'undefined' ? HouseholdConstraints.explain(ar).ok : true;
        const bf = typeof HouseholdConstraints !== 'undefined' ? HouseholdConstraints.explain(br).ok : true;
        return Number(bf) - Number(af);
      });
      this.renderResults(orderedResults, container);
    } catch (e) {
      container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--danger);">Failed to load recommendations.</div>`;
    }
  },

  renderResults(results, container) {
    if (!results || results.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 40px; background: var(--bg-card); border-radius: var(--radius-lg);">
          <div style="font-size: 36px; margin-bottom: 10px;">🍲</div>
          <h3>No matching dishes found for this craving</h3>
          <p style="color: var(--text-muted); margin-top: 6px;">Try adjusting your flavor sliders or search terms.</p>
        </div>
      `;
      return;
    }

    let html = '';
    results.forEach(item => {
      const r = item.recipe;
      const relPct = item.relevance_percentage;
      const progressClass = relPct >= 75 ? 'high' : (relPct >= 50 ? 'medium' : 'low');

      html += `
        <div class="recipe-card">
          ${RecipeVisuals.card(r)}
<div class="recipe-header">
            <div class="badge-row">
              <span class="household-fit-badge ${HouseholdConstraints.explain(r).ok ? 'fit' : 'conflict'}">${HouseholdConstraints.explain(r).ok ? '✓ Household fit' : '⚠ Check household'}</span>
              <span class="cuisine-badge">${r.regional_cuisine}</span>
              <span class="ready-badge ready">✨ ${relPct}% Craving Match</span>
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
                <span>Flavor & Craving Alignment</span>
                <span>${relPct}%</span>
              </div>
              <div class="progress-bar-bg">
                <div class="progress-bar-fill ${progressClass}" style="width: ${relPct}%"></div>
              </div>
            </div>

            <!-- Taste Profile Badges -->
            <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px;">
              <span class="mini-tag" style="background: rgba(239, 68, 68, 0.15); color: #FCA5A5;">🌶️ Spice ${item.taste_profile.spicy}/5</span>
              <span class="mini-tag" style="background: rgba(245, 158, 11, 0.15); color: #FCD34D;">🍋 Tangy ${item.taste_profile.tangy}/5</span>
              <span class="mini-tag" style="background: rgba(16, 185, 129, 0.15); color: #6EE7B7;">🥣 Comfort ${item.taste_profile.comfort}/5</span>
            </div>
          </div>

          <div class="recipe-body">
            <div class="ingredients-preview">
              <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Why it matches:</div>
              <ul style="list-style: none; margin-top: 4px; font-size: 12px; color: #A7F3D0;">
                ${item.matched_reasons.map(reason => `<li>• ${reason}</li>`).join('')}
              </ul>
            </div>

            <div class="card-actions">
              <button class="btn-card-primary" onclick="RecipeModal.open('${r.id}')">
                🍳 View Recipe & Cook
              </button>
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }
};
