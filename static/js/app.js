// NutriChef AI - Frontend Engine
let currentAnalysisRecipe = null;
let savedRecipes = [];
let selectedForCompare = new Set();
let macroDonutChartInstance = null;
let compareBarChartInstance = null;
let compareCaloriesChartInstance = null;
let currentInputMode = 'text'; // 'text' | 'image' | 'video'
let selectedImageFile = null;
let currentCategoryFilter = 'all';

const CATEGORY_META = {
    'desayuno': { label: 'Desayuno', icon: '🌅', color: 'bg-amber-100 text-amber-800 border-amber-200' },
    'comida': { label: 'Comida', icon: '🍽️', color: 'bg-emerald-100 text-emerald-800 border-emerald-200' },
    'merienda': { label: 'Merienda', icon: '☕', color: 'bg-orange-100 text-orange-800 border-orange-200' },
    'cena': { label: 'Cena', icon: '🌙', color: 'bg-indigo-100 text-indigo-800 border-indigo-200' },
    'postre': { label: 'Postre', icon: '🍰', color: 'bg-pink-100 text-pink-800 border-pink-200' },
    'merienda-postre': { label: 'Merienda / Postre', icon: '☕', color: 'bg-purple-100 text-purple-800 border-purple-200' }
};

// Custom Foods State
let savedCustomFoods = [];
let currentFoodCategoryFilter = 'all';

const FOOD_CATEGORY_META = {
    'proteina': { label: 'Proteína', icon: '🥩', color: 'bg-blue-50 text-blue-700 border-blue-200' },
    'carbohidrato': { label: 'Carbohidrato', icon: '🍚', color: 'bg-amber-50 text-amber-700 border-amber-200' },
    'verdura': { label: 'Verdura / Fruta', icon: '🥦', color: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
    'lacteo': { label: 'Lácteo', icon: '🥛', color: 'bg-cyan-50 text-cyan-700 border-cyan-200' },
    'grasa': { label: 'Grasa / Aceite', icon: '🥑', color: 'bg-rose-50 text-rose-700 border-rose-200' },
    'despensa': { label: 'Despensa', icon: '🥫', color: 'bg-slate-100 text-slate-700 border-slate-200' }
};

function safeCreateIcons() {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
        try {
            window.lucide.createIcons();
        } catch (e) {
            console.warn('Lucide icons warning:', e);
        }
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    safeCreateIcons();
    checkApiConfig();
    loadRecipes();
    loadCustomFoods();
});

// ==========================================
// TABS & NAVIGATION
// ==========================================
function switchTab(tabId) {
    const tabs = ['analyzer', 'pantry', 'foods', 'recipes', 'comparator', 'suggester'];
    tabs.forEach(t => {
        const section = document.getElementById(`section-${t}`);
        const navBtn = document.getElementById(`tab-nav-${t}`);
        const mobileNavBtn = document.getElementById(`tab-nav-mobile-${t}`);
        
        if (t === tabId) {
            if (section) section.classList.remove('hidden');
            if (navBtn) {
                navBtn.classList.add('text-emerald-700', 'bg-emerald-50');
                navBtn.classList.remove('text-slate-600', 'hover:bg-slate-100');
            }
            if (mobileNavBtn) {
                mobileNavBtn.classList.add('bg-emerald-50', 'text-emerald-700');
                mobileNavBtn.classList.remove('text-slate-600');
            }
        } else {
            if (section) section.classList.add('hidden');
            if (navBtn) {
                navBtn.classList.remove('text-emerald-700', 'bg-emerald-50');
                navBtn.classList.add('text-slate-600', 'hover:bg-slate-100');
            }
            if (mobileNavBtn) {
                mobileNavBtn.classList.remove('bg-emerald-50', 'text-emerald-700');
                mobileNavBtn.classList.add('text-slate-600');
            }
        }
    });

    if (tabId === 'comparator') {
        renderCompareSelectionGrid();
    } else if (tabId === 'recipes') {
        renderRecipesGrid();
    } else if (tabId === 'foods') {
        renderCustomFoodsGrid();
    } else if (tabId === 'pantry') {
        loadPantryTab();
    }
    safeCreateIcons();
}

function setAnalysisInputMode(mode) {
    currentInputMode = mode;
    const modes = ['text', 'image', 'video'];
    modes.forEach(m => {
        const container = document.getElementById(`input-container-${m}`);
        const btn = document.getElementById(`mode-btn-${m}`);
        if (m === mode) {
            container.classList.remove('hidden');
            btn.classList.add('bg-white', 'text-emerald-700', 'shadow-sm', 'border', 'border-slate-200/60');
            btn.classList.remove('text-slate-600');
        } else {
            container.classList.add('hidden');
            btn.classList.remove('bg-white', 'text-emerald-700', 'shadow-sm', 'border', 'border-slate-200/60');
            btn.classList.add('text-slate-600');
        }
    });
    safeCreateIcons();
}

// ==========================================
// IMAGE UPLOAD & DRAG/DROP
// ==========================================
function handleImageSelected(event) {
    const file = event.target.files[0];
    if (file) {
        selectedImageFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('image-placeholder-view').classList.add('hidden');
            const previewView = document.getElementById('image-preview-view');
            previewView.classList.remove('hidden');
            document.getElementById('image-preview-element').src = e.target.result;
            document.getElementById('image-filename').textContent = `Foto seleccionada: ${file.name} (${(file.size / 1024).toFixed(0)} KB)`;
        };
        reader.readAsDataURL(file);
    }
}

function clearSelectedImage(event) {
    event.stopPropagation();
    selectedImageFile = null;
    document.getElementById('image-file-input').value = '';
    document.getElementById('image-placeholder-view').classList.remove('hidden');
    document.getElementById('image-preview-view').classList.add('hidden');
}

async function extractResponseError(resp, defaultMsg) {
    try {
        const err = await resp.json();
        return err.detail || defaultMsg;
    } catch (_) {
        try {
            const text = await resp.text();
            return text || defaultMsg;
        } catch (__) {
            return defaultMsg;
        }
    }
}

// Captura de fotograma representativo del vídeo para usarlo como foto del plato terminado
async function captureVideoFrame(videoFile) {
    return new Promise((resolve) => {
        try {
            const video = document.createElement('video');
            video.preload = 'metadata';
            video.muted = true;
            video.playsInline = true;
            const url = URL.createObjectURL(videoFile);
            video.src = url;

            const cleanUp = () => {
                try { URL.revokeObjectURL(url); } catch (_) {}
                try { video.remove(); } catch (_) {}
            };

            video.onloadedmetadata = () => {
                video.currentTime = Math.min(1.5, (video.duration || 1) / 2);
            };

            video.onseeked = () => {
                try {
                    const canvas = document.createElement('canvas');
                    canvas.width = Math.min(video.videoWidth || 640, 1280);
                    canvas.height = Math.min(video.videoHeight || 360, 720);
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                    canvas.toBlob((blob) => {
                        cleanUp();
                        resolve(blob);
                    }, 'image/jpeg', 0.85);
                } catch (e) {
                    cleanUp();
                    resolve(null);
                }
            };

            video.onerror = () => {
                cleanUp();
                resolve(null);
            };

            setTimeout(() => {
                cleanUp();
                resolve(null);
            }, 2500);
        } catch (_) {
            resolve(null);
        }
    });
}

// ==========================================
// ANALYSIS EXECUTION
// ==========================================
async function executeAnalysis() {
    const loadingElem = document.getElementById('analysis-loading');
    const resultsElem = document.getElementById('analysis-results');
    const stepTitle = document.getElementById('loading-step-title');
    const stepSubtitle = document.getElementById('loading-step-subtitle');

    loadingElem.classList.remove('hidden');
    resultsElem.classList.add('hidden');

    try {
        let recipeData = null;

        if (currentInputMode === 'text') {
            const text = document.getElementById('recipe-text-input').value.trim();
            if (!text) {
                alert('Por favor, escribe o pega los ingredientes de la receta.');
                loadingElem.classList.add('hidden');
                return;
            }
            stepTitle.textContent = 'Analizando texto e ingredientes...';
            stepSubtitle.textContent = 'Consultando modelo bromatológico Gemini 3.8 Flash...';
            
            const resp = await fetch('/api/analyze/text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            if (!resp.ok) {
                throw new Error(await extractResponseError(resp, 'Error analizando texto'));
            }
            recipeData = await resp.json();

        } else if (currentInputMode === 'image') {
            if (!selectedImageFile) {
                alert('Por favor, selecciona o arrastra una foto para analizar.');
                loadingElem.classList.add('hidden');
                return;
            }
            stepTitle.textContent = 'Analizando imagen mediante visión artificial...';
            stepSubtitle.textContent = 'Detectando alimentos visibles, estimando cantidades y raciones...';

            const formData = new FormData();
            formData.append('file', selectedImageFile);

            const resp = await fetch('/api/analyze/image', {
                method: 'POST',
                body: formData
            });
            if (!resp.ok) {
                throw new Error(await extractResponseError(resp, 'Error analizando imagen'));
            }
            recipeData = await resp.json();

        } else if (currentInputMode === 'video') {
            const videoFileInput = document.getElementById('video-file-input');
            const socialUrl = document.getElementById('social-url-input').value.trim();

            if (videoFileInput.files.length > 0) {
                // Archivo de vídeo subido
                const file = videoFileInput.files[0];
                stepTitle.textContent = 'Procesando archivo de vídeo...';
                stepSubtitle.textContent = 'Extrayendo fotograma del plato y analizando con Gemini IA...';

                const formData = new FormData();
                formData.append('file', file);

                try {
                    const frameBlob = await captureVideoFrame(file);
                    if (frameBlob) {
                        formData.append('thumbnail', frameBlob, 'frame.jpg');
                    }
                } catch (_) {}

                const resp = await fetch('/api/analyze/video', {
                    method: 'POST',
                    body: formData
                });
                if (!resp.ok) {
                    throw new Error(await extractResponseError(resp, 'Error analizando vídeo'));
                }
                recipeData = await resp.json();

            } else if (socialUrl) {
                // Enlace de red social
                stepTitle.textContent = 'Extrayendo contenido de red social...';
                stepSubtitle.textContent = 'Descargando metadatos y contenido con yt-dlp...';

                const resp = await fetch('/api/analyze/url', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: socialUrl })
                });
                if (!resp.ok) {
                    throw new Error(await extractResponseError(resp, 'Error procesando enlace de red social'));
                }
                recipeData = await resp.json();
                if (socialUrl && !recipeData.video_url) {
                    recipeData.video_url = socialUrl;
                }

            } else {
                alert('Por favor, pega un enlace de TikTok/Instagram/YouTube o sube un archivo de vídeo.');
                loadingElem.classList.add('hidden');
                return;
            }
        }

        currentAnalysisRecipe = recipeData;
        renderAnalysisResults(recipeData);

    } catch (error) {
        alert(`Ocurrió un error: ${error.message}`);
    } finally {
        loadingElem.classList.add('hidden');
    }
}

