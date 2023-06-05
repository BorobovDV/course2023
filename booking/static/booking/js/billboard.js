//БЛОК ПЕРЕХОДА К БРОНИРОВАНИЮ
const film_node = document.querySelectorAll('.btn1') //NodeList

film_node.forEach(function(element) {
    element.addEventListener('click', setIdFilm)
});

filmID = ''
function setIdFilm(evt){
    const target = evt.currentTarget

   filmID = target.id
}

const form = document.getElementById('data')
const inputFilmID = document.querySelector('.inputFilmID')
form.addEventListener('submit', () => {
    inputFilmID.value = filmID
})

//ЭТОТ БЛОК ПЕРЕДАЕТ НА СЕРВЕР ID ВЫБРАННОГО ФИЛЬМА, ЧТОБЫ ПЕРЕЙТИ К БРОНИРОВАНИЮ
