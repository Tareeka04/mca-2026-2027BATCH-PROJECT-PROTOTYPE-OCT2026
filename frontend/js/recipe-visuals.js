/* Recipe visuals: uses locally generated recipe-specific images when available. */
const RecipeVisuals = {
  card(recipe) {
    if (!recipe?.image_url) return '';
    const safeAlt = String(recipe.title || 'Recipe').replace(/"/g, '&quot;');
    return `<div class="recipe-card-image-wrap"><img class="recipe-card-image" src="${recipe.image_url}" alt="${safeAlt}" loading="lazy" onerror="this.closest('.recipe-card-image-wrap')?.remove()"></div>`;
  },
  hero(recipe) {
    if (!recipe?.image_url) return '';
    const safeAlt = String(recipe.title || 'Recipe').replace(/"/g, '&quot;');
    return `<div class="recipe-detail-hero-image-wrap"><img class="recipe-detail-hero-image" src="${recipe.image_url}" alt="${safeAlt}" onerror="this.closest('.recipe-detail-hero-image-wrap')?.remove()"></div>`;
  }
};