// ==========================================
// SERVING WEIGHT ESTIMATION
// ==========================================
function calculateEstimatedServingWeight(recipe) {
    if (!recipe) return { rawTotalG: 0, cookedTotalG: 0, perServingG: 0 };
    const servings = Math.max(1, parseInt(recipe.servings) || 1);

    if (recipe.serving_weight_g && recipe.serving_weight_g > 0) {
        const perServing = Math.round(recipe.serving_weight_g);
        return {
            rawTotalG: Math.round(perServing * servings * 1.1),
            cookedTotalG: Math.round(perServing * servings),
            perServingG: perServing
        };
    }

    const ingredients = recipe.ingredients || [];
    let totalRawG = 0;

    for (const ing of ingredients) {
        const amt = (ing.amount || '').toLowerCase();
        const name = (ing.name || '').toLowerCase();
        const text = `${amt} ${name}`;

        let g = 0;
        const gMatch = amt.match(/(\d+(?:[.,]\d+)?)\s*(?:g|gr|gramo|gramos)\b/);
        const kgMatch = amt.match(/(\d+(?:[.,]\d+)?)\s*(?:kg|kilo|kilos)\b/);
        const mlMatch = amt.match(/(\d+(?:[.,]\d+)?)\s*(?:ml|mililitro|mililitros)\b/);
        const clMatch = amt.match(/(\d+(?:[.,]\d+)?)\s*(?:cl)\b/);
        const lMatch = amt.match(/(\d+(?:[.,]\d+)?)\s*(?:l|litro|litros)\b/);
        const eggMatch = text.match(/(\d+)?\s*(?:huevo|huevos)\b/);
        const tbspMatch = amt.match(/(\d+(?:[.,]\d+)?)\s*(?:cucharada|cda|cdas|cucharadas)\b/);
        const tspMatch = amt.match(/(\d+(?:[.,]\d+)?)\s*(?:cucharadita|cdita|cditas|cucharaditas)\b/);

        if (gMatch) {
            g = parseFloat(gMatch[1].replace(',', '.'));
        } else if (kgMatch) {
            g = parseFloat(kgMatch[1].replace(',', '.')) * 1000;
        } else if (mlMatch) {
            g = parseFloat(mlMatch[1].replace(',', '.'));
        } else if (clMatch) {
            g = parseFloat(clMatch[1].replace(',', '.')) * 10;
        } else if (lMatch) {
            g = parseFloat(lMatch[1].replace(',', '.')) * 1000;
        } else if (eggMatch) {
            const count = eggMatch[1] ? parseInt(eggMatch[1]) : 1;
            g = count * 60;
        } else if (tbspMatch) {
            g = parseFloat(tbspMatch[1].replace(',', '.')) * 15;
        } else if (tspMatch) {
            g = parseFloat(tspMatch[1].replace(',', '.')) * 5;
        } else {
            const numMatch = amt.match(/(\d+(?:[.,]\d+)?|\bmedio\b|\bmedia\b|\bun\b|\buna\b)/);
            let qty = 1;
            if (numMatch) {
                const val = numMatch[1];
                if (val === 'medio' || val === 'media') qty = 0.5;
                else if (val === 'un' || val === 'una') qty = 1;
                else qty = parseFloat(val.replace(',', '.')) || 1;
            }
            if (text.includes('calabacín') || text.includes('calabacin')) g = qty * 250;
            else if (text.includes('cebolla')) g = qty * 150;
            else if (text.includes('patata') || text.includes('papa')) g = qty * 180;
            else if (text.includes('tomate')) g = qty * 150;
            else if (text.includes('zanahoria')) g = qty * 80;
            else if (text.includes('aguacate')) g = qty * 160;
            else if (text.includes('diente') || text.includes('ajo')) g = qty * 5;
            else if (text.includes('manzana') || text.includes('pera') || text.includes('plátano') || text.includes('platano')) g = qty * 150;
            else if (text.includes('pechuga')) g = qty * 150;
            else if (text.includes('lata')) g = qty * 80;
            else if (text.includes('pizca')) g = 1;
        }
        totalRawG += g;
    }

    let cookedTotalG = 0;
    if (totalRawG > 30) {
        cookedTotalG = Math.round(totalRawG * 0.88);
    } else if (recipe.total_nutrients && recipe.total_nutrients.calories) {
        cookedTotalG = Math.round(recipe.total_nutrients.calories / 1.4);
    } else if (recipe.per_serving && recipe.per_serving.calories) {
        cookedTotalG = Math.round((recipe.per_serving.calories * servings) / 1.4);
    } else {
        cookedTotalG = servings * 250;
    }

    const perServingG = Math.max(20, Math.round(cookedTotalG / servings));
    return {
        rawTotalG: Math.round(totalRawG || cookedTotalG * 1.12),
        cookedTotalG,
        perServingG
    };
}

// ==========================================
// RENDER ANALYSIS RESULTS
// ==========================================
function renderAnalysisResults(recipe) {
    const resultsElem = document.getElementById('analysis-results');
    resultsElem.classList.remove('hidden');

    // Control del aviso de Modo Demostración
    const isDemo = (recipe.dietary_tags || []).some(t => t.includes('Modo Demostración')) || (recipe.title || '').includes('Modo Demo');
    const demoBanner = document.getElementById('demo-warning-banner');
    if (demoBanner) {
        if (isDemo) {
            demoBanner.classList.remove('hidden');
        } else {
            demoBanner.classList.add('hidden');
        }
    }

    // Header
    document.getElementById('res-recipe-title').textContent = recipe.title || 'Receta Analizada';
    document.getElementById('res-recipe-description').textContent = recipe.description || '';
    const weightEst = calculateEstimatedServingWeight(recipe);
    const servingsText = `${recipe.servings || 1} ${recipe.servings > 1 ? 'raciones' : 'ración'}`;
    document.getElementById('res-servings-badge').textContent = weightEst.perServingG > 0
        ? `${servingsText} (~${weightEst.perServingG}g / ración)`
        : servingsText;
    const prep = recipe.prep_time_minutes || 0;
    const cook = recipe.cook_time_minutes || 0;
    document.getElementById('res-time-badge').textContent = `⏱️ ${(prep + cook) || 20} min`;

    // Foto / Imagen del plato
    const imgWrapper = document.getElementById('res-image-wrapper');
    const imgElem = document.getElementById('res-recipe-image');
    if (imgWrapper && imgElem) {
        if (recipe.image_url) {
            imgElem.src = recipe.image_url;
            imgWrapper.classList.remove('hidden');
        } else {
            imgWrapper.classList.add('hidden');
        }
    }
    
    const sourceTypes = {
        'text': 'Texto Escrito',
        'image': 'Foto / Imagen',
        'video_file': 'Vídeo Subido',
        'social_url': 'Red Social',
        'ai_generated': 'Sugerencia IA'
    };
    document.getElementById('res-source-badge').textContent = sourceTypes[recipe.source_type] || 'Analizada';

    // Category badge
    const catKey = (recipe.category || 'comida').toLowerCase();
    const catMeta = CATEGORY_META[catKey] || CATEGORY_META['comida'];
    const catBadge = document.getElementById('res-category-badge');
    if (catBadge) {
        catBadge.textContent = `${catMeta.icon} ${catMeta.label}`;
        catBadge.className = `px-2.5 py-0.5 rounded-full text-xs font-bold border ${catMeta.color}`;
    }

    // Video original link
    const videoLink = document.getElementById('res-video-link');
    if (videoLink) {
        const vUrl = recipe.video_url || (recipe.source_reference && recipe.source_reference.startsWith('http') ? recipe.source_reference : null);
        if (vUrl) {
            videoLink.href = vUrl;
            videoLink.classList.remove('hidden');
        } else {
            videoLink.classList.add('hidden');
        }
    }

    // Nutri-Score
    const ns = (recipe.nutri_score || 'B').toUpperCase();
    const nsElem = document.getElementById('res-nutriscore');
    nsElem.textContent = ns;
    nsElem.className = `nutriscore-badge nutriscore-${ns} my-1`;

    // Macros Highlight
    const ps = recipe.per_serving || {};
    const cal = ps.calories || 0;
    const prot = ps.protein || 0;
    const carbs = ps.carbohydrates || 0;
    const fats = ps.fats || 0;
    const fiber = ps.fiber || 0;

    document.getElementById('res-calories').textContent = cal.toFixed(0);
    const servingLabelElem = document.getElementById('res-serving-label');
    if (servingLabelElem) {
        servingLabelElem.textContent = weightEst.perServingG > 0 ? `Por ración (~${weightEst.perServingG}g)` : 'Por ración';
    }
    document.getElementById('res-protein').textContent = prot.toFixed(1);
    document.getElementById('res-carbs').textContent = carbs.toFixed(1);
    document.getElementById('res-fats').textContent = fats.toFixed(1);
    document.getElementById('res-fiber').textContent = fiber.toFixed(1);

    // Porcentaje de calorías por macro
    const protCal = prot * 4;
    const carbsCal = carbs * 4;
    const fatsCal = fats * 9;
    const totalCalMacros = protCal + carbsCal + fatsCal || 1;

    document.getElementById('res-protein-pct').textContent = `${((protCal / totalCalMacros) * 100).toFixed(0)}% kcal`;
    document.getElementById('res-carbs-pct').textContent = `${((carbsCal / totalCalMacros) * 100).toFixed(0)}% kcal`;
    document.getElementById('res-fats-pct').textContent = `${((fatsCal / totalCalMacros) * 100).toFixed(0)}% kcal`;

    // Render Macro Donut Chart
    renderMacroDonutChart(protCal, carbsCal, fatsCal);

    // Micronutrientes y Detalle
    const tot = recipe.total || {};
    document.getElementById('res-sugar-serving').textContent = `${(ps.sugar || 0).toFixed(1)} g`;
    document.getElementById('res-sugar-total').textContent = `${(tot.sugar || 0).toFixed(1)} g`;
    setNutrientTag('res-sugar-tag', ps.sugar, 5, 12, 'g');

    document.getElementById('res-satfat-serving').textContent = `${(ps.saturated_fat || 0).toFixed(1)} g`;
    document.getElementById('res-satfat-total').textContent = `${(tot.saturated_fat || 0).toFixed(1)} g`;
    setNutrientTag('res-satfat-tag', ps.saturated_fat, 2, 5, 'g');

    document.getElementById('res-sodium-serving').textContent = `${(ps.sodium || 0).toFixed(0)} mg`;
    document.getElementById('res-sodium-total').textContent = `${(tot.sodium || 0).toFixed(0)} mg`;
    setNutrientTag('res-sodium-tag', ps.sodium, 400, 800, 'mg');

    document.getElementById('res-chol-serving').textContent = `${(ps.cholesterol || 0).toFixed(0)} mg`;
    document.getElementById('res-chol-total').textContent = `${(tot.cholesterol || 0).toFixed(0)} mg`;

    document.getElementById('res-potassium-serving').textContent = `${(ps.potassium || 0).toFixed(0)} mg`;
    document.getElementById('res-potassium-total').textContent = `${(tot.potassium || 0).toFixed(0)} mg`;

    // Vitaminas y Minerales
    const vitContainer = document.getElementById('res-vitamins-container');
    vitContainer.innerHTML = '';
    const vits = ps.vitamins_and_minerals || [];
    if (vits.length === 0) {
        vitContainer.innerHTML = '<span class="text-xs text-slate-400">Equilibrio vitamínico estándar</span>';
    } else {
        vits.forEach(v => {
            const span = document.createElement('span');
            span.className = 'px-2 py-0.5 rounded-full text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200/50';
            span.textContent = v;
            vitContainer.appendChild(span);
        });
    }

    // Dietary Tags
    const tagsContainer = document.getElementById('res-tags-container');
    tagsContainer.innerHTML = '';
    (recipe.dietary_tags || []).forEach(t => {
        const span = document.createElement('span');
        span.className = 'px-2 py-0.5 rounded-full text-[11px] font-semibold bg-slate-100 text-slate-700';
        span.textContent = t;
        tagsContainer.appendChild(span);
    });

    // Ingredientes
    const ingList = document.getElementById('res-ingredients-list');
    ingList.innerHTML = '';
    (recipe.ingredients || []).forEach(ing => {
        const li = document.createElement('li');
        li.className = 'flex items-center justify-between p-2 rounded-xl bg-slate-50 border border-slate-100';
        li.innerHTML = `
            <div class="flex items-center space-x-2">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                <span class="font-semibold text-slate-800">${ing.name}</span>
                <span class="text-slate-500">(${ing.amount})</span>
            </div>
            ${ing.calories ? `<span class="text-[11px] font-medium text-slate-400">${ing.calories.toFixed(0)} kcal</span>` : ''}
        `;
        ingList.appendChild(li);
    });

    // Instrucciones
    const insList = document.getElementById('res-instructions-list');
    insList.innerHTML = '';
    (recipe.instructions || []).forEach((step, idx) => {
        const li = document.createElement('li');
        li.className = 'flex items-start space-x-2.5';
        li.innerHTML = `
            <span class="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-100 text-emerald-800 font-bold flex items-center justify-center text-[10px] mt-0.5">${idx + 1}</span>
            <span class="text-slate-700">${step}</span>
        `;
        insList.appendChild(li);
    });

    // Veredicto y Alternativas
    document.getElementById('res-verdict-text').textContent = recipe.health_verdict || 'Receta equilibrada apta para consumo regular.';
    const altList = document.getElementById('res-alternatives-list');
    altList.innerHTML = '';
    (recipe.healthier_alternatives || []).forEach(alt => {
        const li = document.createElement('li');
        li.textContent = alt;
        altList.appendChild(li);
    });

    safeCreateIcons();
    resultsElem.scrollIntoView({ behavior: 'smooth' });
}

function setNutrientTag(elemId, value, lowThreshold, highThreshold, unit) {
    const elem = document.getElementById(elemId);
    if (!elem) return;
    const v = value || 0;
    if (v <= lowThreshold) {
        elem.textContent = 'Bajo (Óptimo)';
        elem.className = 'px-2 py-0.5 rounded text-[10px] bg-emerald-100 text-emerald-800 font-medium';
    } else if (v <= highThreshold) {
        elem.textContent = 'Moderado';
        elem.className = 'px-2 py-0.5 rounded text-[10px] bg-amber-100 text-amber-800 font-medium';
    } else {
        elem.textContent = 'Alto';
        elem.className = 'px-2 py-0.5 rounded text-[10px] bg-rose-100 text-rose-800 font-medium';
    }
}

