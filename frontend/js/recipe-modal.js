/**
 * Recipe Detail & Interactive Cooking Mode Modal
 * Features:
 * 1. Dynamic Servings Scaler (recalculates ingredient quantities & total nutrition)
 * 2. Step-by-Step Cooking Mode with Countdown Timers
 * 3. Voice Narration / Read Aloud using Web Speech API
 */

const RecipeModal = {
  currentRecipe: null,
  currentServings: 2,
  activeStepIndex: 0,
  timerInterval: null,
  timerSecondsLeft: 0,

  init() {
    this.bindEvents();
  },

  bindEvents() {
    const modalBackdrop = document.getElementById('recipe-modal-backdrop');
    const closeBtn = document.getElementById('recipe-modal-close');

    if (closeBtn && modalBackdrop) {
      closeBtn.addEventListener('click', () => this.close());
      modalBackdrop.addEventListener('click', (e) => {
        if (e.target === modalBackdrop) this.close();
      });
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modalBackdrop?.classList.contains('show')) {
        this.close();
      }
    });
  },

  async open(recipeId) {
    const backdrop = document.getElementById('recipe-modal-backdrop');
    const modalBody = document.getElementById('recipe-modal-body');
    if (!backdrop || !modalBody) return;

    backdrop.classList.add('show');
    modalBody.innerHTML = `<div style="text-align: center; padding: 60px;"><div class="spinner"></div><p style="color: var(--text-muted); margin-top: 14px;">Loading authentic recipe secrets...</p></div>`;

    try {
      this.currentRecipe = await API.getRecipe(recipeId);
      const householdCount = typeof HouseholdConstraints !== 'undefined' ? HouseholdConstraints.getMembers().length : 0;
      this.currentServings = Math.min(24, Math.max(1, householdCount || this.currentRecipe.nutrition_per_serving?.servings || 2));
      this.render();
    } catch (e) {
      modalBody.innerHTML = `<div style="color: var(--danger); padding: 40px; text-align: center;">Failed to load recipe details.</div>`;
    }
  },

  close() {
    const backdrop = document.getElementById('recipe-modal-backdrop');
    if (backdrop) backdrop.classList.remove('show');
    this.stopTimer();
    window.speechSynthesis?.cancel();
  },

  async updateServings(delta, force = false) {
    const newServings = Math.max(1, Math.min(24, this.currentServings + delta));
    if (newServings === this.currentServings && !force) return;

    this.currentServings = newServings;
    try {
      const scaledData = await API.scaleRecipe(this.currentRecipe.id, this.currentServings);
      this.renderIngredientsAndNutrition(scaledData);
    } catch (e) {
      console.error(e);
    }
  },

  render() {
    const modalBody = document.getElementById('recipe-modal-body');
    const modalTitle = document.getElementById('recipe-modal-title');
    const r = this.currentRecipe;
    if (!modalBody || !r) return;

    if (modalTitle) {
      modalTitle.innerText = r.title;
    }

    const householdFit = typeof HouseholdConstraints !== 'undefined' ? HouseholdConstraints.explain(r) : { ok: true, reasons: [], conflicts: [], memberChecks: [] };
    const memberRows = (householdFit.memberChecks || []).map(m => `
      <div class="household-member-check-row">
        <div><strong>${m.name}</strong><span>${m.role || ''}</span></div>
        <div class="household-member-checks">${m.checks.map(c => `<span class="constraint-chip ${c.ok ? 'ok' : 'bad'}">${c.ok ? '✓' : '✗'} ${c.label}${c.detail ? `: ${c.detail}` : ''}</span>`).join('')}</div>
      </div>`).join('');

    modalBody.innerHTML = `
      <div class="recipe-detail-hero">
        ${RecipeVisuals.hero(r)}
<div class="recipe-detail-hero-copy">
          <div class="recipe-detail-kicker">${r.regional_cuisine} • ${r.course || 'Indian recipe'}</div>
          <h1>${r.title}</h1>
          <p>${r.summary || ''}</p>
        </div>
      </div>

      <div class="household-recipe-check ${householdFit.ok ? 'compatible' : 'conflict'}">
        <div style="width:100%;"><strong>${householdFit.ok ? '✓ Fits your saved household constraints' : '⚠ Household constraint conflict'}</strong>
        <div class="household-check-detail">${(householdFit.ok ? householdFit.reasons : householdFit.conflicts).map(x => `<span>• ${x}</span>`).join('')}</div>
        ${memberRows ? `<div class="household-member-checks-panel"><div class="household-member-check-title">How each member is satisfied</div>${memberRows}</div>` : ''}</div>
        <button class="btn-secondary" onclick="App.switchTab('household'); RecipeModal.close();">Edit household</button>
      </div>

      <!-- Header Meta -->
      <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 18px;">
        <span class="cuisine-badge" style="font-size: 13px; padding: 4px 12px;">🚩 ${r.regional_cuisine}</span>
        <span class="ready-badge ready" style="font-size: 13px; padding: 4px 12px;">🌱 ${r.diet}</span>
        <span class="mini-tag" style="background: rgba(255,255,255,0.08); font-size: 13px; padding: 4px 12px;">⏱️ Prep: ${r.prep_time_mins}m | Cook: ${r.cook_time_mins}m</span>
        <span class="mini-tag" style="background: rgba(255,255,255,0.08); font-size: 13px; padding: 4px 12px;">🔥 ${r.difficulty}</span>
      </div>

      <!-- Servings Scaler Widget -->
      <div class="servings-widget">
        <div>
          <div style="font-weight: 700; font-size: 15px; color: #fff;">Adjust Servings</div>
          <div style="font-size: 12px; color: var(--text-muted);">Ingredient quantities & calories scale proportionally</div>
        </div>
        <div class="servings-controls">
          <button class="btn-servings" onclick="RecipeModal.updateServings(-1)">-</button>
          <span class="servings-count" id="modal-servings-count">${this.currentServings}</span>
          <button class="btn-servings" onclick="RecipeModal.updateServings(1)">+</button>
          <span style="font-size: 13px; color: var(--text-muted); margin-left: 4px;">servings</span>
        </div>
      </div>

      <!-- Scaled Ingredients Container -->
      <div id="modal-ingredients-section" style="margin-bottom: 28px;">
        <!-- Filled by renderIngredientsAndNutrition -->
      </div>

      <!-- Equipment Needed -->
      ${r.equipment && r.equipment.length > 0 ? `
        <div style="margin-bottom: 28px; background: rgba(255,255,255,0.03); border: 1px solid var(--border-light); padding: 16px; border-radius: var(--radius-md);">
          <div style="font-size: 13px; font-weight: 700; color: var(--accent-gold); text-transform: uppercase; margin-bottom: 8px;">🔪 Equipment Required</div>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            ${r.equipment.map(eq => `<span class="mini-tag" style="background: rgba(255,255,255,0.08); color: #fff;">${eq}</span>`).join('')}
          </div>
        </div>
      ` : ''}

      <!-- Interactive Step-by-Step Cooking Mode Button -->
      <div style="text-align: center; margin-bottom: 24px;">
        <button class="btn-primary" style="padding: 14px 28px; font-size: 16px;" onclick="RecipeModal.startCookingMode()">
          🚀 Launch Interactive Cooking Mode (with Voice & Timers)
        </button>
      </div>

      <!-- Step by step listing -->
      <div>
        <div style="display:flex;justify-content:space-between;align-items:end;gap:12px;margin-bottom:16px;flex-wrap:wrap;">
          <div><h3 style="font-size: 22px; margin-bottom: 4px; color: #fff;">Detailed Preparation & Cooking</h3><p style="color:var(--text-muted);font-size:13px;">${r.steps.length} recipe-specific steps • follow the timing and visual cues for this dish</p></div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 16px;">
          ${r.steps.map(s => `
            <div style="background: var(--bg-input); border: 1px solid var(--border-light); border-radius: var(--radius-md); padding: 18px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-weight: 800; color: var(--primary); font-size: 15px;">Step ${s.step_number}: ${s.title}</span>
                ${s.duration_mins > 0 ? `<span style="font-size: 12px; color: var(--text-muted);">⏱️ ~${s.duration_mins} mins</span>` : ''}
              </div>
              <p style="color: var(--text-main); font-size: 14px; line-height: 1.6;">${s.instruction}</p>
              ${s.tip ? `
                <div style="margin-top: 8px; font-size: 12px; color: #A7F3D0; background: rgba(16, 185, 129, 0.1); padding: 6px 10px; border-radius: 6px;">
                  💡 <b>Pro Tip:</b> ${s.tip}
                </div>
              ` : ''}
            </div>
          `).join('')}
        </div>
      </div>
    `;

    // Trigger the initial ingredients render even when the serving count has not changed.
    // Previously updateServings(0) returned early, leaving the ingredient panel empty.
    this.updateServings(0, true);
  },

  renderIngredientsAndNutrition(data) {
    const container = document.getElementById('modal-ingredients-section');
    const servingsCount = document.getElementById('modal-servings-count');
    if (!container) return;

    if (servingsCount) servingsCount.innerText = data.target_servings;

    const ingredients = data.scaled_ingredients || [];
    const nut = data.total_nutrition_estimate || {};

    let html = `
      <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
        <!-- Ingredients List -->
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <h4 style="font-size: 17px; color: #fff;">Ingredients (${ingredients.length})</h4>
            <button class="btn-secondary" style="font-size: 12px; padding: 4px 10px;" onclick="ShoppingListModule.addAllFromRecipe('${this.currentRecipe.id}', RecipeModal.currentServings)">
              + Add All to Shopping List
            </button>
          </div>
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 8px;">
            ${ingredients.map(ing => `
              <li style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.03); border: 1px solid var(--border-light); padding: 8px 12px; border-radius: var(--radius-sm); font-size: 14px;">
                <span>
                  <b style="color: #FFD8A8;">${ing.display_quantity} ${ing.unit}</b>
                  <span style="color: #fff; margin-left: 6px;">${ing.name}</span>
                  ${ing.is_optional ? `<span style="font-size: 10px; color: var(--text-dim); margin-left: 4px;">(optional)</span>` : ''}
                </span>
                ${ing.substitutes && ing.substitutes.length > 0 ? `
                  <span style="font-size: 11px; color: var(--accent-turmeric); margin-left: 8px;" title="Substitute: ${ing.substitutes.join(', ')}">💡 Substitute: ${ing.substitutes.join(', ')}</span>
                ` : ''}
              </li>
            `).join('')}
          </ul>
        </div>

        <!-- Scaled Nutrition Panel -->
        <div style="background: var(--bg-input); border: 1px solid var(--border-light); border-radius: var(--radius-md); padding: 16px;">
          <h4 style="font-size: 15px; color: var(--accent-gold); margin-bottom: 12px; text-transform: uppercase;">
            📊 Nutrition (${data.target_servings} Servings)
          </h4>
          <div style="display: flex; flex-direction: column; gap: 10px; font-size: 14px;">
            <div style="display: flex; justify-content: space-between;">
              <span style="color: var(--text-muted);">Calories:</span>
              <span style="font-weight: 800; color: #fff;">${nut.total_calories || '--'} kcal</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span style="color: var(--text-muted);">Protein:</span>
              <span style="font-weight: 700; color: #4ADE80;">${nut.total_protein_g || '--'} g</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span style="color: var(--text-muted);">Carbs:</span>
              <span style="font-weight: 700; color: #60A5FA;">${nut.total_carbs_g || '--'} g</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span style="color: var(--text-muted);">Fats:</span>
              <span style="font-weight: 700; color: #F87171;">${nut.total_fat_g || '--'} g</span>
            </div>
          </div>
        </div>
      </div>
    `;

    container.innerHTML = html;
  },

  // Interactive Cooking Mode
  startCookingMode() {
    this.activeStepIndex = 0;
    this.renderCookingStep();
  },

  renderCookingStep() {
    const modalBody = document.getElementById('recipe-modal-body');
    const r = this.currentRecipe;
    if (!modalBody || !r) return;

    const step = r.steps[this.activeStepIndex];
    const totalSteps = r.steps.length;

    modalBody.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <button class="btn-secondary" onclick="RecipeModal.render()">← Exit Cooking Mode</button>
        <div style="font-weight: 800; color: var(--primary); font-size: 16px;">
          Step ${this.activeStepIndex + 1} of ${totalSteps}
        </div>
        <button class="btn-secondary" onclick="RecipeModal.readAloud()">🔊 Read Aloud</button>
      </div>

      <div class="cooking-step-card">
        <h2 style="font-size: 24px; color: #fff; margin-bottom: 12px;">${step.title}</h2>
        <p style="font-size: 18px; line-height: 1.7; color: var(--text-main); margin-bottom: 20px;">
          ${step.instruction}
        </p>
        
        ${step.tip ? `
          <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: var(--radius-sm); padding: 12px 16px; color: #A7F3D0; font-size: 14px;">
            💡 <b>Chef Tip:</b> ${step.tip}
          </div>
        ` : ''}

        ${step.duration_mins > 0 ? `
          <div class="timer-box">
            <div>
              <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: var(--text-muted);">Step Timer</div>
              <div class="timer-display" id="cooking-timer-display">${String(step.duration_mins).padStart(2, '0')}:00</div>
            </div>
            <div style="display: flex; gap: 8px;">
              <button class="btn-primary" id="timer-toggle-btn" onclick="RecipeModal.toggleTimer(${step.duration_mins * 60})">▶ Start Timer</button>
              <button class="btn-secondary" onclick="RecipeModal.resetTimer(${step.duration_mins * 60})">↺ Reset</button>
            </div>
          </div>
        ` : ''}
      </div>

      <!-- Navigation buttons -->
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <button class="btn-secondary" ${this.activeStepIndex === 0 ? 'disabled style="opacity: 0.4;"' : ''} onclick="RecipeModal.prevStep()">
          ← Previous Step
        </button>

        ${this.activeStepIndex < totalSteps - 1 ? `
          <button class="btn-primary" onclick="RecipeModal.nextStep()">Next Step →</button>
        ` : `
          <button class="btn-primary" style="background: linear-gradient(135deg, #10B981, #059669);" onclick="RecipeModal.finishCooking()">
            🎉 Finish & Serve!
          </button>
        `}
      </div>
    `;

    // Automatically speak step instruction
    this.readAloud();
  },

  prevStep() {
    if (this.activeStepIndex > 0) {
      this.activeStepIndex--;
      this.stopTimer();
      this.renderCookingStep();
    }
  },

  nextStep() {
    if (this.activeStepIndex < this.currentRecipe.steps.length - 1) {
      this.activeStepIndex++;
      this.stopTimer();
      this.renderCookingStep();
    }
  },

  finishCooking() {
    this.stopTimer();
    App.showToast(`🎉 Congratulations! Enjoy your delicious ${this.currentRecipe.title}!`);
    this.render();
  },

  // Speech Synthesis
  readAloud() {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    const step = this.currentRecipe.steps[this.activeStepIndex];
    const textToSpeak = `Step ${step.step_number}. ${step.title}. ${step.instruction}. ${step.tip ? 'Pro tip: ' + step.tip : ''}`;

    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  },

  // Countdown Timer
  toggleTimer(totalSecs) {
    if (this.timerInterval) {
      this.stopTimer();
      const btn = document.getElementById('timer-toggle-btn');
      if (btn) btn.innerText = '▶ Resume Timer';
    } else {
      if (this.timerSecondsLeft <= 0) {
        this.timerSecondsLeft = totalSecs;
      }
      this.startTimer();
      const btn = document.getElementById('timer-toggle-btn');
      if (btn) btn.innerText = '⏸ Pause Timer';
    }
  },

  startTimer() {
    this.timerInterval = setInterval(() => {
      this.timerSecondsLeft--;
      this.updateTimerDisplay();

      if (this.timerSecondsLeft <= 0) {
        this.stopTimer();
        App.showToast('⏰ Timer finished for this step!');
        // Play beep chime
        try {
          const ctx = new (window.AudioContext || window.webkitAudioContext)();
          const osc = ctx.createOscillator();
          osc.connect(ctx.destination);
          osc.frequency.value = 800;
          osc.start();
          setTimeout(() => osc.stop(), 500);
        } catch (e) {}
      }
    }, 1000);
  },

  stopTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  },

  resetTimer(totalSecs) {
    this.stopTimer();
    this.timerSecondsLeft = totalSecs;
    this.updateTimerDisplay();
    const btn = document.getElementById('timer-toggle-btn');
    if (btn) btn.innerText = '▶ Start Timer';
  },

  updateTimerDisplay() {
    const el = document.getElementById('cooking-timer-display');
    if (!el) return;
    const mins = Math.floor(this.timerSecondsLeft / 60);
    const secs = this.timerSecondsLeft % 60;
    el.innerText = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }
};
