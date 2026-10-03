/**
 * Smart Shopping List Module
 * Aggregates missing ingredients across recipes, handles check-offs, and exports for WhatsApp / printing
 */

const ShoppingListModule = {
  items: [],

  init() {
    this.loadFromStorage();
    this.bindEvents();
    this.render();
  },

  bindEvents() {
    const backdrop = document.getElementById('cart-modal-backdrop');
    const openBtn = document.getElementById('nav-cart-btn');
    const closeBtn = document.getElementById('cart-modal-close');
    const clearBtn = document.getElementById('cart-clear-btn');
    const copyBtn = document.getElementById('cart-copy-btn');

    if (openBtn) openBtn.addEventListener('click', () => this.open());
    if (closeBtn && backdrop) {
      closeBtn.addEventListener('click', () => this.close());
      backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) this.close();
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        this.items = [];
        this.saveToStorage();
        this.render();
        App.showToast('Shopping list cleared');
      });
    }

    if (copyBtn) {
      copyBtn.addEventListener('click', () => this.copyForWhatsApp());
    }
  },

  loadFromStorage() {
    try {
      const saved = localStorage.getItem('mealsolver_shopping_list');
      this.items = saved ? JSON.parse(saved) : [];
    } catch (e) {
      this.items = [];
    }
    this.updateBadge();
  },

  saveToStorage() {
    localStorage.setItem('mealsolver_shopping_list', JSON.stringify(this.items));
    this.updateBadge();
  },

  updateBadge() {
    const badge = document.getElementById('cart-badge');
    if (badge) {
      badge.innerText = this.items.filter(i => !i.checked).length;
    }
  },

  open() {
    const backdrop = document.getElementById('cart-modal-backdrop');
    if (backdrop) backdrop.classList.add('show');
    this.render();
  },

  close() {
    const backdrop = document.getElementById('cart-modal-backdrop');
    if (backdrop) backdrop.classList.remove('show');
  },

  addMissing(recipeId, recipeTitle, missingList) {
    if (!missingList || missingList.length === 0) return;
    const details = missingList.map(item => typeof item === 'string' ? {name: item} : item);
    let addedCount = 0;

    details.forEach(detail => {
      const name = detail.name || '';
      if (!name) return;
      const unit = detail.unit || '';
      const existing = this.items.find(i =>
        i.name.toLowerCase() === name.toLowerCase() &&
        (i.unit || '') === unit &&
        i.recipeTitle === recipeTitle
      );
      if (existing && detail.quantity) {
        existing.quantity = Math.round((Number(existing.quantity || 0) + Number(detail.quantity)) * 100) / 100;
      } else if (!existing) {
        this.items.push({
          id: 'item_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
          name, recipeTitle, recipeId, quantity: detail.quantity || null, unit, checked: false
        });
        addedCount++;
      }
    });

    this.saveToStorage();
    this.render();
    App.showToast(`🛒 Added ${addedCount || 'updated'} ingredient quantities to your Shopping List!`);
  },

  addScaledIngredients(recipeId, recipeTitle, ingredients) {
    if (!ingredients || ingredients.length === 0) return;
    this.addMissing(recipeId, recipeTitle, ingredients.map(i => ({
      name: i.name, quantity: i.quantity, unit: i.unit
    })));
  },

  async addAllFromRecipe(recipeId, servings = null) {
    try {
      const recipe = await API.getRecipe(recipeId);
      if (!recipe) return;
      const target = servings || recipe.nutrition_per_serving?.servings || 2;
      const scaled = await API.scaleRecipe(recipeId, target);
      this.addScaledIngredients(recipe.id, recipe.title, scaled.scaled_ingredients || []);
    } catch (e) {
      console.error(e);
    }
  },

  toggleCheck(id) {
    const item = this.items.find(i => i.id === id);
    if (item) {
      item.checked = !item.checked;
      this.saveToStorage();
      this.render();
    }
  },

  removeItem(id) {
    this.items = this.items.filter(i => i.id !== id);
    this.saveToStorage();
    this.render();
  },

  render() {
    const container = document.getElementById('cart-items-container');
    if (!container) return;

    if (this.items.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 40px; color: var(--text-muted);">
          <div style="font-size: 36px; margin-bottom: 8px;">🛒</div>
          <h4>Your Shopping List is empty</h4>
          <p style="font-size: 13px; margin-top: 4px;">Tap the cart icon on recipe cards to add missing items!</p>
        </div>
      `;
      return;
    }

    // Group by recipe
    const groups = {};
    this.items.forEach(item => {
      const key = item.recipeTitle || 'General Grocery';
      if (!groups[key]) groups[key] = [];
      groups[key].push(item);
    });

    let html = '';
    for (const [recipeTitle, itemsList] of Object.entries(groups)) {
      html += `
        <div style="margin-bottom: 20px; background: var(--bg-input); border: 1px solid var(--border-light); border-radius: var(--radius-md); padding: 14px;">
          <div style="font-size: 13px; font-weight: 700; color: var(--accent-gold); margin-bottom: 10px; text-transform: uppercase;">
            🍲 For: ${recipeTitle}
          </div>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            ${itemsList.map(item => `
              <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 10px; background: rgba(255,255,255,0.03); border-radius: var(--radius-sm);">
                <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; user-select: none;">
                  <input type="checkbox" ${item.checked ? 'checked' : ''} onchange="ShoppingListModule.toggleCheck('${item.id}')" style="accent-color: var(--primary); width: 16px; height: 16px;">
                  <span style="font-size: 14px; ${item.checked ? 'text-decoration: line-through; color: var(--text-dim);' : 'color: #fff;'}">${item.name}${item.quantity ? ` <b style=\"color:var(--accent-gold);\">— ${item.quantity} ${item.unit || ''}</b>` : ''}</span>
                </label>
                <button class="chip-remove" onclick="ShoppingListModule.removeItem('${item.id}')" style="background: transparent; border: none; font-size: 16px;">&times;</button>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    container.innerHTML = html;
  },

  copyForWhatsApp() {
    if (this.items.length === 0) {
      App.showToast('Nothing to copy!');
      return;
    }

    let text = `🛒 *MealSolver Grocery List*\n`;
    text += `Generated for Indian Kitchen\n\n`;

    const groups = {};
    this.items.forEach(item => {
      const key = item.recipeTitle || 'General Items';
      if (!groups[key]) groups[key] = [];
      groups[key].push(item);
    });

    for (const [title, itemsList] of Object.entries(groups)) {
      text += `*${title}:*\n`;
      itemsList.forEach(i => {
        text += `  ${i.checked ? '✅' : '▫️'} ${i.name}${i.quantity ? ` — ${i.quantity} ${i.unit || ''}` : ''}\n`;
      });
      text += `\n`;
    }

    navigator.clipboard.writeText(text).then(() => {
      App.showToast('📋 Copied shopping list to clipboard for WhatsApp!');
    }).catch(() => {
      App.showToast('Failed to copy. Please allow clipboard permissions.');
    });
  }
};
