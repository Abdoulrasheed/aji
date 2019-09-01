$(document).ready(()=>{
    const endpoint = `http://${window.location.hostname}/api/`

    $.ajax({
      method: "GET",
      url: endpoint,
      success: (data) => {
        total = data.total
        html_detail = data.q
        setData(total, html_detail);

        labels = data.labels
        values = data.values
        setGraph(labels, values);
      },

      error: (error_data) => {
        console.log(`error_data: ${error_data}`);
      },
    });

    const setData = (total, html_detail) =>{
        $('.v_total').text(total);
        $('.v_detail').html(html_detail);

    }

    const setGraph = () => {
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '# Summary Data',
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    }
});