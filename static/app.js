/**
 * DrugSymptomFinder Frontend Logic
 * Handles interactive search, autocomplete, fuzzy match visualization, and responsive card rendering.
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const symptomInput = document.getElementById('symptomInput');
    const searchBtn = document.getElementById('searchBtn');
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    const autocompleteDropdown = document.getElementById('autocompleteDropdown');
    const presetButtons = document.querySelectorAll('.preset-btn');
    
    const resultsHeaderSection = document.getElementById('resultsHeaderSection');
    const resultsQueryTitle = document.getElementById('resultsQueryTitle');
    const activeQueryText = document.getElementById('activeQueryText');
    const resultsCountBadge = document.getElementById('resultsCountBadge');
    const minScoreFilter = document.getElementById('minScoreFilter');
    
    const loadingState = document.getElementById('loadingState');
    const emptyState = document.getElementById('emptyState');
    const emptyQueryText = document.getElementById('emptyQueryText');
    const resultsGrid = document.getElementById('resultsGrid');
    const statCount = document.getElementById('statCount');

    let autocompleteDebounceTimer = null;
    let currentResults = [];

    // Load initial stats
    fetchStats();

    // Event Listeners
    searchBtn.addEventListener('click', () => triggerSearch());
    
    symptomInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            hideAutocomplete();
            triggerSearch();
        }
    });

    symptomInput.addEventListener('input', (e) => {
        const val = e.target.value;
        if (val.trim()) {
            clearSearchBtn.classList.remove('hidden');
        } else {
            clearSearchBtn.classList.add('hidden');
            hideAutocomplete();
        }
        
        clearTimeout(autocompleteDebounceTimer);
        autocompleteDebounceTimer = setTimeout(() => {
            fetchAutocomplete(val);
        }, 200);
    });

    clearSearchBtn.addEventListener('click', () => {
        symptomInput.value = '';
        clearSearchBtn.classList.add('hidden');
        hideAutocomplete();
        symptomInput.focus();
    });

    presetButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const sym = btn.getAttribute('data-symptom');
            symptomInput.value = sym;
            clearSearchBtn.classList.remove('hidden');
            hideAutocomplete();
            triggerSearch(sym);
        });
    });

    minScoreFilter.addEventListener('change', () => {
        renderResults();
    });

    // Close autocomplete on outside click
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-box-wrapper')) {
            hideAutocomplete();
        }
    });

    // API Functions
    async function fetchStats() {
        try {
            const res = await fetch('/api/stats');
            if (res.ok) {
                const data = await res.json();
                if (data.total_approved_drugs && statCount) {
                    statCount.textContent = Number(data.total_approved_drugs).toLocaleString();
                }
            }
        } catch (err) {
            console.error('Failed to fetch stats:', err);
        }
    }

    async function fetchAutocomplete(query) {
        if (!query || query.trim().length < 1) {
            hideAutocomplete();
            return;
        }

        try {
            const res = await fetch(`/api/symptoms/autocomplete?q=${encodeURIComponent(query)}`);
            if (res.ok) {
                const data = await res.json();
                renderAutocomplete(data.suggestions || []);
            }
        } catch (err) {
            console.error('Autocomplete error:', err);
        }
    }

    function renderAutocomplete(items) {
        if (!items || items.length === 0) {
            hideAutocomplete();
            return;
        }

        autocompleteDropdown.innerHTML = items.map(item => `
            <div class="autocomplete-item" data-value="${escapeHtml(item)}">
                <i class="fa-solid fa-notes-medical"></i>
                <span>${highlightMatch(item, symptomInput.value)}</span>
            </div>
        `).join('');

        autocompleteDropdown.classList.remove('hidden');

        // Add click listeners to items
        autocompleteDropdown.querySelectorAll('.autocomplete-item').forEach(el => {
            el.addEventListener('click', () => {
                const val = el.getAttribute('data-value');
                symptomInput.value = val;
                clearSearchBtn.classList.remove('hidden');
                hideAutocomplete();
                triggerSearch(val);
            });
        });
    }

    function hideAutocomplete() {
        autocompleteDropdown.classList.add('hidden');
        autocompleteDropdown.innerHTML = '';
    }

    async function triggerSearch(overrideQuery = null) {
        const query = overrideQuery !== null ? overrideQuery : symptomInput.value.trim();
        if (!query) {
            symptomInput.focus();
            return;
        }

        // Reset & Show Loading
        showLoading();

        try {
            const res = await fetch('/api/search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    symptom: query,
                    min_score: 35.0, // fetch broader set, UI filter handles display cutoff
                    limit: 80
                })
            });

            if (!res.ok) {
                throw new Error(`Server returned HTTP ${res.status}`);
            }

            const data = await res.json();
            currentResults = data.results || [];
            hideLoading();
            
            activeQueryText.textContent = query;
            emptyQueryText.textContent = query;
            resultsHeaderSection.classList.remove('hidden');

            renderResults();
        } catch (err) {
            hideLoading();
            console.error('Search request error:', err);
            resultsGrid.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1;">
                    <div class="empty-icon-box" style="background: rgba(239,68,68,0.15); color: var(--danger);">
                        <i class="fa-solid fa-triangle-exclamation"></i>
                    </div>
                    <h3>Error Connecting to Server</h3>
                    <p>Unable to perform search. Please check backend connection.</p>
                </div>
            `;
        }
    }

    function renderResults() {
        const threshold = parseFloat(minScoreFilter.value) || 40.0;
        const filtered = currentResults.filter(item => item.confidence_score >= threshold);

        resultsCountBadge.textContent = `${filtered.length} Match${filtered.length === 1 ? '' : 'es'} Found`;

        if (filtered.length === 0) {
            resultsGrid.innerHTML = '';
            emptyState.classList.remove('hidden');
            return;
        }

        emptyState.classList.add('hidden');

        resultsGrid.innerHTML = filtered.map(drug => {
            const hasStrength = drug.strength && drug.strength.trim() !== '' && drug.strength.trim() !== 'nan';
            const isHighMatch = drug.confidence_score >= 70;

            return `
                <article class="drug-card">
                    <div class="card-header">
                        <h4 class="drug-title">${escapeHtml(drug.drug_name)}</h4>
                        <div class="match-badge ${isHighMatch ? 'high' : ''}">
                            <i class="fa-solid ${isHighMatch ? 'fa-circle-check' : 'fa-bullseye'}"></i>
                            ${drug.confidence_score}% Match
                        </div>
                    </div>

                    <!-- Confidence Bar Meter -->
                    <div class="confidence-wrapper">
                        <div class="confidence-bar-bg">
                            <div class="confidence-bar-fill" style="width: ${Math.min(100, Math.max(10, drug.confidence_score))}%;"></div>
                        </div>
                        <div class="confidence-label">
                            <span>Relevance Match Score</span>
                            <span>${drug.confidence_score}/100</span>
                        </div>
                    </div>

                    <!-- Strength Info -->
                    <div class="strength-tag ${hasStrength ? '' : 'empty'}">
                        <i class="fa-solid fa-pills"></i> 
                        ${hasStrength 
                            ? `<strong>Strength/Form:</strong> ${escapeHtml(drug.strength)}` 
                            : `Strength: <em>Not specified in source CDSCO record</em>`}
                    </div>

                    <!-- Indication Clinical Description -->
                    <div class="indication-box">
                        <div class="indication-label">
                            <i class="fa-solid fa-file-medical"></i> Approved Clinical Indication
                        </div>
                        <p class="indication-text">${escapeHtml(drug.indication)}</p>
                    </div>

                    <!-- Footer Metadata -->
                    <div class="card-footer-meta">
                        <div class="approval-date">
                            <i class="fa-regular fa-calendar-check"></i>
                            <span>Approval: <strong>${escapeHtml(drug.date_of_approval || 'N/A')}</strong></span>
                        </div>
                        <div class="sr-tag">Ref #${drug.sr_no}</div>
                    </div>
                </article>
            `;
        }).join('');
    }

    // Helper functions
    function showLoading() {
        loadingState.classList.remove('hidden');
        emptyState.classList.add('hidden');
        resultsHeaderSection.classList.add('hidden');
        resultsGrid.innerHTML = '';
    }

    function hideLoading() {
        loadingState.classList.add('hidden');
    }

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    function highlightMatch(text, query) {
        if (!query) return escapeHtml(text);
        const qEsc = escapeHtml(query);
        const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        return escapeHtml(text).replace(regex, '<strong>$1</strong>');
    }
});
