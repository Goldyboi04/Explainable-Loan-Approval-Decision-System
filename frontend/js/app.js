const API_BASE_URL = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '/api';

// Navigation
document.getElementById('nav-new').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('view-new-application').style.display = 'block';
    document.getElementById('view-history').style.display = 'none';
    document.getElementById('nav-new').classList.add('active');
    document.getElementById('nav-history').classList.remove('active');
});

document.getElementById('nav-history').addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('view-history').style.display = 'block';
    document.getElementById('view-new-application').style.display = 'none';
    document.getElementById('nav-history').classList.add('active');
    document.getElementById('nav-new').classList.remove('active');
    fetchHistory();
});

// Form Submission
document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = document.getElementById('btn-predict');
    btn.disabled = true;
    btn.textContent = 'Analyzing...';

    const payload = {
        no_of_dependents: parseInt(document.getElementById('no_of_dependents').value),
        education: document.getElementById('education').value,
        self_employed: document.getElementById('self_employed').value,
        income_annum: parseFloat(document.getElementById('income_annum').value),
        loan_amount: parseFloat(document.getElementById('loan_amount').value),
        loan_term: parseInt(document.getElementById('loan_term').value),
        cibil_score: parseFloat(document.getElementById('cibil_score').value),
        residential_assets_value: parseFloat(document.getElementById('residential_assets_value').value),
        commercial_assets_value: parseFloat(document.getElementById('commercial_assets_value').value),
        luxury_assets_value: parseFloat(document.getElementById('luxury_assets_value').value),
        bank_asset_value: parseFloat(document.getElementById('bank_asset_value').value)
    };

    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('API request failed');
        const data = await response.json();

        displayResults(data);
    } catch (error) {
        alert("Failed to connect to API: " + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Analyze Risk';
    }
});

function displayResults(data) {
    const container = document.getElementById('results-container');
    container.style.display = 'flex';

    // Reset animations
    container.style.animation = 'none';
    container.offsetHeight; /* trigger reflow */
    container.style.animation = null;

    const probVal = Math.round(data.risk_probability * 100);
    document.getElementById('res-prob').textContent = `${probVal}%`;
    document.getElementById('res-prob').style.color = probVal > 40 ? 'var(--danger)' : 'var(--success)';

    const decBox = document.getElementById('decision-box');
    decBox.className = `decision-box ${probVal > 40 ? 'risk' : 'safe'}`;
    document.getElementById('res-decision').textContent = data.automated_decision_recommendation;
    document.getElementById('res-primary-factor').textContent = data.primary_decision_factor;

    const riskUL = document.getElementById('list-risk-signals');
    riskUL.innerHTML = '';
    data.risk_signals.forEach(sig => {
        const li = document.createElement('li');
        li.textContent = sig;
        riskUL.appendChild(li);
    });

    const posUL = document.getElementById('list-positive-indicators');
    posUL.innerHTML = '';
    data.positive_indicators.forEach(sig => {
        const li = document.createElement('li');
        li.textContent = sig;
        posUL.appendChild(li);
    });
}

async function fetchHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/predictions`);
        if (!response.ok) return;
        const records = await response.json();

        const tbody = document.getElementById('history-tbody');
        tbody.innerHTML = '';

        records.reverse().forEach(record => {
            const riskProb = Math.round(record.risk_probability * 100);
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>#${record.id}</td>
                <td>₹${record.income_annum.toLocaleString()}</td>
                <td>₹${record.loan_amount.toLocaleString()}</td>
                <td>${record.debt_to_income.toFixed(2)}</td>
                <td style="color: ${riskProb > 40 ? 'var(--danger)' : 'var(--success)'}; font-weight: bold;">
                    ${riskProb}%
                </td>
                <td>${record.automated_decision}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error("Failed to load history", e);
    }
}