function renderMacroDonutChart(protCal, carbsCal, fatsCal) {
    const ctx = document.getElementById('macroDonutChart').getContext('2d');
    if (macroDonutChartInstance) {
        macroDonutChartInstance.destroy();
    }
    macroDonutChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Proteína', 'Carbohidratos', 'Grasas'],
            datasets: [{
                data: [protCal, carbsCal, fatsCal],
                backgroundColor: ['#3b82f6', '#f59e0b', '#f43f5e'],
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` ${context.label}: ${context.raw.toFixed(0)} kcal`;
                        }
                    }
                }
            }
        }
    });
}

// ==========================================
// SAVE & MANAGE RECIPES
// ==========================================
async function saveCurrentRecipe() {
    if (!currentAnalysisRecipe) return;
    try {
        const resp = await fetch('/api/recipes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentAnalysisRecipe)
        });
        if (resp.ok) {
            const saved = await resp.json();
            currentAnalysisRecipe = saved;
            alert('¡Receta guardada exitosamente en Mi Recetario!');
            await loadRecipes();
        } else {
            alert('No se pudo guardar la receta.');
        }
    } catch (e) {
        alert(`Error al guardar receta: ${e.message}`);
    }
}

async function loadRecipes() {
    try {
        const resp = await fetch('/api/recipes');
        if (resp.ok) {
            savedRecipes = await resp.json();
            updateCategoryFilterCounts();
            renderRecipesGrid();
            renderCompareSelectionGrid();
        }
    } catch (e) {
        console.error('Error cargando recetas:', e);
    }
}

function updateCategoryFilterCounts() {
    const counts = {
        'all': savedRecipes.length,
        'desayuno': 0,
        'comida': 0,
        'merienda': 0,
        'cena': 0,
        'postre': 0
    };

    savedRecipes.forEach(r => {
        const cat = (r.category || 'comida').toLowerCase();
        if (counts[cat] !== undefined) {
            counts[cat]++;
        } else if (cat === 'merienda-postre') {
            counts['merienda']++;
        } else {
            counts['comida']++;
        }
    });

    for (const [key, cnt] of Object.entries(counts)) {
        const el = document.getElementById(`cat-count-${key}`);
        if (el) el.textContent = cnt;
    }
}

function setCategoryFilter(category) {
    currentCategoryFilter = category;
    const cats = ['all', 'desayuno', 'comida', 'merienda', 'cena', 'postre'];
    cats.forEach(c => {
        const btn = document.getElementById(`cat-btn-${c}`);
        const countSpan = document.getElementById(`cat-count-${c}`);
        if (!btn) return;
        if (c === category) {
            btn.className = 'cat-filter-btn px-4 py-2 rounded-xl text-xs font-bold transition bg-emerald-600 text-white shadow-sm flex items-center space-x-1.5 flex-shrink-0';
            if (countSpan) countSpan.className = 'ml-1 px-1.5 py-0.5 text-[10px] rounded-full bg-white/20 text-white';
        } else {
            btn.className = 'cat-filter-btn px-4 py-2 rounded-xl text-xs font-bold transition bg-slate-100 text-slate-700 hover:bg-slate-200 flex items-center space-x-1.5 flex-shrink-0';
            if (countSpan) countSpan.className = 'ml-1 px-1.5 py-0.5 text-[10px] rounded-full bg-slate-200 text-slate-700';
        }
    });
    renderRecipesGrid();
}

function renderRecipesGrid() {
    const grid = document.getElementById('recipes-book-grid');
    if (!grid) return;
    grid.innerHTML = '';

    const filterText = (document.getElementById('recipe-search')?.value || '').toLowerCase();
    const filtered = savedRecipes.filter(r => {
        const matchesText = !filterText || 
            (r.title && r.title.toLowerCase().includes(filterText)) || 
            (r.dietary_tags || []).some(t => t.toLowerCase().includes(filterText)) ||
            (r.ingredients || []).some(i => i.name && i.name.toLowerCase().includes(filterText));

        const cat = (r.category || 'comida').toLowerCase();
        const matchesCat = (currentCategoryFilter === 'all') || (cat === currentCategoryFilter);

        return matchesText && matchesCat;
    });

    if (filtered.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full py-12 text-center text-slate-400">
                <i data-lucide="chef-hat" class="w-12 h-12 mx-auto text-slate-300 mb-2"></i>
                <p class="text-sm font-medium">No se encontraron recetas para esta categoría o búsqueda.</p>
                <p class="text-xs text-slate-400">Prueba con otra categoría o analiza una nueva receta.</p>
            </div>
        `;
        safeCreateIcons();
        return;
    }

    filtered.forEach(recipe => {
        const ps = recipe.per_serving || {};
        const ns = (recipe.nutri_score || 'B').toUpperCase();
        const catKey = (recipe.category || 'comida').toLowerCase();
        const catMeta = CATEGORY_META[catKey] || CATEGORY_META['comida'];
        const vUrl = recipe.video_url || (recipe.source_reference && recipe.source_reference.startsWith('http') ? recipe.source_reference : null);
        const weight = calculateEstimatedServingWeight(recipe);

        const card = document.createElement('div');
        card.className = 'bg-white rounded-2xl border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between overflow-hidden group';
        card.innerHTML = `
            ${recipe.image_url ? `
                <div class="h-44 w-full relative overflow-hidden bg-slate-100">
                    <img src="${recipe.image_url}" alt="${recipe.title}" referrerpolicy="no-referrer" class="w-full h-full object-cover transition-transform duration-300 hover:scale-105" onerror="this.parentElement.style.display='none'">
                    <span class="nutriscore-badge nutriscore-${ns} text-xs w-7 h-7 absolute top-3 left-3 shadow">${ns}</span>
                    <span class="text-[10px] font-bold px-2.5 py-0.5 rounded-full ${catMeta.color} border shadow-sm absolute top-3 right-3 backdrop-blur-sm">
                        ${catMeta.icon} ${catMeta.label}
                    </span>
                    <button onclick="openEditPhotoModal('${recipe.id}', event)" class="p-1.5 rounded-xl bg-black/60 hover:bg-black/80 text-white transition absolute bottom-2.5 left-2.5 shadow backdrop-blur-sm flex items-center space-x-1" title="Cambiar foto de la receta">
                        <i data-lucide="camera" class="w-3.5 h-3.5"></i>
                        <span class="text-[10px] font-medium hidden sm:inline">Foto</span>
                    </button>
                    <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-black/60 text-white backdrop-blur-sm absolute bottom-2.5 right-2.5">
                        ${recipe.servings || 1} ${recipe.servings > 1 ? 'raciones' : 'ración'} (~${weight.perServingG}g)
                    </span>
                </div>
            ` : ''}
            <div class="p-5 space-y-3 flex-1 flex flex-col justify-between">
                <div class="space-y-2">
                    ${!recipe.image_url ? `
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-2">
                                <span class="nutriscore-badge nutriscore-${ns} text-xs w-7 h-7">${ns}</span>
                                <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${catMeta.color} border">
                                    ${catMeta.icon} ${catMeta.label}
                                </span>
                            </div>
                            <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                                ${recipe.servings || 1} ${recipe.servings > 1 ? 'raciones' : 'ración'} (~${weight.perServingG}g)
                            </span>
                        </div>
                    ` : ''}
                    <h3 class="text-base font-bold text-slate-800 line-clamp-1">${recipe.title}</h3>
                    <p class="text-xs text-slate-500 line-clamp-2">${recipe.description || 'Sin descripción'}</p>
                    
                    <!-- Badges de Macros -->
                    <div class="grid grid-cols-4 gap-1 text-center pt-2 border-t border-slate-100 text-[11px]">
                        <div class="bg-slate-50 p-1.5 rounded-lg">
                            <span class="text-slate-400 block text-[9px] uppercase">Kcal</span>
                            <span class="font-bold text-emerald-700">${(ps.calories || 0).toFixed(0)}</span>
                        </div>
                        <div class="bg-blue-50/60 p-1.5 rounded-lg">
                            <span class="text-blue-400 block text-[9px] uppercase">Prot</span>
                            <span class="font-bold text-blue-700">${(ps.protein || 0).toFixed(0)}g</span>
                        </div>
                        <div class="bg-amber-50/60 p-1.5 rounded-lg">
                            <span class="text-amber-400 block text-[9px] uppercase">Carb</span>
                            <span class="font-bold text-amber-700">${(ps.carbohydrates || 0).toFixed(0)}g</span>
                        </div>
                        <div class="bg-rose-50/60 p-1.5 rounded-lg">
                            <span class="text-rose-400 block text-[9px] uppercase">Grasa</span>
                            <span class="font-bold text-rose-700">${(ps.fats || 0).toFixed(0)}g</span>
                        </div>
                    </div>
                </div>

                <!-- Acciones -->
                <div class="flex items-center justify-between pt-2 border-t border-slate-100">
                    <button onclick="openRecipeModal('${recipe.id}')" class="text-xs font-bold text-emerald-600 hover:text-emerald-700 flex items-center space-x-1">
                        <i data-lucide="eye" class="w-3.5 h-3.5"></i>
                        <span>Ver Detalle</span>
                    </button>
                    <div class="flex items-center space-x-1.5">
                        <button onclick="openEditPhotoModal('${recipe.id}', event)" class="p-1.5 rounded-lg text-xs font-semibold text-slate-500 hover:text-emerald-700 hover:bg-emerald-50 transition" title="Cambiar foto de la receta">
                            <i data-lucide="camera" class="w-4 h-4"></i>
                        </button>
                        ${vUrl ? `
                            <a href="${vUrl}" target="_blank" rel="noopener noreferrer" class="p-1.5 rounded-lg text-xs font-bold text-rose-600 bg-rose-50 hover:bg-rose-100 border border-rose-200 transition flex items-center space-x-1" title="Ver vídeo original">
                                <i data-lucide="video" class="w-3.5 h-3.5"></i>
                                <span class="text-[10px]">Vídeo</span>
                            </a>
                        ` : ''}
                        <button onclick="toggleCompareRecipe('${recipe.id}')" class="p-1.5 rounded-lg text-xs font-semibold ${selectedForCompare.has(recipe.id) ? 'bg-emerald-600 text-white' : 'hover:bg-slate-100 text-slate-600'} transition" title="Añadir a comparar">
                            <i data-lucide="scale" class="w-4 h-4"></i>
                        </button>
                        <button onclick="deleteRecipe('${recipe.id}')" class="p-1.5 rounded-lg text-xs font-semibold text-rose-500 hover:bg-rose-50 transition" title="Eliminar">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
    safeCreateIcons();
}

function filterRecipesList() {
    renderRecipesGrid();
}

async function deleteRecipe(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar esta receta?')) return;
    try {
        const resp = await fetch(`/api/recipes/${id}`, { method: 'DELETE' });
        if (resp.ok) {
            selectedForCompare.delete(id);
            updateCompareBadge();
            await loadRecipes();
        }
    } catch (e) {
        alert('Error eliminando receta');
    }
}

// ==========================================
// RECIPE DETAILS MODAL
// ==========================================
function openRecipeModal(recipeId) {
    const recipe = savedRecipes.find(r => r.id === recipeId);
    if (!recipe) return;

    document.getElementById('modal-title').textContent = recipe.title;
    const body = document.getElementById('modal-body');
    const ps = recipe.per_serving || {};
    const catKey = (recipe.category || 'comida').toLowerCase();
    const catMeta = CATEGORY_META[catKey] || CATEGORY_META['comida'];
    const vUrl = recipe.video_url || (recipe.source_reference && recipe.source_reference.startsWith('http') ? recipe.source_reference : null);
    const weight = calculateEstimatedServingWeight(recipe);

    body.innerHTML = `
        ${recipe.image_url ? `
            <div class="w-full h-52 sm:h-64 rounded-2xl overflow-hidden mb-4 shadow border border-slate-200 relative group">
                <img src="${recipe.image_url}" alt="${recipe.title}" referrerpolicy="no-referrer" onerror="this.parentElement.style.display='none'" class="w-full h-full object-cover">
                <button onclick="openEditPhotoModal('${recipe.id}')" class="absolute bottom-3 right-3 px-3 py-1.5 rounded-xl bg-slate-900/75 hover:bg-slate-900 text-white font-medium text-xs flex items-center space-x-1.5 backdrop-blur-sm transition shadow-lg">
                    <i data-lucide="camera" class="w-3.5 h-3.5 text-emerald-400"></i>
                    <span>Cambiar Foto</span>
                </button>
            </div>
        ` : `
            <div class="mb-4 flex justify-end">
                <button onclick="openEditPhotoModal('${recipe.id}')" class="px-3.5 py-1.5 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-emerald-700 font-semibold text-xs flex items-center space-x-1.5 border border-emerald-200 transition">
                    <i data-lucide="camera" class="w-3.5 h-3.5"></i>
                    <span>Añadir Foto</span>
                </button>
            </div>
        `}

        <div class="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-slate-100">
            <div class="flex flex-wrap items-center gap-2">
                <div class="inline-flex items-center space-x-1.5 bg-slate-50 px-2.5 py-1 rounded-xl border border-slate-200">
                    <span class="text-[11px] font-semibold text-slate-500">Momento:</span>
                    <select onchange="updateRecipeCategory('${recipe.id}', this.value)" class="text-xs font-bold py-0.5 px-2 rounded-lg border outline-none cursor-pointer transition ${catMeta.color}">
                        <option value="desayuno" ${catKey === 'desayuno' ? 'selected' : ''}>🌅 Desayuno</option>
                        <option value="comida" ${catKey === 'comida' ? 'selected' : ''}>🍽️ Comida</option>
                        <option value="merienda" ${catKey === 'merienda' ? 'selected' : ''}>☕ Merienda</option>
                        <option value="cena" ${catKey === 'cena' ? 'selected' : ''}>🌙 Cena</option>
                        <option value="postre" ${catKey === 'postre' ? 'selected' : ''}>🍰 Postre</option>
                    </select>
                    <span id="cat-saved-check-${recipe.id}" class="hidden text-emerald-600 text-[11px] font-bold">✓ Guardado</span>
                </div>
                <span class="px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-700">
                    ${recipe.servings || 1} ${recipe.servings > 1 ? 'raciones' : 'ración'} (~${weight.perServingG}g / ración)
                </span>
                <span class="px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-700">
                    ⏱️ ${(recipe.prep_time_minutes || 0) + (recipe.cook_time_minutes || 0) || 20} min
                </span>
            </div>

            <div class="flex items-center space-x-2">
                <button onclick="openEditPhotoModal('${recipe.id}')" class="inline-flex items-center space-x-1 px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs transition">
                    <i data-lucide="camera" class="w-3.5 h-3.5 text-slate-600"></i>
                    <span>Foto</span>
                </button>
                ${vUrl ? `
                    <a href="${vUrl}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center space-x-1.5 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-rose-500 to-red-600 hover:from-rose-600 hover:to-red-700 text-white font-bold text-xs shadow-sm transition">
                        <i data-lucide="play-circle" class="w-4 h-4"></i>
                        <span>Ver vídeo</span>
                    </a>
                ` : ''}
            </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center pt-2">
            <div class="bg-emerald-50 p-2.5 rounded-xl"><span class="block text-[10px] text-emerald-600 uppercase font-bold">Calorías</span><span class="text-lg font-extrabold text-emerald-800">${ps.calories?.toFixed(0) || 0} kcal</span><span class="block text-[9px] text-emerald-600/80">~${weight.perServingG}g / ración</span></div>
            <div class="bg-blue-50 p-2.5 rounded-xl"><span class="block text-[10px] text-blue-600 uppercase font-bold">Proteína</span><span class="text-lg font-extrabold text-blue-800">${ps.protein?.toFixed(1) || 0} g</span></div>
            <div class="bg-amber-50 p-2.5 rounded-xl"><span class="block text-[10px] text-amber-600 uppercase font-bold">Carbos</span><span class="text-lg font-extrabold text-amber-800">${ps.carbohydrates?.toFixed(1) || 0} g</span></div>
            <div class="bg-rose-50 p-2.5 rounded-xl"><span class="block text-[10px] text-rose-600 uppercase font-bold">Grasas</span><span class="text-lg font-extrabold text-rose-800">${ps.fats?.toFixed(1) || 0} g</span></div>
        </div>

        <div class="space-y-2">
            <h4 class="font-bold text-slate-800">Ingredientes:</h4>
            <ul class="list-disc list-inside space-y-1 text-slate-600">
                ${(recipe.ingredients || []).map(i => `<li><strong>${i.name}</strong> - ${i.amount}</li>`).join('')}
            </ul>
        </div>

        <div class="space-y-2">
            <h4 class="font-bold text-slate-800">Preparación:</h4>
            <ol class="list-decimal list-inside space-y-1 text-slate-600">
                ${(recipe.instructions || []).map(step => `<li>${step}</li>`).join('')}
            </ol>
        </div>

        <div class="bg-emerald-50/70 p-3.5 rounded-xl border border-emerald-200">
            <h4 class="font-bold text-emerald-900 mb-1">Dictamen del Nutricionista:</h4>
            <p class="text-slate-700">${recipe.health_verdict || 'Perfil nutricional verificado.'}</p>
        </div>
    `;

    document.getElementById('recipe-modal').classList.remove('hidden');
    safeCreateIcons();
}

function closeRecipeModal() {
    document.getElementById('recipe-modal').classList.add('hidden');
}

async function updateRecipeCategory(recipeId, newCat) {
    try {
        const resp = await fetch(`/api/recipes/${recipeId}/category`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category: newCat })
        });
        if (!resp.ok) {
            const errData = await resp.json();
            throw new Error(errData.detail || 'Error al actualizar categoría');
        }

        // Actualizar en memoria
        const idx = savedRecipes.findIndex(r => r.id === recipeId);
        if (idx !== -1) savedRecipes[idx].category = newCat;
        if (currentAnalysisRecipe && currentAnalysisRecipe.id === recipeId) {
            currentAnalysisRecipe.category = newCat;
        }

        // Feedback visual en el modal
        const check = document.getElementById(`cat-saved-check-${recipeId}`);
        if (check) {
            check.classList.remove('hidden');
            setTimeout(() => {
                if (check) check.classList.add('hidden');
            }, 2500);
        }

        updateCategoryFilterCounts();
        renderRecipesGrid();
    } catch (e) {
        alert('No se pudo guardar la categoría: ' + e.message);
    }
}

