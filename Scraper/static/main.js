
const toggleButton = document.getElementById('toggle-btn');
const sideBar = document.getElementById('side-bar');
const forms = document.querySelector('.forms');

toggleButton.addEventListener('click', show);

function show(){
  sideBar.classList.toggle('active');
  if (forms.style.display === 'none') {
    $('form').css({"display": "block", "transition": "3.5s ease"});
  } else {
    forms.style.display = 'none';
  }
}

// CHART NOT WROKING WITH THIS
// REMOVE SIDEBAR IF CLICK ON THE MAIN CONTENT
const content = document.querySelector('.chart');

content.addEventListener('click', () => {
  sideBar.classList.remove('active');
  forms.style.display = 'block';
});


var language_labels = ['C#', 'C/C++', 'Dart', 'Golang', 'Java', 
                       'JavaScript', 'Kotlin', 'PHP', 'Python', 'Ruby', 'Scala', 'Swift', 'Typescript']

var framwork_labels = ['.NET', 'Angular', 'Django', 'Flask', 'Laravel', 
                       'React', 'Ruby on Rails', 'Spring', 'Vue.js']

var tool_labels = ['AWS', 'DigitalOcean', 'Git', 'Linux', 'Microsoft SQL Server', 
                   'MySQL', 'Oracle', 'PostgreSQL',]           

var lang_data = []
var framework_data = []
var tool_data = []
var chartData = []

var ctx = document.getElementById('myChart').getContext('2d');
var languages = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['C#', 'C/C++', 'Dart', 'Golang', 'Java', 'JavaScript', 'Kotlin', 'PHP',
                  'Python', 'Ruby', 'Scala', 'Swift', 'Typescript'],
        datasets: [{
            label: '# of Jobs',
            data: chartData,
            backgroundColor: [
                'rgba(150, 74, 149, 0.5)',
                'rgba(100, 154, 210, 0.5)',
                'rgba(65, 196, 255, 0.5)',
                'rgba(105, 215, 228, 0.5)',
                'rgba(231, 111, 0, 0.5)',
                'rgba(247, 224, 24, 0.5)',
                'rgba(54, 111, 159, 0.5)',
                'rgba(243, 102, 98, 0.5)',
                'rgba(220, 52, 49, 0.5)',
                'rgba(243, 100, 57, 0.5)',
                'rgba(0, 122, 204, 0.5)',
                'rgba(243, 100, 57, 0.5)',
                'rgba(0, 122, 204, 0.5)',
            ],
            borderColor: [
            ],
            borderWidth: 1
        }]
    },
   options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
             labels: {
                  fontColor: 'white'
                 }
              },
        title: {
            display: true,
            fontColor: 'white',
            text: ''
        }     ,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true,
                    fontColor: 'white'
                },
            }],
          xAxes: [{
                ticks: {
                    fontColor: 'white'
                },
            }]
        }
    }
});

$('#city_select, #stat_options').on('change', function () {
    var city = $('#city_select').find("option:selected").text();
    var stat = $('#stat_options').find("option:selected").text();
    //console.log(city);
    //console.log(stat)

    // POST
    fetch('/city_selection', {

        // Specify the method
        method: 'POST',

        // JSON
        headers: {
            'Content-Type': 'application/json'
        },

        // A JSON payload
        body: JSON.stringify({
            'options': [city, stat]
        })
    }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
    }).then(function (text) {
        //console.log('Chart data',text);
        chartData = JSON.parse(text)
        //console.log('json parsed ', chartData)

	if (stat == 'Languages') {
            languages.data.labels = language_labels;
        }
        else if (stat == 'Frameworks') {
            languages.data.labels = framwork_labels;
        }
        else if (stat == 'Tools'){
            languages.data.labels = tool_labels;
        }

        languages.data.datasets[0].data = chartData;
        languages.update();
    });
});

