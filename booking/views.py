from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from urllib.parse import urlencode
import os

# get the path/directory
# cur_path = r'C:\Users\perso\Desktop\Main project\tsite\booking\static\booking\images'  # Папка, где хранятся изображения для слайдера на сервере
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, r'static\booking\images')
images = []  # массив, который содержит имена изображений
for image in os.listdir(filename):
    # check if the image ends with png and jpeg
    if image.endswith(".png") or image.endswith(".jpeg") or image.endswith(".jpg"):
        images.append(str(image))


def auth(request):
    return redirect(reverse('authentication'))


def reg(request):
    return redirect(reverse('registration'))

def exit_acc(request):
    return redirect(get_url_index(0))


def index(request):
    userid = '0'  # Не авторизированный пользователь
    if request.GET.get('userid'):
        userid = str(request.GET.get('userid'))

    is_user_logged_in = 0
    if userid != '0':
        is_user_logged_in = 1

    up = 'Войти'
    down = 'Регистрация'
    context = {}
    """Чтобы передавать id пользователя дальше по формам, сформируем url который передадим в контекст"""
    if is_user_logged_in:
        user = User.objects.get(userid=userid)
        up = user.login
        down = 'Выход'
        context = {'images': images,
                   'userid': userid,
                   'up': up,
                   'down': down,
                   'is_user_logged_in': is_user_logged_in,
                   'url_billboard': get_url_billboard(userid),
                   'url_home': get_url_index(userid),
                   }
    else:
        context = {'images': images, 'up': up, 'down': down, 'is_user_logged_in': is_user_logged_in}
    return render(request, 'booking/index.html', context=context)


def get_url_billboard(userid):
    billboard_url = reverse('billboard')  # Для перехода на афишу
    query_str = urlencode({'userid': userid})
    url = '{}?{}'.format(billboard_url, query_str)
    return url


def get_url_index(userid):
    base_url = reverse('home')
    query_str = urlencode({'userid': userid})
    url = '{}?{}'.format(base_url, query_str)
    return url


def billboard(request):
    userid = 0  # Не авторизированный пользователь
    is_user_logged_in = 0
    if request.GET.get('userid'):
        userid = str(request.GET.get('userid'))
        is_user_logged_in = 1

    films = ActualFilms.objects.all()
    up = 'Авторизуйтесь'
    down = 'Регистрация'
    context = {}
    """Чтобы передавать id пользователя дальше по формам, сформируем url который передадим в контекст"""
    if is_user_logged_in:
        user = User.objects.get(userid=userid)
        up = user.login
        down = 'Выход'
        context = {'films': films,
                   'userid': userid,
                   'up': up,
                   'down': down,
                   'is_user_logged_in': is_user_logged_in,
                   'url_billboard': get_url_billboard(userid),
                   'url_home': get_url_index(userid),
                   }
    else:
        context = {'films': films,
                   'up': up,
                   'down': down,
                   'is_user_logged_in': is_user_logged_in,
                   }

    return render(request, 'booking/billboard.html', context=context)


def date_selection(request):
    userid = 0  # Не авторизированный пользователь
    is_user_logged_in = 0
    if request.GET['userid']:
        userid = str(request.GET['userid'])
        is_user_logged_in = 1
    print(is_user_logged_in)
    user = User.objects.get(userid=userid)
    up = user.login
    down = 'Выход'
    filmID = request.GET['filmID']

    sessions = Session.objects.filter(idfilm=filmID).order_by('date')  # Получили список сеансов
    sessions_dates = []  # Cписок дат на сеансы
    list_of_sessions = []
    for session in sessions:
        if session.date not in sessions_dates:
            sessions_dates.append(session.date)
            list_of_sessions.append(session)

    time_dict = {}  # {date: [times]}
    for sess_date in sessions_dates:
        time = []
        sess = Session.objects.filter(idfilm=filmID).filter(date=sess_date)  # Сеансы по дате
        for s in sess:
            time.append(s.time)
        time = sorted(time)
        time_dict[sess_date] = time
    print(time_dict)


    context = {
        'sessions': list_of_sessions,
        'times': time_dict,
        'filmID': filmID,
        'userid': userid,
        'up': up,
        'down': down,
        'is_user_logged_in': is_user_logged_in,
        'url_billboard': get_url_billboard(userid),
        'url_home': get_url_index(userid),
    }

    return render(request, 'booking/date_selection.html', context=context)


