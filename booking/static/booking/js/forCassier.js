const free_node = document.querySelectorAll('.item-empty--free') //NodeList
let free = Array.prototype.slice.call(free_node); //Array
const active_node = document.querySelectorAll('.item-empty--active'); //NodeList
let active = Array.prototype.slice.call(active_node); //Array
// Меняем со свободных на выбранные места
free.forEach((element) => {
    element.addEventListener('click', getActive, {once:true});
})
// Меняем с выбранных на свободные
active.forEach((element) => {
    element.addEventListener('click', getFree, {once:true});
})

function getActive(evt){
    let target = evt.currentTarget; //Получаем наш объект (строку div)

    target.classList.remove('item-empty--free'); //Удаляем класс
    target.classList.add('item-empty--active'); //Добавляем класс, осуществляя замену
    free = free.filter( (element) => element != target ) //Фильтруем изначальный список
    //так как у нас в списке free будет элемент класса item-empty--active
    target.addEventListener('click', getFree, {once:true});//Повесили прослушку события на измененный элемент
    // очень важен параметр {once: true}!
    active.push(target); //Добавили в список активных наш объект
    rentCounter += 1
    rentCount.textContent = rentCounter
}

function getFree(evt){
    //Аналогично, как и у getActive, только для освобождения ячейки.
    const target = evt.currentTarget;

    target.classList.remove('item-empty--active');
    target.classList.add('item-empty--free');
    active = active.filter( (element) => element != target )
    target.addEventListener('click', getActive, {once:true});
    free.push(target);
    rentCounter -= 1
    rentCount.textContent = rentCounter
}

//ТЕСТ!!! НУЖНО СВЯЗЫВАТЬ С БД КОНЕЧНО ЖЕ
let early = Array.prototype.slice.call(document.querySelectorAll('.item-empty--early'));
const UserID = document.querySelector('.inputUserID')
const userid = UserID.value
const Session = document.querySelector('.inputSession')
idsession = Session.value

let formDelRent = document.createElement('form');
formDelRent.action = '/deleteAllRents/';
formDelRent.method = 'GET';

let inputID = document.createElement("input");
inputID.name = "userid"
inputID.value = userid
inputID.style = "display: none;"
formDelRent.appendChild(inputID)
let inputS = document.createElement("input");
inputS.name = "idsession"
inputS.value = idsession
inputS.style = "display: none;"
formDelRent.appendChild(inputS)

// перед отправкой формы, её нужно вставить в документ
document.body.append(formDelRent);
const reset_tickets = () => {
    if  (confirm('Вы уверены, что хотите отменить бронирование?')){
//        early.forEach( (el) => {
//            let target = el;
//
//            target.classList.remove('item-empty--early');
//            target.classList.add('item-empty--free');
//            target.addEventListener('click', getActive, {once:true});
//            free.push(target);
//        })
        formDelRent.submit();
    }
}

//БЛОК КОДА КОТОРЫЙ ОПИСЫВАЕТ ИНФОРМАЦИЮ О БРОНИРОВАНИИ БИЛЕТОВ

//Добавим счетчик на лимит покупки билетов
let rentCounter = 0
//Покажем лимит
let rentCount = document.querySelector('.rent-count')
rentCount.textContent = rentCounter

let cancelCounter = 0
let cancelCount = document.querySelector('.cancel-count')
cancelCount.textContent = cancelCounter

//БЛОК ДЛЯ ОТМЕНЫ БИЛЕТОВ КАССИРОМ



const cassier_node = document.querySelectorAll('.item-empty--cassier') //NodeList
let cassier = Array.prototype.slice.call(cassier_node); //Array
const cancel_node = document.querySelectorAll('.item-empty--cancel') //NodeList
let cancel = Array.prototype.slice.call(cancel_node); //Array
// Меняем со свободных на выбранные места
cassier.forEach((element) => {
    element.addEventListener('click', getCancel, {once:true});
})
// Меняем с выбранных на свободные
cancel.forEach((element) => {
    element.addEventListener('click', getBack, {once:true});
})

function getCancel(evt){
    let target = evt.currentTarget; //Получаем наш объект (строку div)

    target.classList.remove('item-empty--cassier'); //Удаляем класс
    target.classList.add('item-empty--cancel'); //Добавляем класс, осуществляя замену
    cassier = cassier.filter( (element) => element != target ) //Фильтруем изначальный список

    target.addEventListener('click', getBack, {once:true});//Повесили прослушку события на измененный элемент
    // очень важен параметр {once: true}!
    cancel.push(target); //Добавили в список активных наш объект
    cancelCounter += 1
    cancelCount.textContent = cancelCounter
}

function getBack(evt){
    //Аналогично, как и у getActive, только для освобождения ячейки.
    const target = evt.currentTarget;

    target.classList.remove('item-empty--cancel');
    target.classList.add('item-empty--cassier');
    cancel = cancel.filter( (element) => element != target )
    target.addEventListener('click', getCancel, {once:true});
    cassier.push(target);
    cancelCounter -= 1
    cancelCount.textContent = cancelCounter
}

cancel_str = ''
rent_str = ''
const form = document.getElementById('data')
const inputCancel = document.querySelector('.inputCancel')
const inputRent = document.querySelector('.inputRent')
form.addEventListener('submit', (e) => {
    active.forEach( (el) => {
        row = el.getAttribute('row')
        cols = el.getAttribute('cols')
        place = row + cols
        rent_str += place + '.'
    })
    cancel.forEach( (el) => {
        row = el.getAttribute('row')
        cols = el.getAttribute('cols')
        place = row + cols
        cancel_str += place + '.'
    })

    inputCancel.value = cancel_str
    inputRent.value = rent_str
})

