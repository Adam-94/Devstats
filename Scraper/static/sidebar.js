
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
