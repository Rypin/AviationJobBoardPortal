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
    x = document.getElementById("animatable")
    // x.className = "materialize"
    x.style.display = "block" 
});

navBar.addEventListener('mouseleave', () => {
    expandToggle.classList.toggle('show-nav')
    x = document.getElementById("animatable")
    // x.className = "dissolve" 
    // setTimeout(function(){
    x.style.display = "none"
    // },750)
});