def date_format(date_str):  # Вспомогательная функция
    # Format YYYY-MM-DD
    month_dict = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октября': '10',
    'ноября': '11',
    'декабря': '12',
    }
    date_split = date_str.split(' ')
    res_date = f'{date_split[2]}-{month_dict[date_split[1]]}-{date_split[0]}'
    return res_date

def scheme(request):
    """В зависимости от роли у нас разное отображение схемы для кассира и пользователя"""
    is_user_logged_in = 1
    """Предполагаем что у нас пара дата-время для конкретного фильма не повторяются,
       т.е. у нас нет Сеанс 1, дата 10.03.23 время 10:30 и Сеанс 2б дата 10.03.23 время 10:30"""
    date = date_format(request.GET['date'])
    time = request.GET['time']
    filmID = request.GET['filmID']

    # По моей логике мы однозначно определили сеанс, чтобы в дальнейшем это использовать
    session = Session.objects.filter(idfilm=filmID).filter(date=date).filter(time=time)
    idsession = session[0].idsession
    hall = session[0].hall
    film = ActualFilms.objects.get(idfilm=filmID)
    film_name = film.name

    userid = request.GET['userid']  # для теста
    user = User.objects.get(userid=userid)
    userRole = user.role
    # print(userRole)
    places = Places.objects.get(idsession=idsession).get_places()
    place_status = []
    context = {
        'idsession': idsession,
        'film_name': film_name,
        'userid': userid,
        'date': date,
        'time': time,
        'hall': hall,
        'filmID': filmID,
        'place_status': place_status,
        'up': user.login,
        'down': 'Выход',
        'is_user_logged_in': is_user_logged_in,
        'url_billboard': get_url_billboard(userid),
        'url_home': get_url_index(userid),
    }

    if userRole == 'Пользователь':
        """Разберемся с местами, алгоритм такой: 
        есть список мест на сеансе в виде 0 и 1, мы переводим их в массив
        строк где 0 - "item-empty", 1 - "item-empty--free", если 1 нужно ещё проверить
         через таблицу Rent не мы ли забронировали этот билет """
        rents = Rent.objects.filter(idsession=idsession).filter(iduser=userid)  # QuerySet с записями брони на данный сеанс для пользователя
        rent_places_idx = [get_place_index(str(rent.place)) for rent in rents]  # Получили список индексов мест, которые заняты ранее

        for i in range(len(places)):
            # Проверяем раннюю бронь места
            if i in rent_places_idx:
                place_status.append('item-empty--early')
            elif places[i] == 1:
                place_status.append('item-empty--free')
            else:
                place_status.append('item-empty')

        return render(request, 'booking/scheme.html', context=context)
    elif userRole == 'Кассир':
        """Кассир должен иметь доступ к каждому забронированному месту, так что все свободные (1) будут отображаться как 
        'item-empty--free', а все забронированные как 'item-empty--early' """
        for place in places:
            if place == 0:
                place_status.append('item-empty--cassier')
            elif place == 1:
                place_status.append('item-empty--free')

        return render(request, 'booking/scheme_for_cassier.html', context=context)


def rent(request):
    """Сделаю функцию и под пользователя и под кассира"""
    rent_places = request.GET['rent_place'].split('.')  # Вернет массив, в конце будет пробел, его учитывать не будем в дальнейшем
    idsession = request.GET['idsession']
    userid = request.GET['userid']


    place = Places.objects.get(idsession=idsession)
    places = place.get_places()  # Места сеанса для обновления

    session = Session.objects.get(idsession=idsession)
    user = User.objects.get(userid=userid)

    """Теперь удалим записи для билетов в таблице | Только для кассира, проверку можно было сделать по разному
       я просто проверю роль юзера"""
    role = user.role
    # print(role)
    if role == 'Кассир':
        # Принимаем параметр, если запрос был отправлен кассиром
        cancel_places = []
        if request.GET['cancel_place']:
            cancel_places = request.GET['cancel_place'].split('.')  # Вернет массив, в конце будет пробел, его учитывать не будем в дальнейшем
            """Ну и если запрос пришел, то форма была отправлена кассиром и он что то отменяет, и 
            значит обновление мест я пропишу в этом блоке"""
            for i in range(len(cancel_places) - 1):
                pl = cancel_places[i]
                places[get_place_index(pl)] = 1  # собрали массив изменений, осталось их применить
        if len(cancel_places) != 0:
            for i in range(len(cancel_places) - 1):
                pl = int(cancel_places[i])
                Rent.objects.filter(idsession=session, place=pl).delete()

    # Обновим массив рассадки мест | Подходит и для кассира и для пользователя
    for i in range(len(rent_places) - 1):
        pl = rent_places[i]
        places[get_place_index(pl)] = 0  # собрали массив изменений, осталось их применить

    """Теперь создадим записи для билетов в таблице | Подходит и для кассира и для пользователя"""
    for i in range(len(rent_places) - 1):
        pl = int(rent_places[i])
        Rent.objects.create(idsession=session, iduser=user, place=pl, buyflg=False)

    """Я не знаю как ещё обновить поля в модели, пробовал разные варианты и через, массив который 
    возвращает get_places() и через обращение к атрибутам, в итоге меняется только при прямом обращении к полю"""
    place.p1 = places[0]
    place.p2 = places[1]
    place.p3 = places[2]
    place.p4 = places[3]
    place.p5 = places[4]
    place.p6 = places[5]
    place.p7 = places[6]
    place.p8 = places[7]
    place.p9 = places[8]
    place.p10 = places[9]
    place.p11 = places[10]
    place.p12 = places[11]
    place.p13 = places[12]
    place.p14 = places[13]
    place.p15 = places[14]
    place.p16 = places[15]
    place.p17 = places[16]
    place.p18 = places[17]
    place.p19 = places[18]
    place.p20 = places[19]
    place.p21 = places[20]
    place.p22 = places[21]
    place.p23 = places[22]
    place.p24 = places[23]
    place.p25 = places[24]
    place.save()
    """Мне тоже было больно это писать, но пока другого выхода я не знаю"""

    return redirect(get_url_billboard(userid), permanent=True)
    # return redirect(request.META.get('HTTP_REFERER'), permanent=True)

