// statistics.js


// Espera a que el DOM esté listo
document.addEventListener("DOMContentLoaded", () => {

    //Number of times played each deck
    const ctx0 = document.getElementById('deckUsageChart').getContext('2d');
    const deckUsageChart = new Chart(ctx0, {
        type: 'bar',
        data: {
            labels: deckNames,
            datasets: [{
                label: 'Number of Times Played',
                data: deckPlayedCounts,
                backgroundColor: 'rgba(229, 153, 0, 0.8)',
                borderColor: 'rgba(229, 80, 0, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false, // Permitir modificar la altura y el ancho
            plugins: {
                legend: {
                    display: false // Ocultar la leyenda si no es necesaria
                },
                title: {
                    display: true,
                    text: 'Number of times played each deck'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 45, // Ajustar rotación de las etiquetas si es necesario
                        minRotation: 0
                    }
                }
            }
        }
    });
    
    
    //Wincons pie
    const ctx1 = document.getElementById('endConditionChart').getContext('2d');
    const endConditionChart = new Chart(ctx1, {
        type: 'pie',
        data: {
            labels: conditionLabels,
            datasets: [{
                label: 'End Conditions',
                data: conditionValues,
                backgroundColor: [
                    '#EEEEEE', // White
                    '#00AEEF', // Blue
                    '#000000', // Black
                    '#E53935', // Red
                    '#4CAF50', // Green
                    '#FFD700', // Yellow for unique cases
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Distribution of End Conditions'
                }
            }
        }
    });

    //Guilds graph
    

    const ctx2 = document.getElementById('colorCombinationChart').getContext('2d');
    const colorCombinationChart = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: colorLabels,
            datasets: [{
                label: 'Times Played',
                data: colorPlayedCounts,
                backgroundColor: 'rgba(229, 153, 0, 0.8)',
                borderColor: 'rgba(229, 80, 0, 1)',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'x', // Barras horizontales
            responsive: true,
            maintainAspectRatio: false, // Permitir modificar la altura y el ancho
            plugins: {
                legend: {
                    display: false // Ocultar leyenda
                },
                title: {
                    display: true,
                    text: 'Color Combinations Played'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                },
                x: {
                    ticks: {
                        maxRotation: 45, // Ajustar rotación de las etiquetas si es necesario
                        minRotation: 0
                    }
                }
            }
        }
    });

    //Color pie
    const ctx3 = document.getElementById('colorPieChart').getContext('2d');
    const colorPieChart = new Chart(ctx3, {
        type: 'pie',
        data: {
            labels: colorLabelsPie,
            datasets: [{
                label: 'Color Distribution',
                data: colorCountsPie,
                backgroundColor: [
                    '#FFFFFF', // White
                    '#00AEEF', // Blue
                    '#000000', // Black
                    '#E53935', // Red
                    '#4CAF50', // Green
                    '#CCCCCC'  // Colorless
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false,
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Color Distribution'
                }
            }
        }
    });


    //Pie chart posiciones %
    const ctx4 = document.getElementById('positionChart').getContext('2d');
    new Chart(ctx4, {
        type: 'pie',
        data: {
            labels: positionLabels,
            datasets: [{
                data: positionValues,
                backgroundColor: ['gold', 'silver', '#cd7f32', '#4caf50', '#000000'], // Colores para cada posición
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Position Distribution'
                }
            }
        }
    });


});