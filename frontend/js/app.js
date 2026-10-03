/**
 * MealSolver Master Orchestrator Application
 */

const App = {
  currentTab: 'household',
  allIngredientsCache: [],

  init() {
    this.bindGlobalEvents();
    this.initAutocomplete();
    
    // Initialize feature modules
    HouseholdModule.init();
    PantryModule.init();
    CravingModule.init();
    LeftoversModule.init();
    ScannerModule.init();
    RecipeModal.init();
    ShoppingListModule.init();
    this.loadCatalog();
  },

  filterForHousehold(recipes) {
    return typeof HouseholdConstraints !== 'undefined' ? HouseholdConstraints.filterRecipes(recipes) : (recipes || []);
  },

  bindGlobalEvents() {
    // Tab switching
    document.querySelectorAll('.mode-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        const target = tab.dataset.tab;
        this.switchTab(target);
      });
    });

    // Catalog search and filters
    const catSearch = document.getElementById('catalog-search-input');
    if (catSearch) {
      catSearch.addEventListener('input', () => this.loadCatalog());
    }

    ['catalog-cuisine', 'catalog-diet', 'catalog-meal'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.addEventListener('change', () => this.loadCatalog());
    });
  },

  switchTab(tabId) {
    this.currentTab = tabId;

    // Update active tab button
    document.querySelectorAll('.mode-tab').forEach(tab => {
      if (tab.dataset.tab === tabId) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });

    // Update active tab content section
    document.querySelectorAll('.tab-content').forEach(section => {
      if (section.id === `tab-${tabId}`) {
        section.classList.add('active');
      } else {
        section.classList.remove('active');
      }
    });

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Refresh active section if needed
    if (tabId === 'catalog') {
      this.loadCatalog();
    }
  },

  async initAutocomplete() {
    try {
      const res = await API.getAllIngredients();
      this.allIngredientsCache = res.ingredients || [];

      const datalist = document.getElementById('ingredients-datalist');
      if (datalist && this.allIngredientsCache.length > 0) {
        datalist.innerHTML = this.allIngredientsCache.map(i => `<option value="${i}">`).join('');
      }
    } catch (e) {
      console.warn('Could not load ingredient datalist', e);
    }
  },

  async loadCatalog() {
    const container = document.getElementById('catalog-results-grid');
    const countContainer = document.getElementById('catalog-total-count');
    if (!container) return;

    const search = document.getElementById('catalog-search-input')?.value.trim() || '';
    const cuisine = document.getElementById('catalog-cuisine')?.value || 'All';
    const diet = document.getElementById('catalog-diet')?.value || 'All';
    const meal = document.getElementById('catalog-meal')?.value || 'All';

    container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px;"><div class="spinner"></div></div>`;

    try {
      // Explore is a catalog, not the strict household solver. Always ask for the
      // complete catalog and show household compatibility as a badge instead of
      // hiding recipes. This prevents a strict/conflicting household profile from
      // making Explore All look empty.
      let res = await API.getRecipes({
        search: search || undefined,
        cuisine: cuisine !== 'All' ? cuisine : undefined,
        diet: diet !== 'All' ? diet : undefined,
        meal_type: meal !== 'All' ? meal : undefined,
        limit: 150
      });

      // Defensive fallback: if an API/proxy ever returns an empty filtered catalog,
      // fetch the complete catalog and apply the simple filters locally.
      if ((!res.recipes || res.recipes.length === 0) && !search && cuisine === 'All' && diet === 'All' && meal === 'All') {
        res = await API.getRecipes({limit: 150});
      }

      if (countContainer) {
        countContainer.innerText = `${res.total || (res.recipes || []).length} recipes available`;
      }
      this.renderCatalog(res.recipes || [], container);
    } catch (e) {
      container.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--danger);">Failed to load recipes.</div>`;
    }
  },

  renderCatalog(recipes, container) {
    if (!recipes || recipes.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 40px; background: var(--bg-card); border-radius: var(--radius-lg);">
          <div style="font-size: 36px; margin-bottom: 10px;">🔍</div>
          <h3>No recipes matched your search filter</h3>
        </div>
      `;
      return;
    }

    let html = '';
    recipes.forEach(r => {
      html += `
        <div class="recipe-card">
          ${RecipeVisuals.card(r)}
<div class="recipe-header">
            <div class="badge-row">
              <span class="cuisine-badge">${r.regional_cuisine}</span>
              <span class="ready-badge ready">🌱 ${r.diet}</span>
              ${(() => { const f = typeof HouseholdConstraints !== 'undefined' ? HouseholdConstraints.explain(r) : {ok:true}; return `<span class="household-fit-badge ${f.ok ? 'fit' : 'conflict'}">${f.ok ? '✓ Household fit' : '⚠ Check household'}</span>`; })()}
            </div>
            <h3 class="recipe-title">${r.title}</h3>
            <div class="recipe-meta">
              <span class="meta-item">⏱️ ${r.total_time_mins}m</span>
              <span class="meta-item">🔥 ${r.difficulty}</span>
              <span class="meta-item">🥣 ${r.meal_type.slice(0, 2).join(', ')}</span>
              <span class="meta-item">👥 ${Math.max(1, (typeof HouseholdConstraints !== 'undefined' ? HouseholdConstraints.getMembers().length : 0) || r.nutrition_per_serving?.servings || 2)} people</span>
            </div>
            <p class="recipe-summary">${r.summary}</p>
          </div>

          <div class="recipe-body">
            <div class="ingredients-preview">
              <div style="font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Key Ingredients:</div>
              <div class="matched-tags">
                ${r.ingredients.slice(0, 5).map(i => `<span class="mini-tag" style="background: rgba(255,255,255,0.06); color: #fff;">${i.name}</span>`).join('')}
              </div>
            </div>

            <div class="card-actions">
              <button class="btn-card-primary" onclick="RecipeModal.open('${r.id}')">
                🍳 View Recipe & Scale
              </button>
            </div>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  },

  showToast(message) {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerText = message;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
};

// Bootstrap app on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});