def get_place_index(rowCol):
    accord = {
        '11': 0,
        '12': 1,
        '13': 2,
        '14': 3,
        '15': 4,
        '21': 5,
        '22': 6,
        '23': 7,
        '24': 8,
        '25': 9,
        '31': 10,
        '32': 11,
        '33': 12,
        '34': 13,
        '35': 14,
        '41': 15,
        '42': 16,
        '43': 17,
        '44': 18,
        '45': 19,
        '51': 20,
        '52': 21,
        '53': 22,
        '54': 23,
        '55': 24,
    }
    return accord[rowCol]

# Удаление всех забронированных мест
def deleteAllRents(request):
    userid = request.GET['userid']
    idsession = request.GET['idsession']

    place = Places.objects.get(idsession=idsession)
    places = place.get_places()  # Места сеанса для обновления

    session = Session.objects.get(idsession=idsession)
    user = User.objects.get(userid=userid)

    role = user.role
    print(role)
    if role == 'Кассир':
        for i in range(len(places)):
            places[i] = 1

        Rent.objects.filter(idsession=session).delete()
        print('BLOCK CAASIER')
    elif role == 'Пользователь':
        rents = Rent.objects.filter(idsession=idsession).filter(iduser=userid)  # QuerySet с записями брони на данный сеанс для пользователя
        rent_places_idx = [get_place_index(str(rent.place)) for rent in rents]  # Получили список индексов мест, которые заняты ранее
        for i in rent_places_idx:
            places[i] = 1

        Rent.objects.filter(idsession=session, iduser=userid).delete()
        print('BLOCK USER')

    """Я не знаю как ещё обновить поля в модели, пробовал разные варианты и через, массив который 
    возвращает get_places() и через обращение к атрибутам, в итоге меняется только при прямом обращении к полю"""
    place.p1 = places[0]
    place.p2 = places[1]
    place.p3 = places[2]
    place.p4 = places[3]
    place.p5 = places[4]
    place.p6 = places[5]
    place.p7 = places[6]
    place.p8 = places[7]
    place.p9 = places[8]
    place.p10 = places[9]
    place.p11 = places[10]
    place.p12 = places[11]
    place.p13 = places[12]
    place.p14 = places[13]
    place.p15 = places[14]
    place.p16 = places[15]
    place.p17 = places[16]
    place.p18 = places[17]
    place.p19 = places[18]
    place.p20 = places[19]
    place.p21 = places[20]
    place.p22 = places[21]
    place.p23 = places[22]
    place.p24 = places[23]
    place.p25 = places[24]
    place.save()
    """Мне тоже было больно это писать, но пока другого выхода я не знаю"""

    return redirect(get_url_billboard(userid), permanent=True)
    # return redirect(request.META.get('HTTP_REFERER'), permanent=True)

def test(request):
    rent_place = request.GET['rent_place']
    cancel_place = request.GET['cancel_place']
    return HttpResponse(f'cancel_place {cancel_place} AND rent_place = {rent_place}')