async function triggerAutoFixPhotos() {
    const btn = document.getElementById('btn-auto-fix-photos');
    const origHtml = btn ? btn.innerHTML : '';
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="inline-block animate-spin mr-1.5">✨</span> <span>Corrigiendo fotos...</span>';
    }

    try {
        const resp = await fetch('/api/recipes/auto-fix-photos', { method: 'POST' });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Error al ejecutar la corrección automática.');

        await loadSavedRecipes();
        alert(`✅ ¡Completado! ${data.message || 'Fotos actualizadas correctamente.'}`);
    } catch (e) {
        alert('Aviso al auto-corregir fotos: ' + e.message);
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = origHtml;
            safeCreateIcons();
        }
    }
}

// ==========================================
// ==========================================
// PHOTO MODAL HANDLERS & IMAGE SEARCH
// ==========================================
let editPhotoSelectedFile = null;
let currentPhotoResults = [];

function switchEditPhotoTab(tab) {
    const tabs = ['search', 'ai', 'upload', 'url'];
    tabs.forEach(t => {
        const btn = document.getElementById(`tab-btn-photo-${t}`);
        const panel = document.getElementById(`photo-tab-panel-${t}`);
        if (t === tab) {
            if (btn) {
                btn.className = 'px-3 py-2 font-bold rounded-xl transition text-emerald-700 bg-emerald-50 border border-emerald-200 flex items-center space-x-1.5';
            }
            if (panel) panel.classList.remove('hidden');
        } else {
            if (btn) {
                btn.className = 'px-3 py-2 font-semibold rounded-xl transition text-slate-500 hover:text-slate-800 hover:bg-slate-100 flex items-center space-x-1.5';
            }
            if (panel) panel.classList.add('hidden');
        }
    });
    safeCreateIcons();
}

function openEditPhotoModal(recipeId, event) {
    if (event) event.stopPropagation();
    const recipe = savedRecipes.find(r => r.id === recipeId);
    if (!recipe) return;

    document.getElementById('edit-photo-recipe-id').value = recipeId;
    document.getElementById('edit-photo-recipe-title').textContent = recipe.title || 'Receta';

    const aiDishName = document.getElementById('edit-photo-ai-dish-name');
    if (aiDishName) aiDishName.textContent = recipe.title || 'este plato';

    const preview = document.getElementById('edit-photo-preview');
    if (preview) {
        preview.src = recipe.image_url || 'https://images.unsplash.com/photo-1498837167922-ddd27525d352?w=700&auto=format&fit=crop&q=80';
    }

    const selectedLabel = document.getElementById('edit-photo-selected-label');
    if (selectedLabel) selectedLabel.textContent = 'Foto actual del plato';

    const fileInput = document.getElementById('edit-photo-file-input');
    if (fileInput) fileInput.value = '';

    const urlInput = document.getElementById('edit-photo-url-input');
    if (urlInput) urlInput.value = (recipe.image_url && recipe.image_url.startsWith('http')) ? recipe.image_url : '';

    const searchInput = document.getElementById('photo-search-input');
    if (searchInput) searchInput.value = recipe.title || '';

    const aiStatusMsg = document.getElementById('photo-ai-status-msg');
    if (aiStatusMsg) {
        aiStatusMsg.classList.add('hidden');
        aiStatusMsg.innerHTML = '';
    }

    editPhotoSelectedFile = null;

    // Abrir por defecto en pestaña buscar
    switchEditPhotoTab('search');

    const modal = document.getElementById('edit-photo-modal');
    if (modal) modal.classList.remove('hidden');
    safeCreateIcons();

    // Búsqueda automática inicial
    searchPhotosModal();
}

function closeEditPhotoModal() {
    const modal = document.getElementById('edit-photo-modal');
    if (modal) modal.classList.add('hidden');
    editPhotoSelectedFile = null;
}

