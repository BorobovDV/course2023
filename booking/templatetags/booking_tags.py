from django import template
import os

register = template.Library()

@register.simple_tag()
def get_main_back():
    return r'C:\Users\perso\Desktop\Main Project\tsite\booking\static\booking\images\backs\main_back.jpg' # Абсолютный путь к фоновой картинке

@register.simple_tag()
def get_images_path():
    return r'C:\Users\perso\Desktop\Main Project\tsite\booking\static\booking\images'

@register.simple_tag()
def get_image_path():
    # Получаем массив, который содержит пути для картинок в слайдер, и потом этот тег пишем в html index
    # get the path/directory
    cur_path = r'C:\Users\perso\Desktop\Main project\tsite\booking\static\booking\images'  # Папка, где хранятся изображения для слайдера на сервере
    images = []  # массив, который содержит имена изображений
    for image in os.listdir(cur_path):
        # check if the image ends with png and jpeg
        if image.endswith(".png") or image.endswith(".jpeg") or image.endswith(".jpg"):
            images.append(cur_path + '\\' + str(image))

    return images
