new Chart("byMonthsChart", {
    type: "bar",
    data: {
      labels: byMonthLabels,
      datasets: [{
        backgroundColor: '#C62E2E',
        data: expensesByMonthValues,
        borderColor: "gray",
        borderWidth: 0.5
      }]
    },
    options: {
      scales: {
              yAxes: [{
                  display: true,
                  ticks: {
                      beginAtZero: true
                  }
              }],
          },
      legend: {display: false},
      title: {
        display: true,
        text: "Next months"
      }
    }
  });
  
new Chart("byTypeChart", {
    type: 'doughnut',
    data: {
      labels: ['Fixes', 'Variable'],
      datasets: [
          {
          label: 'Dataset 1',
          data: byTypeValues,
          backgroundColor: ['Gray', '#C62E2E'],
          }
    ]},
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Type'
        }
      }
    },
});
  
new Chart("byCategoryChart", {
    type: 'doughnut',
    data: {
      labels: byCategoryLabels,
      datasets: [
          {
          label: 'Dataset 1',
          data: byCategoryValues,
          backgroundColor: byCategoryColors,
          }
    ]},
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Type'
        }
      }
    },
});
  
new Chart("balanceChart", {
    type: "bar",
    data: {
      labels: byMonthLabels,
      datasets: [{
            label: 'Incomes',
            backgroundColor: 'Green',
            data: incomesByMonthValues,
            borderColor: "gray",
            borderWidth: 0.5
          },
        {
        label: 'Expenses',
        backgroundColor: '#C62E2E',
        data: expensesByMonthValues,
        borderColor: "gray",
        borderWidth: 0.5
      }]
    },
    options: {
      scales: {
              yAxes: [{
                  display: true,
                  ticks: {
                      beginAtZero: true
                  }
              }],
          },
      legend: {display: true},
    }
  });