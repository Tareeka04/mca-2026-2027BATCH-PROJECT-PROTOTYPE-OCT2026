/**
 * Fridge Scanner Module
 * Local image upload, HSV feature analysis, editable detected tags, and transfer to pantry
 */

const ScannerModule = {
  detectedIngredients: [],

  init() {
    this.bindEvents();
  },

  bindEvents() {
    const dropzone = document.getElementById('scanner-dropzone');
    const fileInput = document.getElementById('scanner-file-input');

    if (dropzone && fileInput) {
      dropzone.addEventListener('click', () => fileInput.click());

      dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
      });

      dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
      });

      dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
          this.handleImageFile(e.dataTransfer.files[0]);
        }
      });

      fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
          this.handleImageFile(e.target.files[0]);
        }
      });
    }

    const transferBtn = document.getElementById('transfer-to-pantry-btn');
    if (transferBtn) {
      transferBtn.addEventListener('click', () => this.transferToPantry());
    }
  },

  async handleImageFile(file) {
    if (!file.type.startsWith('image/')) {
      App.showToast('Please select a valid image file (PNG, JPG, JPEG)');
      return;
    }

    // Show image preview
    const previewImg = document.getElementById('scanner-preview-img');
    const previewContainer = document.getElementById('scanner-preview-box');
    if (previewImg && previewContainer) {
      const reader = new FileReader();
      reader.onload = (e) => {
        previewImg.src = e.target.result;
        previewContainer.style.display = 'block';
      };
      reader.readAsDataURL(file);
    }

    // Call detection API
    const resultsBox = document.getElementById('scanner-results-box');
    const tagsContainer = document.getElementById('scanner-tags-container');
    if (resultsBox) resultsBox.style.display = 'block';
    if (tagsContainer) {
      tagsContainer.innerHTML = `<div style="text-align: center; padding: 20px;"><div class="spinner"></div><p style="color: var(--text-muted); margin-top: 8px;">Analyzing fridge image colors & shapes locally...</p></div>`;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await API.detectFridge(formData);
      this.detectedIngredients = res.detections || [];
      this.renderDetectedTags();
    } catch (e) {
      if (tagsContainer) {
        tagsContainer.innerHTML = `<div style="color: var(--danger); padding: 10px;">Recognition failed. Please verify with manual tags below.</div>`;
      }
    }
  },

  loadSample(sampleType) {
    // Generate an instant synthetic demo canvas to test scanner without uploading
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 256;
    const ctx = canvas.getContext('2d');

    if (sampleType === 'veggies') {
      // Draw red tomato circle, green chillies, brown potato
      ctx.fillStyle = '#C0392B'; // Red tomato
      ctx.beginPath(); ctx.arc(70, 80, 50, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#27AE60'; // Green coriander
      ctx.fillRect(130, 40, 90, 80);
      ctx.fillStyle = '#D35400'; // Orange carrot
      ctx.fillRect(50, 150, 140, 50);
    } else if (sampleType === 'dairy') {
      ctx.fillStyle = '#FDFEFE'; // White paneer / curd
      ctx.fillRect(40, 40, 160, 160);
      ctx.fillStyle = '#F39C12'; // Yellow lemon
      ctx.beginPath(); ctx.arc(190, 190, 40, 0, Math.PI * 2); ctx.fill();
    } else {
      ctx.fillStyle = '#8E44AD'; // Purple brinjal
      ctx.beginPath(); ctx.arc(90, 100, 60, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#D4AC0D'; // Potato
      ctx.beginPath(); ctx.arc(180, 160, 50, 0, Math.PI * 2); ctx.fill();
    }

    canvas.toBlob((blob) => {
      const file = new File([blob], `${sampleType}_sample.png`, { type: 'image/png' });
      this.handleImageFile(file);
    });
  },

  renderDetectedTags() {
    const container = document.getElementById('scanner-tags-container');
    if (!container) return;

    if (this.detectedIngredients.length === 0) {
      container.innerHTML = `<div style="color: var(--text-muted);">No distinct ingredients detected. You can add items manually below!</div>`;
      return;
    }

    let html = '';
    this.detectedIngredients.forEach((item, idx) => {
      const confPct = Math.round((item.confidence || 0.8) * 100);
      html += `
        <span class="chip selected" style="border-color: #8B5CF6; background: rgba(139, 92, 246, 0.2);">
          <span>🔍 ${item.name} (${confPct}%)</span>
          <span class="chip-remove" onclick="ScannerModule.removeDetected(${idx})">&times;</span>
        </span>
      `;
    });

    container.innerHTML = html;
  },

  removeDetected(index) {
    this.detectedIngredients.splice(index, 1);
    this.renderDetectedTags();
  },

  transferToPantry() {
    if (this.detectedIngredients.length === 0) {
      App.showToast('No detected ingredients to transfer!');
      return;
    }

    let addedCount = 0;
    this.detectedIngredients.forEach(item => {
      const canon = item.canonical || item.name.split('/')[0].trim();
      const formatted = canon.charAt(0).toUpperCase() + canon.slice(1);
      PantryModule.selectedIngredients.add(formatted);
      addedCount++;
    });

    PantryModule.renderSelectedPills();
    PantryModule.updateQuickChips();
    
    // Switch to Pantry Tab
    App.switchTab('pantry');
    PantryModule.solve();

    App.showToast(`✨ Added ${addedCount} detected items to your Pantry Solver!`);
  }
};
