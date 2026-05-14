let trafficChart;

// 1. Live Clock
setInterval(() => {
    document.getElementById('live-clock').innerText =
        new Date().toLocaleTimeString('en-US', { hour12: false });
}, 1000);

// 2. Animated Counters Function
function animateValue(id, end, duration, unit = "") {
    const obj = document.getElementById(id);
    const start = parseInt(obj.innerText.replace(/\D/g, '')) || 0;

    if (start === end) return;

    let startTimestamp = null;

    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;

        const progress = Math.min(
            (timestamp - startTimestamp) / duration,
            1
        );

        obj.innerHTML =
            Math.floor(progress * (end - start) + start) + unit;

        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };

    window.requestAnimationFrame(step);
}

// 3. Initialize Chart.js
function initChart() {
    const ctx = document.getElementById('trafficChart').getContext('2d');

    // Gradient fill for the chart
    let gradient = ctx.createLinearGradient(0, 0, 0, 400);

    gradient.addColorStop(0, 'rgba(56, 189, 248, 0.4)');
    gradient.addColorStop(1, 'rgba(56, 189, 248, 0.0)');

    trafficChart = new Chart(ctx, {
        type: 'line',

        data: {
            labels: [],

            datasets: [{
                label: 'Global Congestion %',
                data: [],
                borderColor: '#38bdf8',
                backgroundColor: gradient,
                borderWidth: 2,
                pointBackgroundColor: '#0f172a',
                pointBorderColor: '#38bdf8',
                pointRadius: 4,
                fill: true,
                tension: 0.4
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,

                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },

                    ticks: {
                        color: '#94a3b8'
                    }
                },

                x: {
                    grid: {
                        display: false
                    },

                    ticks: {
                        color: '#94a3b8'
                    }
                }
            },

            plugins: {
                legend: {
                    display: false
                },

                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },

            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// 4. Update Chart Data
function updateChart(data) {
    const labels = data.map(d => d.timestamp).reverse();
    const values = data.map(d => d.congestion).reverse();

    trafficChart.data.labels = labels;
    trafficChart.data.datasets[0].data = values;

    trafficChart.update('none');
}

// 5. Main Dashboard Update Logic
async function updateDashboard() {

    try {

        const response = await fetch('/api/traffic');
        const data = await response.json();

        // Update KPIs
        animateValue('stat-roads', data.stats.total_roads, 800);

        animateValue(
            'stat-avg',
            data.stats.avg_congestion,
            800,
            '%'
        );

        animateValue(
            'stat-critical',
            data.stats.critical_zones,
            800
        );

        // Update Infra Metrics
        document.getElementById('infra-latency').innerText =
            data.infra.api_latency;

        // Update Table
        const tbody =
            document.querySelector('#traffic-table tbody');

        tbody.innerHTML = '';

        data.traffic_data.forEach(row => {

            let statusClass = 'text-green';
            let barColor = '#22c55e';
            let statusText = 'Clear';

            if (row.congestion > 80) {

                statusClass = 'text-red';
                barColor = '#ef4444';
                statusText = 'Critical';

            } else if (row.congestion > 50) {

                statusClass = 'text-orange';
                barColor = '#f59e0b';
                statusText = 'Moderate';
            }

            tbody.innerHTML += `
                <tr>
                    <td style="color: #94a3b8;">
                        ${row.timestamp}
                    </td>

                    <td>
                        <strong>${row.location}</strong>
                    </td>

                    <td>
                        <div class="progress-bg">
                            <div 
                                class="progress-fill"
                                style="
                                    width: ${row.congestion}%;
                                    background: ${barColor};
                                ">
                            </div>
                        </div>

                        ${row.congestion}%
                    </td>

                    <td class="${statusClass}">
                        <i class="fas fa-circle"
                           style="
                           font-size:0.6rem;
                           vertical-align:middle;
                           margin-right:5px;">
                        </i>

                        ${statusText}
                    </td>
                </tr>
            `;
        });

        // Update Chart
        updateChart(data.traffic_data);

    } catch (error) {

        console.error('Error fetching data:', error);

        document.getElementById('infra-status').innerText =
            'Connection Lost';

        document.getElementById('infra-status')
            .previousElementSibling
            .style.background = '#ef4444';

        document.getElementById('infra-status')
            .previousElementSibling
            .style.animation = 'none';
    }
}

// 6. Initialization
window.onload = () => {

    initChart();

    updateDashboard();

    setInterval(updateDashboard, 5000);
};