async function searchPhotosModal() {
    const query = (document.getElementById('photo-search-input')?.value || '').trim();
    const grid = document.getElementById('photo-search-results-grid');
    const btn = document.getElementById('btn-photo-search-action');
    if (!grid) return;

    if (!query) {
        grid.innerHTML = '<p class="col-span-full text-slate-400 text-center py-6 text-xs">Introduce el nombre de la receta para buscar fotos.</p>';
        return;
    }

    if (btn) btn.disabled = true;
    grid.innerHTML = `
        <div class="col-span-full py-8 text-center text-slate-400 text-xs flex flex-col items-center justify-center space-y-2">
            <span class="inline-block animate-spin text-lg">⏳</span>
            <span>Buscando fotografías gastronómicas para "${escapeHtml(query)}"...</span>
        </div>
    `;

    try {
        const resp = await fetch(`/api/recipes/search-images?q=${encodeURIComponent(query)}`);
        if (!resp.ok) throw new Error('Error al buscar imágenes.');
        const data = await resp.json();
        const results = data.results || [];
        currentPhotoResults = results;

        if (results.length === 0) {
            grid.innerHTML = `
                <div class="col-span-full py-6 text-center text-slate-400 text-xs">
                    <p>No se encontraron fotos exactas para "${escapeHtml(query)}".</p>
                    <p class="text-[11px] text-emerald-600 mt-1 cursor-pointer font-semibold underline" onclick="document.getElementById('photo-search-input').value='plato comida'; searchPhotosModal();">Ver sugerencias generales</p>
                </div>
            `;
            return;
        }

        const currentUrl = (document.getElementById('edit-photo-url-input')?.value || '').trim();
        grid.innerHTML = results.map((item, idx) => {
            const isSelected = item.url === currentUrl;
            return `
                <div onclick="selectPhotoResult(${idx})" 
                     id="photo-card-${idx}" 
                     class="group cursor-pointer rounded-xl overflow-hidden border-2 transition relative aspect-square bg-slate-100 shadow-sm hover:shadow-md ${isSelected ? 'border-emerald-600 ring-2 ring-emerald-500/40' : 'border-slate-200 hover:border-emerald-400'}">
                    <img src="${escapeHtml(item.url)}" alt="${escapeHtml(item.title)}" loading="lazy" class="w-full h-full object-cover transition group-hover:scale-105 duration-200">
                    <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-slate-950/80 via-slate-900/40 to-transparent p-1.5 pt-4 text-white">
                        <p class="text-[10px] font-medium leading-tight line-clamp-1">${escapeHtml(item.title)}</p>
                    </div>
                    <div class="photo-check-badge absolute top-1.5 right-1.5 w-5 h-5 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[10px] shadow-sm ${isSelected ? '' : 'hidden'}">
                        ✓
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        grid.innerHTML = `<p class="col-span-full text-rose-500 text-center py-6 text-xs">${escapeHtml(e.message || 'Error al conectar con el buscador de fotos.')}</p>`;
    } finally {
        if (btn) btn.disabled = false;
        safeCreateIcons();
    }
}

function selectPhotoResult(index) {
    const item = currentPhotoResults[index];
    if (!item) return;

    const preview = document.getElementById('edit-photo-preview');
    if (preview) preview.src = item.url;

    const urlInput = document.getElementById('edit-photo-url-input');
    if (urlInput) urlInput.value = item.url;

    const selectedLabel = document.getElementById('edit-photo-selected-label');
    if (selectedLabel) selectedLabel.textContent = item.title;

    editPhotoSelectedFile = null;
    const fileInput = document.getElementById('edit-photo-file-input');
    if (fileInput) fileInput.value = '';

    document.querySelectorAll('#photo-search-results-grid > div').forEach((el, idx) => {
        const badge = el.querySelector('.photo-check-badge');
        if (idx === index) {
            el.className = 'group cursor-pointer rounded-xl overflow-hidden border-2 transition relative aspect-square bg-slate-100 shadow-md border-emerald-600 ring-2 ring-emerald-500/40';
            if (badge) badge.classList.remove('hidden');
        } else {
            el.className = 'group cursor-pointer rounded-xl overflow-hidden border-2 transition relative aspect-square bg-slate-100 shadow-sm hover:shadow-md border-slate-200 hover:border-emerald-400';
            if (badge) badge.classList.add('hidden');
        }
    });
}

async function generateAiRecipePhoto() {
    const recipeId = document.getElementById('edit-photo-recipe-id')?.value;
    const btn = document.getElementById('btn-generate-ai-photo');
    const statusMsg = document.getElementById('photo-ai-status-msg');
    if (!recipeId) return;

    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="inline-block animate-spin mr-1.5">✨</span> Consultando a Gemini IA...';
    }
    if (statusMsg) {
        statusMsg.classList.remove('hidden');
        statusMsg.className = 'text-center text-xs p-3 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 leading-relaxed';
        statusMsg.innerHTML = '🎨 <strong>Gemini IA está analizando los ingredientes y buscando la mejor foto...</strong>';
    }

    try {
        const resp = await fetch(`/api/recipes/${recipeId}/generate-image`, { method: 'POST' });
        const data = await resp.json();
        if (!resp.ok) {
            throw new Error(data.detail || 'Error al procesar la imagen con IA.');
        }

        const newImageUrl = data.image_url;
        const preview = document.getElementById('edit-photo-preview');
        if (preview) preview.src = newImageUrl;

        const urlInput = document.getElementById('edit-photo-url-input');
        if (urlInput) urlInput.value = newImageUrl;

        const selectedLabel = document.getElementById('edit-photo-selected-label');
        if (selectedLabel) selectedLabel.textContent = '✨ Seleccionada por Gemini IA';

        if (statusMsg) {
            statusMsg.className = 'text-center text-xs p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 leading-relaxed';
            statusMsg.innerHTML = '✅ <strong>¡Fotografía asignada con éxito por Gemini IA!</strong> Hemos actualizado la vista previa. Pulsa "Guardar Foto" para confirmar.';
        }

        // Desplazar suavemente hacia arriba para que el usuario vea la foto inmediatamente
        const scrollArea = document.querySelector('#edit-photo-modal .overflow-y-auto');
        if (scrollArea) scrollArea.scrollTo({ top: 0, behavior: 'smooth' });

        const idx = savedRecipes.findIndex(r => r.id === recipeId);
        if (idx !== -1) savedRecipes[idx].image_url = newImageUrl;
        if (currentAnalysisRecipe && currentAnalysisRecipe.id === recipeId) {
            currentAnalysisRecipe.image_url = newImageUrl;
        }
        renderRecipesGrid();
    } catch (e) {
        if (statusMsg) {
            statusMsg.className = 'text-left text-xs p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-900 leading-relaxed';
            statusMsg.innerHTML = `⚠️ <strong>Aviso:</strong> ${escapeHtml(e.message)}<br><span class="block mt-1 text-[11px] text-slate-600">💡 También puedes usar la pestaña <strong>"Buscar Fotos"</strong> para elegir una foto real en la galería.</span>`;
        }
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i data-lucide="sparkles" class="w-4 h-4 mr-1"></i><span>Asignar Foto con Gemini IA</span>';
            safeCreateIcons();
        }
    }
}

function handleRecipePhotoFileSelected(event) {
    const file = event.target.files[0];
    if (file) {
        editPhotoSelectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.getElementById('edit-photo-preview');
            if (preview) preview.src = e.target.result;
            const selectedLabel = document.getElementById('edit-photo-selected-label');
            if (selectedLabel) selectedLabel.textContent = `Archivo: ${file.name}`;
        };
        reader.readAsDataURL(file);
    }
}

function handleRecipePhotoUrlInput(url) {
    if (url && url.trim().length > 6) {
        const preview = document.getElementById('edit-photo-preview');
        if (preview) preview.src = url.trim();
        const selectedLabel = document.getElementById('edit-photo-selected-label');
        if (selectedLabel) selectedLabel.textContent = 'Enlace web introducido';
        editPhotoSelectedFile = null;
        const fileInput = document.getElementById('edit-photo-file-input');
        if (fileInput) fileInput.value = '';
    }
}

async function saveRecipePhoto() {
    const recipeId = document.getElementById('edit-photo-recipe-id')?.value;
    const urlVal = (document.getElementById('edit-photo-url-input')?.value || '').trim();
    if (!recipeId) return;

    if (!editPhotoSelectedFile && !urlVal) {
        alert('Por favor, selecciona una foto de las sugerencias, de tu dispositivo o pega un enlace de imagen.');
        return;
    }

    const btn = document.getElementById('btn-save-recipe-photo');
    const originalBtnText = btn ? btn.innerHTML : '';
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="inline-block animate-spin mr-1">⏳</span> Guardando...';
    }

    try {
        const formData = new FormData();
        if (editPhotoSelectedFile) {
            formData.append('file', editPhotoSelectedFile);
        } else if (urlVal) {
            formData.append('image_url', urlVal);
        }

        const resp = await fetch(`/api/recipes/${recipeId}/image`, {
            method: 'POST',
            body: formData
        });

        if (!resp.ok) {
            const err = await extractResponseError(resp, 'Error al guardar la foto.');
            throw new Error(err);
        }

        const data = await resp.json();
        const newImageUrl = data.image_url;

        // Actualizar receta en memoria local
        const idx = savedRecipes.findIndex(r => r.id === recipeId);
        if (idx !== -1) {
            savedRecipes[idx].image_url = newImageUrl;
        }
        if (currentAnalysisRecipe && currentAnalysisRecipe.id === recipeId) {
            currentAnalysisRecipe.image_url = newImageUrl;
        }

        closeEditPhotoModal();
        renderRecipesGrid();

        // Si el modal de la receta estaba abierto, actualizarlo también
        const recipeModal = document.getElementById('recipe-modal');
        if (recipeModal && !recipeModal.classList.contains('hidden')) {
            openRecipeModal(recipeId);
        }
    } catch (e) {
        alert(e.message || 'Error al actualizar la foto.');
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = originalBtnText;
            safeCreateIcons();
        }
    }
}

// ==========================================
// COMPARATOR ENGINE
// ==========================================
function addCurrentRecipeToCompare() {
    if (!currentAnalysisRecipe) return;
    if (!currentAnalysisRecipe.id) {
        currentAnalysisRecipe.id = 'temp-' + Date.now();
        savedRecipes.push(currentAnalysisRecipe);
    }
    selectedForCompare.add(currentAnalysisRecipe.id);
    updateCompareBadge();
    switchTab('comparator');
}

function toggleCompareRecipe(id) {
    if (selectedForCompare.has(id)) {
        selectedForCompare.delete(id);
    } else {
        if (selectedForCompare.size >= 4) {
            alert('Puedes comparar hasta un máximo de 4 recetas simultáneamente.');
            return;
        }
        selectedForCompare.add(id);
    }
    updateCompareBadge();
    renderCompareSelectionGrid();
    renderRecipesGrid();
}

function updateCompareBadge() {
    const badge = document.getElementById('compare-badge');
    if (!badge) return;
    if (selectedForCompare.size > 0) {
        badge.textContent = selectedForCompare.size;
        badge.classList.remove('hidden');
    } else {
        badge.classList.add('hidden');
    }
}

function renderCompareSelectionGrid() {
    const grid = document.getElementById('compare-selection-grid');
    if (!grid) return;
    grid.innerHTML = '';

    if (savedRecipes.length === 0) {
        grid.innerHTML = '<p class="text-xs text-slate-400 col-span-full">Aún no hay recetas para comparar.</p>';
        return;
    }

    savedRecipes.forEach(r => {
        const isSelected = selectedForCompare.has(r.id);
        const div = document.createElement('div');
        div.onclick = () => toggleCompareRecipe(r.id);
        div.className = `p-3 rounded-xl border cursor-pointer transition flex items-center justify-between ${isSelected ? 'border-emerald-500 bg-emerald-50/60 shadow-sm' : 'border-slate-200 bg-white hover:bg-slate-50'}`;
        div.innerHTML = `
            <div class="flex items-center space-x-2">
                <input type="checkbox" ${isSelected ? 'checked' : ''} class="rounded text-emerald-600 focus:ring-emerald-500 pointer-events-none">
                <div>
                    <span class="text-xs font-bold text-slate-800 line-clamp-1">${r.title}</span>
                    <span class="text-[11px] text-slate-400">${(r.per_serving?.calories || 0).toFixed(0)} kcal | ${(r.per_serving?.protein || 0).toFixed(0)}g prot</span>
                </div>
            </div>
            <span class="nutriscore-badge nutriscore-${(r.nutri_score || 'B').toUpperCase()} text-[10px] w-5 h-5">${(r.nutri_score || 'B').toUpperCase()}</span>
        `;
        grid.appendChild(div);
    });
}

async function runComparison() {
    if (selectedForCompare.size < 2) {
        alert('Por favor, selecciona al menos 2 recetas para iniciar la comparación.');
        return;
    }

    const btn = document.getElementById('btn-run-compare');
    btn.disabled = true;
    btn.innerHTML = '<span>Comparando...</span>';

    try {
        const resp = await fetch('/api/compare', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ recipe_ids: Array.from(selectedForCompare) })
        });

        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(err.detail || 'Error al comparar recetas');
        }

        const compResult = await resp.json();
        renderComparisonResults(compResult);

    } catch (e) {
        alert(e.message);
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i data-lucide="bar-chart-2" class="w-4 h-4"></i><span>Comparar Seleccionadas</span>';
        safeCreateIcons();
    }
}

function renderComparisonResults(compResult) {
    const resElem = document.getElementById('comparison-results');
    resElem.classList.remove('hidden');

    // Winners
    document.getElementById('cmp-winner-muscle').textContent = compResult.winner_for_muscle_gain;
    document.getElementById('cmp-winner-fatloss').textContent = compResult.winner_for_fat_loss;
    document.getElementById('cmp-winner-health').textContent = compResult.winner_for_general_health;

    const recipes = compResult.recipes || [];
    const labels = recipes.map(r => r.title.length > 18 ? r.title.substring(0, 16) + '...' : r.title);

    // Chart 1: Grouped Bar Chart (Macros)
    const ctxBar = document.getElementById('compareBarChart').getContext('2d');
    if (compareBarChartInstance) compareBarChartInstance.destroy();

    compareBarChartInstance = new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Proteínas (g)',
                    data: recipes.map(r => r.per_serving?.protein || 0),
                    backgroundColor: '#3b82f6',
                    borderRadius: 6
                },
                {
                    label: 'Carbohidratos (g)',
                    data: recipes.map(r => r.per_serving?.carbohydrates || 0),
                    backgroundColor: '#f59e0b',
                    borderRadius: 6
                },
                {
                    label: 'Grasas (g)',
                    data: recipes.map(r => r.per_serving?.fats || 0),
                    backgroundColor: '#f43f5e',
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            },
            scales: {
                y: { beginAtZero: true, title: { display: true, text: 'Gramos (g)' } }
            }
        }
    });

    // Chart 2: Calories & Fiber
    const ctxCal = document.getElementById('compareCaloriesChart').getContext('2d');
    if (compareCaloriesChartInstance) compareCaloriesChartInstance.destroy();

    compareCaloriesChartInstance = new Chart(ctxCal, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Calorías (Kcal)',
                    data: recipes.map(r => r.per_serving?.calories || 0),
                    backgroundColor: '#10b981',
                    borderRadius: 6,
                    yAxisID: 'y'
                },
                {
                    label: 'Fibra (g)',
                    data: recipes.map(r => r.per_serving?.fiber || 0),
                    backgroundColor: '#0d9488',
                    borderRadius: 6,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: { display: true, text: 'Calorías (Kcal)' }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    grid: { drawOnChartArea: false },
                    title: { display: true, text: 'Fibra (g)' }
                }
            }
        }
    });

    // Table side-by-side
    const table = document.getElementById('comparison-table');
    table.innerHTML = `
        <thead>
            <tr class="border-b border-slate-200 text-slate-500">
                <th class="py-2.5 font-bold">Métrica</th>
                ${recipes.map(r => `<th class="py-2.5 font-bold">${r.title}</th>`).join('')}
            </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
            <tr>
                <td class="py-2 font-semibold text-slate-700">Nutri-Score</td>
                ${recipes.map(r => `<td class="py-2"><span class="nutriscore-badge nutriscore-${(r.nutri_score||'B').toUpperCase()} text-[10px] w-6 h-6">${(r.nutri_score||'B').toUpperCase()}</span></td>`).join('')}
            </tr>
            <tr>
                <td class="py-2 font-semibold text-slate-700">Calorías por Ración</td>
                ${recipes.map(r => `<td class="py-2 font-bold text-emerald-700">${(r.per_serving?.calories || 0).toFixed(0)} kcal</td>`).join('')}
            </tr>
            <tr>
                <td class="py-2 font-semibold text-slate-700">Proteína</td>
                ${recipes.map(r => `<td class="py-2 font-bold text-blue-700">${(r.per_serving?.protein || 0).toFixed(1)} g</td>`).join('')}
            </tr>
            <tr>
                <td class="py-2 font-semibold text-slate-700">Carbohidratos</td>
                ${recipes.map(r => `<td class="py-2 font-bold text-amber-700">${(r.per_serving?.carbohydrates || 0).toFixed(1)} g</td>`).join('')}
            </tr>
            <tr>
                <td class="py-2 font-semibold text-slate-700">Grasas Totales</td>
                ${recipes.map(r => `<td class="py-2 font-bold text-rose-700">${(r.per_serving?.fats || 0).toFixed(1)} g</td>`).join('')}
            </tr>
            <tr>
                <td class="py-2 font-semibold text-slate-700">Fibra</td>
                ${recipes.map(r => `<td class="py-2 font-bold text-teal-700">${(r.per_serving?.fiber || 0).toFixed(1)} g</td>`).join('')}
            </tr>
            <tr>
                <td class="py-2 font-semibold text-slate-700">Sodio</td>
                ${recipes.map(r => `<td class="py-2 text-slate-600">${(r.per_serving?.sodium || 0).toFixed(0)} mg</td>`).join('')}
            </tr>
        </tbody>
    `;

    safeCreateIcons();
    resElem.scrollIntoView({ behavior: 'smooth' });
}

// ==========================================
// SUGGESTER ENGINE
// ==========================================
async function generateRecipeSuggestions() {
    const loadingElem = document.getElementById('suggestions-loading');
    const gridElem = document.getElementById('suggestions-results-grid');
    const btn = document.getElementById('btn-generate-sug');

    loadingElem.classList.remove('hidden');
    gridElem.innerHTML = '';
    btn.disabled = true;

    const payload = {
        target_calories: parseFloat(document.getElementById('sug-calories').value) || null,
        min_protein: parseFloat(document.getElementById('sug-protein').value) || null,
        max_carbs: parseFloat(document.getElementById('sug-carbs').value) || null,
        max_fat: parseFloat(document.getElementById('sug-fat').value) || null,
        diet_type: document.getElementById('sug-diet').value,
        meal_type: document.getElementById('sug-meal').value,
        available_ingredients: document.getElementById('sug-ingredients').value.trim(),
        count: 3
    };

    try {
        const resp = await fetch('/api/suggest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!resp.ok) {
            let errorMsg = 'Error generando sugerencias';
            try {
                const err = await resp.json();
                errorMsg = err.detail || errorMsg;
            } catch (_) {
                const text = await resp.text();
                errorMsg = text || errorMsg;
            }
            throw new Error(errorMsg);
        }

        const data = await resp.json();
        renderSuggestionsGrid(data.suggestions || []);

    } catch (e) {
        alert(e.message);
    } finally {
        loadingElem.classList.add('hidden');
        btn.disabled = false;
        safeCreateIcons();
    }
}

function renderSuggestionsGrid(suggestions) {
    const grid = document.getElementById('suggestions-results-grid');
    grid.innerHTML = '';

    if (suggestions.length === 0) {
        grid.innerHTML = '<p class="col-span-full text-center text-xs text-slate-400 py-6">No se pudieron generar sugerencias. Ajusta tus parámetros e inténtalo de nuevo.</p>';
        return;
    }

    suggestions.forEach((rec, idx) => {
        const ps = rec.per_serving || {};
        const ns = (rec.nutri_score || 'A').toUpperCase();

        const card = document.createElement('div');
        card.className = 'bg-white rounded-2xl border border-emerald-100 shadow-sm hover:shadow-md transition flex flex-col justify-between overflow-hidden';
        card.innerHTML = `
            ${rec.image_url ? `
                <div class="h-40 w-full relative overflow-hidden bg-slate-100">
                    <img src="${rec.image_url}" alt="${rec.title}" referrerpolicy="no-referrer" onerror="this.parentElement.style.display='none'" class="w-full h-full object-cover">
                    <span class="nutriscore-badge nutriscore-${ns} text-xs w-7 h-7 absolute top-3 left-3 shadow">${ns}</span>
                    <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-600 text-white backdrop-blur-sm absolute bottom-3 right-3 shadow">
                        Objetivo Cumplido ✨
                    </span>
                </div>
            ` : ''}
            <div class="p-6 space-y-3 flex-1 flex flex-col justify-between">
                <div class="space-y-3">
                    ${!rec.image_url ? `
                        <div class="flex items-center justify-between">
                            <span class="nutriscore-badge nutriscore-${ns} text-xs w-7 h-7">${ns}</span>
                            <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
                                Objetivo Cumplido ✨
                            </span>
                        </div>
                    ` : ''}
                    <h3 class="text-base font-bold text-slate-800 line-clamp-1">${rec.title}</h3>
                    <p class="text-xs text-slate-600 line-clamp-2">${rec.description}</p>
                
                <div class="grid grid-cols-4 gap-1.5 text-center pt-2 border-t border-slate-100 text-xs">
                    <div class="bg-emerald-50 p-1.5 rounded-xl font-bold text-emerald-800">${ps.calories?.toFixed(0) || 0} <span class="block text-[9px] font-normal text-slate-400">kcal</span></div>
                    <div class="bg-blue-50 p-1.5 rounded-xl font-bold text-blue-800">${ps.protein?.toFixed(0) || 0}g <span class="block text-[9px] font-normal text-slate-400">prot</span></div>
                    <div class="bg-amber-50 p-1.5 rounded-xl font-bold text-amber-800">${ps.carbohydrates?.toFixed(0) || 0}g <span class="block text-[9px] font-normal text-slate-400">carb</span></div>
                    <div class="bg-rose-50 p-1.5 rounded-xl font-bold text-rose-800">${ps.fats?.toFixed(0) || 0}g <span class="block text-[9px] font-normal text-slate-400">grasa</span></div>
                </div>

                <div class="space-y-1 pt-1">
                    <span class="text-[11px] font-bold text-slate-700 block">Ingredientes principales:</span>
                    <p class="text-xs text-slate-500 line-clamp-2">${(rec.ingredients || []).map(i => `${i.name} (${i.amount})`).join(', ')}</p>
                </div>
            </div>

            <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                <button onclick="inspectSuggestion(${idx})" class="text-xs font-bold text-emerald-600 hover:text-emerald-700 flex items-center space-x-1">
                    <i data-lucide="eye" class="w-3.5 h-3.5"></i>
                    <span>Ver Receta Completa</span>
                </button>
                <button onclick="saveSuggestedRecipe(${idx})" class="px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-sm transition">
                    Guardar
                </button>
            </div>
        `;
        grid.appendChild(card);
    });

    window._latestSuggestions = suggestions;
    safeCreateIcons();
}

function inspectSuggestion(idx) {
    if (window._latestSuggestions && window._latestSuggestions[idx]) {
        currentAnalysisRecipe = window._latestSuggestions[idx];
        renderAnalysisResults(currentAnalysisRecipe);
        switchTab('analyzer');
    }
}

async function saveSuggestedRecipe(idx) {
    if (window._latestSuggestions && window._latestSuggestions[idx]) {
        try {
            const resp = await fetch('/api/recipes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(window._latestSuggestions[idx])
            });
            if (resp.ok) {
                alert('¡Receta sugerida guardada en Mi Recetario!');
                await loadRecipes();
            }
        } catch (e) {
            alert('Error guardando receta sugerida');
        }
    }
}

// ==========================================
// SAMPLES & CONFIG
// ==========================================
function loadSampleRecipeText() {
    document.getElementById('recipe-text-input').value = `Pollo con Brócoli y Arroz Integral al Estilo Asiático
Ingredientes:
- 250g de pechuga de pollo cortada en tiras
- 200g de brócoli fresco al vapor
- 120g de arroz integral cocido
- 1 cucharada sopera de salsa de soja baja en sal
- 1 cucharadita de aceite de sésamo
- 1 diente de ajo y pizca de jengibre fresco rallado

Preparación:
1. Dorar el pollo con el aceite de sésamo y el ajo picado durante 6 minutos.
2. Incorporar los ramilletes de brócoli y saltear a fuego fuerte durante 3 minutos.
3. Añadir la salsa de soja y servir caliente acompañado del arroz integral.`;
}

function loadSampleSocialUrl() {
    document.getElementById('social-url-input').value = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';
}

async function checkApiConfig() {
    try {
        const resp = await fetch('/api/config');
        if (resp.ok) {
            const data = await resp.json();
            const ind = document.getElementById('api-status-indicator');
            const txt = document.getElementById('api-status-text');
            if (data.has_api_key) {
                ind.className = 'w-2.5 h-2.5 rounded-full bg-emerald-500';
                txt.textContent = `Gemini IA Activo`;
            } else {
                ind.className = 'w-2.5 h-2.5 rounded-full bg-amber-400';
                txt.textContent = `Modo Demo (Sin Key)`;
            }
        }
    } catch (e) {
        console.error('Error comprobando config:', e);
    }
}

function openConfigModal() {
    document.getElementById('config-modal').classList.remove('hidden');
    safeCreateIcons();
}

function closeConfigModal() {
    document.getElementById('config-modal').classList.add('hidden');
}

async function saveApiKey() {
    const key = document.getElementById('input-gemini-key').value.trim();
    if (!key) {
        alert('Por favor, ingresa una clave de API válida.');
        return;
    }
    try {
        const resp = await fetch('/api/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ api_key: key })
        });
        if (resp.ok) {
            alert('¡Clave de Gemini API configurada con éxito!');
            closeConfigModal();
            checkApiConfig();
        } else {
            alert('Error guardando la clave.');
        }
    } catch (e) {
        alert('Error conectando con el servidor');
    }
}

// ==========================================
// MIS ALIMENTOS (CUSTOM PANTRY FOODS)
// ==========================================
async function loadCustomFoods() {
    try {
        const resp = await fetch('/api/foods');
        if (resp.ok) {
            savedCustomFoods = await resp.json();
            updateFoodCategoryCounts();
            renderCustomFoodsGrid();
            renderPantryQuickBadges();
        }
    } catch (e) {
        console.error('Error cargando alimentos personalizados:', e);
    }
}

function updateFoodCategoryCounts() {
    const counts = { all: savedCustomFoods.length, proteina: 0, carbohidrato: 0, verdura: 0, lacteo: 0, grasa: 0, despensa: 0 };
    savedCustomFoods.forEach(f => {
        const cat = (f.category || 'despensa').toLowerCase();
        if (counts[cat] !== undefined) {
            counts[cat]++;
        } else {
            counts.despensa++;
        }
    });

    ['all', 'proteina', 'carbohidrato', 'verdura', 'lacteo', 'grasa'].forEach(cat => {
        const el = document.getElementById(`count-foods-${cat}`);
        if (el) el.textContent = counts[cat] || 0;
    });
}

function setFoodCategoryFilter(cat) {
    currentFoodCategoryFilter = cat;
    document.querySelectorAll('.food-cat-btn').forEach(btn => {
        const btnCat = btn.getAttribute('data-cat');
        if (btnCat === cat) {
            btn.className = 'food-cat-btn px-3.5 py-1.5 rounded-xl text-xs font-bold transition bg-emerald-600 text-white shadow-sm flex-shrink-0';
        } else {
            btn.className = 'food-cat-btn px-3.5 py-1.5 rounded-xl text-xs font-bold transition bg-slate-100 text-slate-700 hover:bg-slate-200 flex-shrink-0';
        }
    });
    filterFoodsGrid();
}

function filterFoodsGrid() {
    const query = (document.getElementById('food-search-input')?.value || '').toLowerCase().trim();
    const filtered = savedCustomFoods.filter(f => {
        const matchesCat = currentFoodCategoryFilter === 'all' || (f.category || '').toLowerCase() === currentFoodCategoryFilter;
        const matchesQuery = !query || 
            (f.name || '').toLowerCase().includes(query) || 
            (f.brand || '').toLowerCase().includes(query) ||
            (f.notes || '').toLowerCase().includes(query);
        return matchesCat && matchesQuery;
    });
    renderCustomFoodsGrid(filtered);
}

function renderCustomFoodsGrid(foodsToRender = null) {
    const grid = document.getElementById('custom-foods-grid');
    if (!grid) return;
    grid.innerHTML = '';

    const list = foodsToRender !== null ? foodsToRender : savedCustomFoods;

    if (!list || list.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full text-center py-12 bg-white rounded-2xl border border-dashed border-slate-200">
                <div class="w-12 h-12 mx-auto rounded-full bg-amber-50 flex items-center justify-center text-amber-600 mb-3">
                    <i data-lucide="package-open" class="w-6 h-6"></i>
                </div>
                <h4 class="text-sm font-bold text-slate-800">No hay alimentos registrados en esta categoría</h4>
                <p class="text-xs text-slate-500 mt-1 mb-4">Añade los alimentos y marcas que sueles comprar para usarlos en recetas inteligentes.</p>
                <button onclick="openAddFoodModal()" class="px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white text-xs font-bold shadow-sm transition inline-flex items-center space-x-1.5">
                    <i data-lucide="plus" class="w-4 h-4"></i>
                    <span>Añadir Primer Alimento</span>
                </button>
            </div>
        `;
        safeCreateIcons();
        return;
    }

    list.forEach(f => {
        const catMeta = FOOD_CATEGORY_META[f.category] || { label: 'Despensa', icon: '🥫', color: 'bg-slate-100 text-slate-700 border-slate-200' };
        const card = document.createElement('div');
        card.className = 'bg-white rounded-2xl p-5 border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between space-y-3';
        
        const carbsVal = f.carbohydrates !== undefined ? f.carbohydrates : (f.carbs || 0);
        const fatsVal = f.fats !== undefined ? f.fats : (f.fat || 0);

        card.innerHTML = `
            <div class="space-y-2">
                <div class="flex items-center justify-between">
                    <span class="inline-flex items-center space-x-1 text-[11px] font-bold px-2 py-0.5 rounded-full border ${catMeta.color}">
                        <span>${catMeta.icon}</span>
                        <span>${catMeta.label}</span>
                    </span>
                    <span class="text-[11px] font-semibold text-slate-400">Por ${f.serving_size_g || 100}g</span>
                </div>
                <div>
                    <h3 class="text-sm font-bold text-slate-800 line-clamp-1">${f.name}</h3>
                    ${f.brand ? `<p class="text-xs text-slate-400 line-clamp-1">${f.brand}</p>` : '<p class="text-xs text-slate-300">Sin marca específica</p>'}
                </div>
                
                <div class="grid grid-cols-4 gap-1 text-center pt-2 border-t border-slate-100 text-xs">
                    <div class="bg-emerald-50 p-1.5 rounded-xl font-bold text-emerald-800">
                        ${(f.calories || 0).toFixed(0)} <span class="block text-[9px] font-normal text-slate-400">kcal</span>
                    </div>
                    <div class="bg-blue-50 p-1.5 rounded-xl font-bold text-blue-800">
                        ${(f.protein || 0).toFixed(1)}g <span class="block text-[9px] font-normal text-slate-400">prot</span>
                    </div>
                    <div class="bg-amber-50 p-1.5 rounded-xl font-bold text-amber-800">
                        ${carbsVal.toFixed(1)}g <span class="block text-[9px] font-normal text-slate-400">carb</span>
                    </div>
                    <div class="bg-rose-50 p-1.5 rounded-xl font-bold text-rose-800">
                        ${fatsVal.toFixed(1)}g <span class="block text-[9px] font-normal text-slate-400">grasa</span>
                    </div>
                </div>

                ${f.notes ? `<p class="text-[11px] text-slate-500 italic line-clamp-1 pt-1">💡 ${f.notes}</p>` : ''}
            </div>

            <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
                <button onclick="useFoodInPantry('${f.id}')" class="px-2.5 py-1.5 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-700 text-xs font-bold transition flex items-center space-x-1" title="Añadir a la nevera para cocinar">
                    <i data-lucide="cooking-pot" class="w-3.5 h-3.5"></i>
                    <span>Cocinar</span>
                </button>
                <div class="flex items-center space-x-1">
                    <button onclick="editFood('${f.id}')" class="p-1.5 rounded-lg hover:bg-slate-100 text-slate-500 hover:text-slate-800 transition" title="Editar alimento">
                        <i data-lucide="pencil" class="w-3.5 h-3.5"></i>
                    </button>
                    <button onclick="deleteCustomFood('${f.id}')" class="p-1.5 rounded-lg hover:bg-rose-50 text-slate-400 hover:text-rose-600 transition" title="Eliminar de la despensa">
                        <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                    </button>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });

    safeCreateIcons();
}

function openAddFoodModal(foodData = null) {
    const modal = document.getElementById('food-modal');
    const titleEl = document.getElementById('food-modal-title');
    
    if (foodData) {
        if (titleEl) titleEl.textContent = 'Editar Alimento';
        document.getElementById('food-form-id').value = foodData.id || '';
        document.getElementById('food-form-name').value = foodData.name || '';
        document.getElementById('food-form-brand').value = foodData.brand || '';
        document.getElementById('food-form-category').value = foodData.category || 'proteina';
        document.getElementById('food-form-calories').value = foodData.calories ?? '';
        document.getElementById('food-form-protein').value = foodData.protein ?? '';
        document.getElementById('food-form-carbs').value = (foodData.carbohydrates ?? foodData.carbs) ?? '';
        document.getElementById('food-form-fats').value = (foodData.fats ?? foodData.fat) ?? '';
        document.getElementById('food-form-fiber').value = foodData.fiber ?? 0;
        document.getElementById('food-form-serving').value = foodData.serving_size_g || 100;
        document.getElementById('food-form-notes').value = foodData.notes || '';
    } else {
        if (titleEl) titleEl.textContent = 'Añadir Alimento a mi Despensa';
        document.getElementById('food-form-id').value = '';
        document.getElementById('food-form-name').value = '';
        document.getElementById('food-form-brand').value = '';
        document.getElementById('food-form-category').value = 'proteina';
        document.getElementById('food-form-calories').value = '';
        document.getElementById('food-form-protein').value = '';
        document.getElementById('food-form-carbs').value = '';
        document.getElementById('food-form-fats').value = '';
        document.getElementById('food-form-fiber').value = '';
        document.getElementById('food-form-serving').value = '100';
        document.getElementById('food-form-notes').value = '';
    }

    modal.classList.remove('hidden');
    safeCreateIcons();
}

function closeFoodModal() {
    const modal = document.getElementById('food-modal');
    if (modal) modal.classList.add('hidden');
}

function editFood(foodId) {
    const food = savedCustomFoods.find(f => f.id === foodId);
    if (food) {
        openAddFoodModal(food);
    }
}

async function autoEstimateFoodWithAi() {
    const name = document.getElementById('food-form-name').value.trim();
    const brand = document.getElementById('food-form-brand').value.trim();
    const btn = document.getElementById('btn-estimate-ai');

    if (!name) {
        alert('Escribe primero el nombre del alimento (ej: Pechuga de pavo, Queso cottage, Avena...) para que la IA pueda calcularlo.');
        return;
    }

    const originalBtnHtml = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = `<div class="w-3.5 h-3.5 rounded-full border-2 border-emerald-500 border-t-transparent animate-spin"></div><span>Calculando...</span>`;

    try {
        const resp = await fetch('/api/foods/estimate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name, brand: brand || null })
        });

        if (!resp.ok) {
            throw new Error('No se pudo estimar el alimento con IA');
        }

        const est = await resp.json();
        document.getElementById('food-form-category').value = est.category || 'despensa';
        document.getElementById('food-form-calories').value = est.calories ?? 0;
        document.getElementById('food-form-protein').value = est.protein ?? 0;
        document.getElementById('food-form-carbs').value = est.carbohydrates ?? 0;
        document.getElementById('food-form-fats').value = est.fats ?? 0;
        document.getElementById('food-form-fiber').value = est.fiber ?? 0;
        document.getElementById('food-form-serving').value = est.serving_size_g || 100;
        if (est.notes && !document.getElementById('food-form-notes').value) {
            document.getElementById('food-form-notes').value = est.notes;
        }
    } catch (e) {
        alert(e.message || 'Error calculando nutrientes');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalBtnHtml;
        safeCreateIcons();
    }
}

async function submitFoodForm() {
    const name = document.getElementById('food-form-name').value.trim();
    if (!name) {
        alert('Por favor, introduce el nombre del alimento.');
        return;
    }

    const payload = {
        id: document.getElementById('food-form-id').value || null,
        name: name,
        brand: document.getElementById('food-form-brand').value.trim() || null,
        category: document.getElementById('food-form-category').value || 'despensa',
        calories: parseFloat(document.getElementById('food-form-calories').value) || 0.0,
        protein: parseFloat(document.getElementById('food-form-protein').value) || 0.0,
        carbohydrates: parseFloat(document.getElementById('food-form-carbs').value) || 0.0,
        fats: parseFloat(document.getElementById('food-form-fats').value) || 0.0,
        fiber: parseFloat(document.getElementById('food-form-fiber').value) || 0.0,
        serving_size_g: parseFloat(document.getElementById('food-form-serving').value) || 100.0,
        notes: document.getElementById('food-form-notes').value.trim() || null
    };

    try {
        const resp = await fetch('/api/foods', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!resp.ok) {
            throw new Error('Error al guardar el alimento.');
        }

        closeFoodModal();
        await loadCustomFoods();
    } catch (e) {
        alert(e.message);
    }
}

async function deleteCustomFood(foodId) {
    if (!confirm('¿Seguro que deseas eliminar este alimento de tu despensa?')) {
        return;
    }

    try {
        const resp = await fetch(`/api/foods/${foodId}`, {
            method: 'DELETE'
        });

        if (!resp.ok) {
            throw new Error('No se pudo eliminar el alimento.');
        }

        await loadCustomFoods();
    } catch (e) {
        alert(e.message);
    }
}

// ==========================================
// ¿QUÉ COCINO HOY? (PANTRY AI ENGINE CON CANTIDADES)
// ==========================================
let pantryItems = []; // List of { id, name, amount, unit, icon }

function loadPantryTab() {
    renderPantryQuickBadges();
    renderPantryItemsList();
}

function renderPantryQuickBadges() {
    const container = document.getElementById('pantry-quick-badges');
    if (!container) return;
    container.innerHTML = '';

    if (!savedCustomFoods || savedCustomFoods.length === 0) {
        container.innerHTML = `<span class="text-[11px] text-slate-400">Aún no has guardado alimentos en 'Mis Alimentos'.</span>`;
        return;
    }

    savedCustomFoods.forEach(f => {
        const catMeta = FOOD_CATEGORY_META[f.category] || { icon: '🥫' };
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 hover:bg-emerald-100 hover:text-emerald-800 text-slate-700 transition flex items-center space-x-1 flex-shrink-0';
        btn.onclick = () => addPantryFoodTag(f.name);
        btn.innerHTML = `<span>${catMeta.icon}</span> <span>${f.name}</span> <span class="text-[10px] text-slate-400 font-semibold">+</span>`;
        container.appendChild(btn);
    });
}

function addPantryFoodTag(foodName) {
    const food = savedCustomFoods.find(f => f.name.toLowerCase() === foodName.toLowerCase());
    const lower = foodName.toLowerCase();

    let defaultAmount = 100;
    let defaultUnit = 'g';
    let icon = (food && FOOD_CATEGORY_META[food.category]?.icon) || '🥗';

    if (lower.includes('huevo')) {
        defaultAmount = 2;
        defaultUnit = 'unidad(es)';
        icon = '🥚';
    } else if (lower.includes('atún') || lower.includes('atun') || lower.includes('lata')) {
        defaultAmount = 1;
        defaultUnit = 'lata(s)';
        icon = '🥫';
    } else if (lower.includes('aceite') || lower.includes('aove')) {
        defaultAmount = 1;
        defaultUnit = 'cucharada(s)';
        icon = '🫒';
    } else if (lower.includes('pan') || lower.includes('rebanada')) {
        defaultAmount = 2;
        defaultUnit = 'rebanada(s)';
        icon = '🍞';
    } else if (food && food.serving_size_g) {
        defaultAmount = food.serving_size_g;
        defaultUnit = 'g';
    }

    addPantryItem(foodName, defaultAmount, defaultUnit, icon);
}

function addManualPantryItem() {
    const nameInput = document.getElementById('pantry-manual-name');
    const amountInput = document.getElementById('pantry-manual-amount');
    const unitInput = document.getElementById('pantry-manual-unit');

    const name = (nameInput?.value || '').trim();
    if (!name) {
        alert('Escribe el nombre del ingrediente (ej: Huevos, Pechuga, Cebolla...).');
        nameInput?.focus();
        return;
    }

    const amount = parseFloat(amountInput?.value) || 100;
    const unit = unitInput?.value || 'g';

    let icon = '🥗';
    const lower = name.toLowerCase();
    if (lower.includes('pollo') || lower.includes('carne') || lower.includes('ternera') || lower.includes('pavo')) icon = '🥩';
    else if (lower.includes('pescado') || lower.includes('salmon') || lower.includes('merluza') || lower.includes('atun')) icon = '🐟';
    else if (lower.includes('huevo')) icon = '🥚';
    else if (lower.includes('arroz') || lower.includes('pasta') || lower.includes('avena')) icon = '🍚';
    else if (lower.includes('leche') || lower.includes('yogur') || lower.includes('queso')) icon = '🥛';
    else if (lower.includes('tomate') || lower.includes('calabacin') || lower.includes('cebolla') || lower.includes('espinaca')) icon = '🥦';
    else if (lower.includes('fruta') || lower.includes('platano') || lower.includes('manzana')) icon = '🍎';

    addPantryItem(name, amount, unit, icon);
    nameInput.value = '';
    nameInput.focus();
}

function addPantryItem(name, amount = 100, unit = 'g', icon = '🥗') {
    const existing = pantryItems.find(i => i.name.toLowerCase() === name.toLowerCase());
    if (existing) {
        existing.amount += amount;
    } else {
        pantryItems.push({
            id: 'item_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
            name: name,
            amount: amount,
            unit: unit,
            icon: icon
        });
    }
    renderPantryItemsList();
}

function renderPantryItemsList() {
    const container = document.getElementById('pantry-items-list-container');
    const badge = document.getElementById('pantry-items-count-badge');
    const clearBtn = document.getElementById('btn-clear-pantry');

    if (badge) {
        const count = pantryItems.length;
        badge.textContent = `${count} ${count === 1 ? 'ingrediente' : 'ingredientes'}`;
        badge.className = count > 0 
            ? 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800' 
            : 'px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-600';
    }

    if (clearBtn) {
        clearBtn.classList.toggle('hidden', pantryItems.length === 0);
    }

    if (!container) return;
    container.innerHTML = '';

    if (pantryItems.length === 0) {
        container.innerHTML = `
            <div class="py-5 px-4 text-center rounded-2xl border border-dashed border-slate-200 bg-slate-50/50">
                <p class="text-xs text-slate-400">Tu cesta está vacía. Añade ingredientes arriba con sus cantidades para que la IA diseñe tu receta.</p>
            </div>
        `;
        safeCreateIcons();
        return;
    }

    pantryItems.forEach(item => {
        const row = document.createElement('div');
        row.className = 'bg-white rounded-xl p-3 border border-slate-200/90 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:border-emerald-200 transition';
        row.innerHTML = `
            <div class="flex items-center space-x-2.5">
                <span class="text-lg flex-shrink-0">${item.icon}</span>
                <div>
                    <span class="text-xs font-bold text-slate-800 block">${item.name}</span>
                    <span class="text-[10px] text-slate-400">Cantidad para cocinar</span>
                </div>
            </div>
            <div class="flex items-center space-x-1.5 self-end sm:self-auto">
                <button type="button" onclick="adjustPantryItemAmount('${item.id}', -1)" class="w-7 h-7 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs flex items-center justify-center transition" title="Reducir">-</button>
                <input type="number" step="any" min="1" value="${item.amount}" onchange="setPantryItemAmount('${item.id}', this.value)" class="w-16 px-2 py-1 text-center rounded-lg border border-slate-200 text-xs font-bold text-emerald-800 focus:ring-1 focus:ring-emerald-500 outline-none">
                <select onchange="setPantryItemUnit('${item.id}', this.value)" class="px-2 py-1 rounded-lg border border-slate-200 text-xs font-medium text-slate-600 bg-white outline-none">
                    <option value="g" ${item.unit === 'g' ? 'selected' : ''}>g</option>
                    <option value="unidad(es)" ${item.unit.includes('unidad') ? 'selected' : ''}>ud(s)</option>
                    <option value="ml" ${item.unit === 'ml' ? 'selected' : ''}>ml</option>
                    <option value="lata(s)" ${item.unit.includes('lata') ? 'selected' : ''}>lata(s)</option>
                    <option value="cucharada(s)" ${item.unit.includes('cucharad') ? 'selected' : ''}>cucharada(s)</option>
                    <option value="rebanada(s)" ${item.unit.includes('rebanad') ? 'selected' : ''}>rebanada(s)</option>
                    <option value="puñado(s)" ${item.unit.includes('puñad') ? 'selected' : ''}>puñado(s)</option>
                    <option value="al gusto" ${item.unit.includes('gusto') ? 'selected' : ''}>al gusto</option>
                </select>
                <button type="button" onclick="adjustPantryItemAmount('${item.id}', 1)" class="w-7 h-7 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs flex items-center justify-center transition" title="Aumentar">+</button>
                <button type="button" onclick="removePantryItem('${item.id}')" class="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition ml-1" title="Quitar ingrediente">
                    <i data-lucide="trash-2" class="w-4 h-4"></i>
                </button>
            </div>
        `;
        container.appendChild(row);
    });

    safeCreateIcons();
}

function adjustPantryItemAmount(id, delta) {
    const item = pantryItems.find(i => i.id === id);
    if (!item) return;

    let step = 1;
    if (item.unit === 'g' || item.unit === 'ml') {
        step = item.amount <= 50 && delta < 0 ? 10 : 50;
    } else if (item.unit === 'al gusto') {
        return;
    }

    item.amount = Math.max(1, (item.amount || 0) + delta * step);
    renderPantryItemsList();
}

function setPantryItemAmount(id, val) {
    const item = pantryItems.find(i => i.id === id);
    if (item) {
        item.amount = Math.max(1, parseFloat(val) || 1);
    }
}

function setPantryItemUnit(id, unit) {
    const item = pantryItems.find(i => i.id === id);
    if (item) {
        item.unit = unit;
    }
}

function removePantryItem(id) {
    pantryItems = pantryItems.filter(i => i.id !== id);
    renderPantryItemsList();
}

function clearPantryItems() {
    pantryItems = [];
    renderPantryItemsList();
}

function useFoodInPantry(foodId) {
    const food = savedCustomFoods.find(f => f.id === foodId);
    if (food) {
        addPantryFoodTag(food.name);
        switchTab('pantry');
        document.getElementById('pantry-items-list-container')?.scrollIntoView({ behavior: 'smooth' });
    }
}

async function generateRecipesFromPantry() {
    const loading = document.getElementById('pantry-loading');
    const grid = document.getElementById('pantry-results-grid');
    const btn = document.getElementById('btn-generate-pantry');

    // Construir lista de ingredientes con cantidades exactas
    const parts = [];
    pantryItems.forEach(item => {
        if (item.unit === 'al gusto') {
            parts.push(`${item.name} al gusto`);
        } else {
            parts.push(`${item.amount} ${item.unit} de ${item.name}`);
        }
    });

    const extraNotes = (document.getElementById('pantry-ingredients-input')?.value || '').trim();
    if (extraNotes) {
        parts.push(extraNotes);
    }

    const ingredientsText = parts.join(', ');

    if (!ingredientsText) {
        alert('Por favor, añade al menos un ingrediente con su cantidad disponible.');
        document.getElementById('pantry-manual-name')?.focus();
        return;
    }

    loading.classList.remove('hidden');
    grid.innerHTML = '';
    btn.disabled = true;

    const payload = {
        ingredients: ingredientsText,
        meal_type: document.getElementById('pantry-meal-type').value,
        cooking_time: document.getElementById('pantry-cooking-time').value,
        dietary_preference: document.getElementById('pantry-diet-style').value,
        servings: parseInt(document.getElementById('pantry-servings').value) || 2,
        selected_pantry_foods: pantryItems.map(i => i.name)
    };

    try {
        const resp = await fetch('/api/suggest/pantry', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!resp.ok) {
            let errorMsg = 'Error diseñando recetas de despensa';
            try {
                const err = await resp.json();
                errorMsg = err.detail || errorMsg;
            } catch (_) {
                const text = await resp.text();
                errorMsg = text || errorMsg;
            }
            throw new Error(errorMsg);
        }

        const data = await resp.json();
        renderPantryResults(data.suggestions || []);
    } catch (e) {
        alert(e.message);
    } finally {
        loading.classList.add('hidden');
        btn.disabled = false;
        safeCreateIcons();
    }
}

function renderPantryResults(suggestions) {
    const grid = document.getElementById('pantry-results-grid');
    grid.innerHTML = '';

    if (!suggestions || suggestions.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full text-center py-12 bg-white rounded-2xl border border-dashed border-slate-200">
                <p class="text-xs text-slate-400">No se pudieron generar recetas con los ingredientes indicados. Prueba añadiendo más opciones comunes como huevos o arroz.</p>
            </div>
        `;
        return;
    }

    suggestions.forEach((rec, idx) => {
        const ps = rec.per_serving || {};
        const ns = (rec.nutri_score || 'A').toUpperCase();
        const catMeta = CATEGORY_META[rec.category] || { label: 'Comida', icon: '🍽️', color: 'bg-teal-100 text-teal-800 border-teal-200' };

        const card = document.createElement('div');
        card.className = 'bg-white rounded-3xl border border-emerald-100 shadow-sm hover:shadow-md transition flex flex-col justify-between overflow-hidden';
        card.innerHTML = `
            ${rec.image_url ? `
                <div class="h-44 w-full relative overflow-hidden bg-slate-100">
                    <img src="${rec.image_url}" alt="${rec.title}" referrerpolicy="no-referrer" onerror="this.parentElement.style.display='none'" class="w-full h-full object-cover">
                    <span class="nutriscore-badge nutriscore-${ns} text-xs w-7 h-7 absolute top-3 left-3 shadow">${ns}</span>
                    <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-600 text-white backdrop-blur-sm absolute bottom-3 right-3 shadow">
                        🍳 Cocina de Casa
                    </span>
                </div>
            ` : ''}
            <div class="p-6 space-y-3 flex-1 flex flex-col justify-between">
                <div class="space-y-3">
                    <div class="flex items-center justify-between gap-2">
                        <span class="px-2.5 py-0.5 rounded-full text-xs font-bold border ${catMeta.color} inline-flex items-center space-x-1">
                            <span>${catMeta.icon}</span>
                            <span>${catMeta.label}</span>
                        </span>
                        <span class="text-xs font-semibold text-slate-500">⏱️ ${(rec.prep_time_minutes || 10) + (rec.cook_time_minutes || 15)} min</span>
                    </div>

                    <h3 class="text-base font-bold text-slate-800 line-clamp-1">${rec.title}</h3>
                    <p class="text-xs text-slate-600 line-clamp-2">${rec.description}</p>
                
                    <div class="grid grid-cols-4 gap-1.5 text-center pt-2 border-t border-slate-100 text-xs">
                        <div class="bg-emerald-50 p-1.5 rounded-xl font-bold text-emerald-800">${ps.calories?.toFixed(0) || 0} <span class="block text-[9px] font-normal text-slate-400">kcal</span></div>
                        <div class="bg-blue-50 p-1.5 rounded-xl font-bold text-blue-800">${ps.protein?.toFixed(0) || 0}g <span class="block text-[9px] font-normal text-slate-400">prot</span></div>
                        <div class="bg-amber-50 p-1.5 rounded-xl font-bold text-amber-800">${ps.carbohydrates?.toFixed(0) || 0}g <span class="block text-[9px] font-normal text-slate-400">carb</span></div>
                        <div class="bg-rose-50 p-1.5 rounded-xl font-bold text-rose-800">${ps.fats?.toFixed(0) || 0}g <span class="block text-[9px] font-normal text-slate-400">grasa</span></div>
                    </div>

                    <div class="space-y-1 pt-1">
                        <span class="text-[11px] font-bold text-slate-700 block">Ingredientes necesarios:</span>
                        <p class="text-xs text-slate-500 line-clamp-2">${(rec.ingredients || []).map(i => `${i.name} (${i.amount})`).join(', ')}</p>
                    </div>
                </div>

                <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
                    <button onclick="inspectPantrySuggestion(${idx})" class="text-xs font-bold text-emerald-600 hover:text-emerald-700 flex items-center space-x-1">
                        <i data-lucide="eye" class="w-3.5 h-3.5"></i>
                        <span>Ver Pasos & Macros</span>
                    </button>
                    <button onclick="savePantryRecipe(${idx})" class="px-3.5 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-sm transition">
                        Guardar en Recetario
                    </button>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });

    window._latestPantrySuggestions = suggestions;
    safeCreateIcons();
    grid.scrollIntoView({ behavior: 'smooth' });
}

function inspectPantrySuggestion(idx) {
    if (window._latestPantrySuggestions && window._latestPantrySuggestions[idx]) {
        currentAnalysisRecipe = window._latestPantrySuggestions[idx];
        renderAnalysisResults(currentAnalysisRecipe);
        switchTab('analyzer');
        document.getElementById('analysis-results')?.scrollIntoView({ behavior: 'smooth' });
    }
}

async function savePantryRecipe(idx) {
    if (window._latestPantrySuggestions && window._latestPantrySuggestions[idx]) {
        try {
            const resp = await fetch('/api/recipes', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(window._latestPantrySuggestions[idx])
            });
            if (resp.ok) {
                alert('¡Receta guardada en Mi Recetario!');
                await loadRecipes();
            }
        } catch (e) {
            alert('Error guardando la receta de despensa');
        }
    }
}

