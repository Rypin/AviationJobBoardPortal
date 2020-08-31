const toggle = document.getElementById('toggle');  
const close  = document.getElementById('close'); 
const expandToggle = document.getElementById('expandToggle')

//toggle nav
toggle.addEventListener('click', () => 
expandToggle.classList.toggle('show-nav') 
);
