# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy


class ActualFilms(models.Model):
    idfilm = models.AutoField(db_column='IDfilm', primary_key=True)
    name = models.CharField(max_length=150, verbose_name='Название фильма')
    duration = models.TimeField(auto_now=False, auto_now_add=False, verbose_name='Длительность')
    poster = models.ImageField(upload_to="posters/%Y/%m/%d", verbose_name='Постер фильма')
    trailer = models.CharField(max_length=150, verbose_name='Ссылка на трейлер', null=True)
    flag = models.BooleanField(default=False, verbose_name='Прямо сейчас в прокате')
    price = models.IntegerField(null=False, help_text='Рекомендуемая цена для всех 300 руб.', verbose_name='Цена')

    class Meta:
        db_table = 'ActualFilms'
        verbose_name = 'Актуальный фильм'
        verbose_name_plural = 'Актуальный фильмы'

    @property
    def get_poster(self):
        """
        Получение заглушки при отсутсвии изображения
        """
        if not self.poster:
            return '/media/images/placeholder.png'
        return self.poster.url

    def __str__(self):
        return f"Фильм: {self.name}, продолжительность: {self.duration}"


def place_validator(place_status):
    if place_status not in [0, 1, 2]:
        raise ValidationError(
            gettext_lazy('%(place_status)s is wrong place status'),
            params={'place_status': place_status},
        )


class Places(models.Model):
    idsession = models.OneToOneField('Session', models.PROTECT, db_column='IDSession', primary_key=True)
    p1 = models.IntegerField(verbose_name='Место 1', validators=[place_validator], default=1)
    p2 = models.IntegerField(verbose_name='Место 2', validators=[place_validator], default=1)
    p3 = models.IntegerField(verbose_name='Место 3', validators=[place_validator], default=1)
    p4 = models.IntegerField(verbose_name='Место 4', validators=[place_validator], default=1)
    p5 = models.IntegerField(verbose_name='Место 5', validators=[place_validator], default=1)
    p6 = models.IntegerField(verbose_name='Место 6', validators=[place_validator], default=1)
    p7 = models.IntegerField(verbose_name='Место 7', validators=[place_validator], default=1)
    p8 = models.IntegerField(verbose_name='Место 8', validators=[place_validator], default=1)
    p9 = models.IntegerField(verbose_name='Место 9', validators=[place_validator], default=1)
    p10 = models.IntegerField(verbose_name='Место 10', validators=[place_validator], default=1)
    p11 = models.IntegerField(verbose_name='Место 11', validators=[place_validator], default=1)
    p12 = models.IntegerField(verbose_name='Место 12', validators=[place_validator], default=1)
    p13 = models.IntegerField(verbose_name='Место 13', validators=[place_validator], default=1)
    p14 = models.IntegerField(verbose_name='Место 14', validators=[place_validator], default=1)
    p15 = models.IntegerField(verbose_name='Место 15', validators=[place_validator], default=1)
    p16 = models.IntegerField(verbose_name='Место 16', validators=[place_validator], default=1)
    p17 = models.IntegerField(verbose_name='Место 17', validators=[place_validator], default=1)
    p18 = models.IntegerField(verbose_name='Место 18', validators=[place_validator], default=1)
    p19 = models.IntegerField(verbose_name='Место 19', validators=[place_validator], default=1)
    p20 = models.IntegerField(verbose_name='Место 20', validators=[place_validator], default=1)
    p21 = models.IntegerField(verbose_name='Место 21', validators=[place_validator], default=1)
    p22 = models.IntegerField(verbose_name='Место 22', validators=[place_validator], default=1)
    p23 = models.IntegerField(verbose_name='Место 23', validators=[place_validator], default=1)
    p24 = models.IntegerField(verbose_name='Место 24', validators=[place_validator], default=1)
    p25 = models.IntegerField(verbose_name='Место 25', validators=[place_validator], default=1)

    class Meta:
        db_table = 'Places'
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def get_places(self):  # ОТЛИЧНАЯ ИДЕЯ, А ПОТОМ ПРОСТО ПЕРЕБИРАЕМ ИХ В ДРУГОМ ВЬЮ
        return [self.p1, self.p2, self.p3, self.p4, self.p5,
                self.p6, self.p7, self.p8, self.p9, self.p10,
                self.p11, self.p12, self.p13, self.p14, self.p15,
                self.p16, self.p17, self.p18, self.p19, self.p20,
                self.p21, self.p22, self.p23, self.p24, self.p25,
                ]

    def __str__(self):
        return f'Сеанс: {self.idsession}'


def rent_validator(rent_status):
    if 1 <= rent_status <= 25:
        raise ValidationError(
            gettext_lazy('%(rent_status)s is wrong place status'),
            params={'rent_status': rent_status},
        )


class Rent(models.Model):
    idrent = models.AutoField(db_column='IDRent', primary_key=True)
    idsession = models.ForeignKey('Session', models.PROTECT, db_column='IDSession')
    iduser = models.ForeignKey('User', models.PROTECT, db_column='IDUser')
    place = models.IntegerField(db_column='Place', null=False, validators=[rent_validator])
    buyflg = models.BooleanField(null=False)  # ? обязательно ли?

    class Meta:
        db_table = 'Rent'
        unique_together = (('idsession', 'place'),)
        verbose_name = 'Бронь'
        verbose_name_plural = 'Бронь'

    def __str__(self):
        return f'Session: {self.idrent}, iduser: {self.iduser}'


class Session(models.Model):
    idsession = models.AutoField(db_column='IDSession', primary_key=True)
    date = models.DateField(db_column='Date', null=False)
    time = models.TimeField(db_column='Time', null=False)
    hall = models.IntegerField(db_column='Hall', null=False)
    idfilm = models.ForeignKey('ActualFilms', models.PROTECT, db_column='IDfilm', null=False)

    class Meta:
        db_table = 'Session'
        unique_together = (('date', 'time', 'idfilm', 'hall'), ('time', 'hall', 'date'),)
        verbose_name = 'Сеанс'
        verbose_name_plural = 'Сеансы'

    def __str__(self):
        return f'Сеанс: {self.idsession}, фильм: {self.idfilm}, время {self.time}'


def role_validator(role_status):
    if role_status not in ['Кассир', 'Администратор', 'Пользователь']:
        raise ValidationError(
            gettext_lazy('%(role_status)s is wrong place status'),
            params={'role_status': role_status},
        )


class User(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)
    email = models.CharField(db_column='Email', unique=True, max_length=75)
    password = models.CharField(db_column='Password', max_length=50)
    login = models.CharField(db_column='Login', unique=True, max_length=50)
    role = models.CharField(max_length=30, db_column='Role', validators=[role_validator])

    class Meta:
        db_table = 'User'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь: {self.login}, роль: {self.role}'

