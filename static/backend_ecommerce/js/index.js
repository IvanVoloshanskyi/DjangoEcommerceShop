const HeaderAccountButton = document.getElementsByClassName('header-container__buttons__ul account')


const categories = document.querySelectorAll('.header-categories__ul li');

categories.forEach(category => {
    category.addEventListener('mouseover', () => {
        category.style.color = '#c5872c'; // змінюємо колір тексту при наведенні курсору
    });

    category.addEventListener('mouseout', () => {
        category.style.color = ''; // знімаємо стиль при відведенні курсору
    });
});


let buttonHelp = document.getElementById('header-button-help__id')
let closeButtonHelp = document.querySelector('.close-banner')
let banner = document.querySelector('.background')
buttonHelp.addEventListener('click', () => {
    banner.style.display = 'block';
})
closeButtonHelp.addEventListener('click', () => {
    banner.style.display = 'none';
})


let headerSpanHelp = document.getElementById('header-button-help__id')
let headerSpanText = document.getElementById('header-span-help')
let headerSpanQuestionMark = document.querySelector('#idk')
headerSpanQuestionMark.style.display = 'none'
headerSpanHelp.addEventListener('mouseover', () => {
    headerSpanText.style.display = 'none'
    headerSpanQuestionMark.style.display = 'block'

})
headerSpanHelp.addEventListener('mouseout', () => {
    headerSpanText.style.display = 'block'
    headerSpanQuestionMark.style.display = 'none'
})


