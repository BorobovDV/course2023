//БЛОК ДЛЯ КНОПКИ ПОДТВЕРЖДЕНИЯ ДАТЫ
const date_node = document.querySelectorAll('.date') //NodeList
const time__content = document.querySelectorAll('.time__content')
const time_node = document.querySelectorAll('.time'); //NodeList
const select_date = document.querySelector('.select_date');  //####
date_node.forEach(function(element) {
    element.addEventListener('click', activeDate)
});

date_active = ''
function activeDate(evt){
    const target = evt.currentTarget

    date_node.forEach((item) => {
        item.classList.remove('date--active')
    })

    target.classList.add('date--active')
    date_active = target.innerHTML

    time__content.forEach((item) => {
        item.classList.remove('time__content--active')
    })

    time__active = document.getElementById(date_active)
    time__active.classList.add('time__content--active')

    //Это для того, чтобы кнопка бронирования не нажималась до выбора времени под соответствующую дату
    time_active = ''
    time_node.forEach((item) => {
        item.classList.remove('time--active')
    })
    select_date.style.display = "block"; //####
}


time_node.forEach(function(element) {
    element.addEventListener('click', activeTime)
});

time_active = ''
function activeTime(evt){
    const target = evt.currentTarget

    time_node.forEach((item) => {
        item.classList.remove('time--active')
    })

    target.classList.add('time--active')
    time_active = target.innerHTML
}



const inputDate = document.querySelector('.inputDate')
const inputTime = document.querySelector('.inputTime')
const form = document.getElementById('data')
const sub_btn = document.querySelector('.date_time_btn')
function sub(){
    if (time_active != ''){
            inputDate.value = date_active
            inputTime.value = time_active
            form.submit()
    }else{
        sub_btn.addEventListener('click', sub)
    }
}
sub_btn.addEventListener('click', sub)


