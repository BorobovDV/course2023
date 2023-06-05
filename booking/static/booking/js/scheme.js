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
    if (counter <= 0){
        target.addEventListener('click', getFree, {once:true})
        alert('Ваш лимит бронирования исчерпан :(')
    }else{
        target.classList.remove('item-empty--free'); //Удаляем класс
        target.classList.add('item-empty--active'); //Добавляем класс, осуществляя замену
        free = free.filter( (element) => element != target ) //Фильтруем изначальный список
        //так как у нас в списке free будет элемент класса item-empty--active
        target.addEventListener('click', getFree, {once:true});//Повесили прослушку события на измененный элемент
        // очень важен параметр {once: true}!
        active.push(target); //Добавили в список активных наш объект

        //Новое: добавление информации о выбраном билете
        rowDiv = target.getAttribute('row')
        cols = target.getAttribute('cols')
        addBlock(rowDiv, cols)
    }
}

function getFree(evt){
    //Аналогично, как и у getActive, только для освобождения ячейки.
    const target = evt.currentTarget;

    target.classList.remove('item-empty--active');
    target.classList.add('item-empty--free');
    active = active.filter( (element) => element != target )
    target.addEventListener('click', getActive, {once:true});
    free.push(target);

    //Новое: обновление информации о выбранных билетах (при отмене выбора)
    rowDiv = target.getAttribute('row')
    cols = target.getAttribute('cols')
    delBlock(rowDiv, cols)
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
//formDelRent.innerHTML = `<input name="idsession" value="${idsession}">`;

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
//Невероятно сложное: отправить данные на сервер для обработки

//Создадим массив, который будет содержать пары рядстолбец
//н-р [12,22,23]
sendArray = []
//В этот массив мы будем вносить или удалять значения рядстолбец
//в функциях addBlock или delBlock
//А при нажатии на кнопку glow-on-hover мы откроем соединение с сервером
//и отправим наш массив


//БЛОК КОДА КОТОРЫЙ ОПИСЫВАЕТ ИНФОРМАЦИЮ О БРОНИРОВАНИИ БИЛЕТОВ

//Прочитаем класс в который будем добавлять сведения о билетах
let placeContent = document.querySelector('.place-content') //NodeList

//Добавим счетчик на лимит покупки билетов
let counter = 5
// counter -= early.length 

//Покажем лимит
let rentCount = document.querySelector('.rent-count')
rentCount.textContent = counter

//Покажем цену
let price = document.querySelector('.price')
price.textContent = (5 - counter) * 300 + ' рублей'

//Создадим класс, который будем добавлять в placeContent
//по типу:
{/* <div class="row">
        <div class="place">
            <p>Ряд :</p>
            <p>1</p>
            <p>Место :</p>
            <p>1</p>
        </div>
    </div> */}

//Добавляем функцию, которая добавляет код
const addBlock = function(rows, cols){
    let addRowDiv = document.createElement('div')
    addRowDiv.className = 'add-row' 
    //Этот блок я сделал чисто для обертки, чтобы потом
    // давать ему уникальное название которое будет равно add-row + row + col элемента
    // это нужно для простого удаления

    let rowDiv = document.createElement('div')
    rowDiv.className = 'row'

    let placeDiv = document.createElement('div')
    placeDiv.className = 'place'

    let placeRowP = document.createElement('p')
    placeRowP.className = 'place-row'
    placeRowP.textContent = 'Ряд :'

    let placeRowNumP = document.createElement('p')
    placeRowNumP.className = 'row-num'

    let placeColP = document.createElement('p')
    placeColP.className = 'place-col'
    placeColP.textContent = 'Место :'

    let placeColNumP = document.createElement('p')
    placeColNumP.className = 'col-num'


    //Создаем добавочный блок
    addRowDiv.className = 'add-row' + rows + cols
    placeRowNumP.textContent = rows
    placeColNumP.textContent = cols
    counter -= 1
    rentCount.textContent = counter
    price.textContent = (5 - counter) * 300 + ' рублей'

    placeDiv.append(placeRowP)
    placeDiv.append(placeRowNumP)
    placeDiv.append(placeColP)
    placeDiv.append(placeColNumP)
    rowDiv.append(placeDiv)
    addRowDiv.append(rowDiv)
    
    placeContent.append(addRowDiv)

    rowcol = rows + cols
    sendArray.push(rowcol) //Добавление элемента для отправки 
}

//Для забронированных ранее сразу создадим блоки
early.forEach((el) => {
    row = el.getAttribute('row')
    cols = el.getAttribute('cols')
    addBlock(row, cols)

    rowcol = row + cols //Удаление элемента из массива для отправки
    sendArray = sendArray.filter((element) => element != rowcol)
})

//Добавляем функцию, которая удаляет блок кода 
const delBlock = function(rows, cols){
    const nameBlock = '.add-row' + rows + cols
    const block = document.querySelector(nameBlock)

    block.remove()

    counter += 1
    rentCount.textContent = counter
    price.textContent = (5 - counter) * 300 + ' рублей'

    rowcol = rows + cols //Удаление элемента из массива для отправки
    sendArray = sendArray.filter((element) => element != rowcol)
}

//БЛОК ЗАКОНЧЕН 

select_places = ''
const form = document.getElementById('data')
const inputRNT = document.querySelector('.inputRNT')
form.addEventListener('submit', (e) => {
    sendArray.forEach( (el) => {
        select_places += el + '.'
    })

    inputRNT.value = select_places
})

