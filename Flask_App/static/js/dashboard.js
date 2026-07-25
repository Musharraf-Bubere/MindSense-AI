// =======================================
// Risk Distribution Chart
// =======================================
const dashboardData = document.getElementById("dashboard-data");

const lowRiskCount = Number(dashboardData.dataset.low);
const highRiskCount = Number(dashboardData.dataset.high);

const riskChart = document.getElementById("riskChart");

if (riskChart) {

    new Chart(riskChart, {

        type: "doughnut",

        data: {

            labels: [
                "Low Risk",
                "High Risk"
            ],

            datasets: [{

                data: [lowRiskCount, highRiskCount],

                backgroundColor: [
                    "#22C55E",
                    "#EF4444"
                ],

                borderWidth: 2,

                hoverOffset: 10

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom"

                },

                tooltip: {

                    callbacks: {

                        label: function(context) {

                            const total = lowRiskCount + highRiskCount;

                            const value = context.raw;

                            const percent = total === 0
                                ? 0
                                : ((value / total) * 100).toFixed(1);

                            return `${context.label}: ${value} (${percent}%)`;

                        }

                    }

                }

            }

        }

    });

}


// =======================================
// Model Performance Chart
// =======================================

const performanceChart = document.getElementById("performanceChart");

if (performanceChart) {

    new Chart(performanceChart, {

        type: "bar",

        data: {

            labels: [
                "Accuracy",
                "Precision",
                "Recall",
                "F1 Score"
            ],

            datasets: [{

                label: "Performance (%)",

                data: [96, 95, 94, 95],

                backgroundColor: [
                    "#2563EB",
                    "#22C55E",
                    "#F59E0B",
                    "#8B5CF6"
                ],

                borderRadius: 8

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            scales: {

                y: {

                    beginAtZero: true,

                    max: 100

                }

            },

            plugins: {

                legend: {

                    display: true

                }

            }

        }

    });

}