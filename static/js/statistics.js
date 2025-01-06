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
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
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
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Distribution of End Conditions'
                }
            }
        }
    });


  });
  