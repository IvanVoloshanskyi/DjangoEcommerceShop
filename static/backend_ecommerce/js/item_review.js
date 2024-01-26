const buttonWriteReview = document.querySelector('.button-write-review');
const dropdown = document.querySelector('.dropdown');

buttonWriteReview.addEventListener('click', function () {
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
});
