const toggle = document.getElementById('toggle');  
const close  = document.getElementById('close'); 
const expandToggle = document.getElementById('expandToggle')

const navBar = document.getElementById('toggleNavBar')

//toggle nav

/*
toggle.addEventListener('click', () => 
expandToggle.classList.toggle('show-nav') 
);

*/

navBar.addEventListener('mouseenter', () => {
    expandToggle.classList.toggle('show-nav')
    document.getElementById("animatable").className = "materialize"
});

navBar.addEventListener('mouseleave', () => {
    expandToggle.classList.toggle('show-nav')
    document.getElementById("animatable").className = "dissolve"
});



