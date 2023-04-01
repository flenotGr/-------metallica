import io
import time
import qrcode
import requests
import base64
from PIL import Image, ImageDraw, ImageGrab, ImageFont
from io import BytesIO
import random

# https://i.ibb.co/smTnTsr/orig-1.png
API_KEY = '425570c7c51f1a2d3f25750fc1580ad6'
UPLOAD_URL = 'https://api.imgbb.com/1/upload?expiration=600&key=425570c7c51f1a2d3f25750fc1580ad6'
settings = {
    'fill_color': "Black",
    'back_color': "White",
}

btn_bg = [
    {
        "title": "Чёрный(задний фон)",
        "hide": False
    },
    {
        "title": "Красный(задний фон)",
        "hide": False
    },
    {
        "title": "Зеленый(задний фон)",
        "hide": False
    },
    {
        "title": "Голубой(задний фон)",
        "hide": False
    },
    {
        "title": "Фиолетовый(задний фон)",
        "hide": False
    },
    {
        "title": "Остановить навык",
        "hide": False
    },

]

btn_code = [
    {
        "title": "Чёрный(цвет кода)",
        "hide": False
    },
    {
        "title": "Красный(цвет кода)",
        "hide": False
    },
    {
        "title": "Зеленый(цвет кода)",
        "hide": False
    },
    {
        "title": "Голубой(цвет кода)",
        "hide": False
    },
    {
        "title": "Фиолетовый(цвет кода)",
        "hide": False
    },
    {
        "title": "Остановить навык",
        "hide": False
    },

]


def send_photo(photo_url):
    photo = requests.get(photo_url).content

    files = {'file': photo}
    headers = {
        'Authorization': 'OAuth y0_AgAAAABa5HHPAAT7owAAAADfitdQrdvCTNsaSlWYlSU58ec54PXrHbc',
    }

    response = requests.post('https://dialogs.yandex.net/api/v1/skills/6478eb06-ec79-4c6f-8676-88b0d26ca563/images/',
                             files=files, headers=headers)
    response = response.json()
    id_image = response["image"]["id"]
    return id_image


def make_rounded_qr_code(qr):
    w, h = qr.size
    # Задаем радиус закругления
    rad = 40
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    # Создаем маску с закругленными углами
    mask = Image.new('L', (w, h), 255)
    mask.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    mask.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    mask.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    mask.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    qr.putalpha(mask)
    return qr





def upload_image_to_hosting_service(image_data, filename):
    response = requests.post('https://api.imgbb.com/1/upload?expiration=600&key=425570c7c51f1a2d3f25750fc1580ad6',
                             data={
                                 'name': filename,
                                 'image': image_data
                             })
    response.raise_for_status()
    image_url = response.json()['data']['url']
    return image_url


def generate_qr_code_image(url, settings_fill, settings_back):
    link = url
    buffer = io.BytesIO()
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)

    qr.add_data(link)

    qr.make(fit=True)
    img_qr = qr.make_image(fill_color=settings_fill,
                           back_color=settings_back)
    response = requests.get("https://i.ibb.co/hYgrPwn/magicly-1679846111574.png")
    img = Image.open(BytesIO(response.content))
    # изменить формат изображения до его отображения
    img_logo = img.convert('RGB')
    width_logo, height_logo = img_logo.size

    # определяем размеры и координаты для вставки логотипа в центр qr-кода

    width_qr, height_qr = img_qr.size
    width_logo_max = int(width_qr / 7)
    height_logo_max = int(height_qr / 7)

    if width_logo > width_logo_max:
        width_logo = width_logo_max

    if width_logo < width_logo_max:
        width_logo = width_logo_max

    if height_logo > height_logo_max:
        height_logo = height_logo_max

    if height_logo < height_logo_max:
        height_logo = height_logo_max

    x_logo = int((width_qr - width_logo) / 2)
    y_logo = int((height_qr - height_logo) / 2)
    make_rounded_qr_code(img_logo)

    make_rounded_qr_code(img_qr)


    img_qr.paste(img_logo.resize((width_logo, height_logo)), (x_logo, y_logo))

    img_qr.save(buffer)
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_base64


def handler(event, context):
    if event['session']['new'] or "начать" in event['request']['original_utterance'].lower():
        text = 'Привет! Меня зовут мяу код, я навык который генерирует QR код, мяу! Для того что бы продолжить нажмите "Созать QR код".' \
 \
            # Если началась новая сессия, отправляем приветственное сообщение
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': text,
                'buttons': [
                    {
                        "title": "Что ты умеешь?",
                        "hide": False
                    },
                    {
                        "title": "Создать QR код",
                        "hide": False
                    },
                    {
                        "title": "Остановить навык",
                        "hide": False
                    }],
                'end_session': False
            }
        }
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'умеешь' in event['request'][
        'original_utterance'].lower():
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Я навык который умеет создавать QR коды. Для того что бы создать QR просто отправьте мне ссылку которую хотите преобразовать! Так же я могу немного кастомизировать ваш QR код",
                'buttons':
                    [
                        {
                            "title": "Далее: Продолжить создание QR кода",
                            "hide": False
                        },

                    ],
                'end_session': False

            }
        }

    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'созда' in event['request'][
        'original_utterance'].lower():
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Отлично, приступим к созданию QR кода! Начнем с настроек. При настройке спользовать строго кнопки. Хотите кастомизировать ваш QR код?",
                'buttons':
                    [
                        {
                            "title": "Да, хочу",
                            "hide": False
                        },
                        {
                            "title": "Нет, не хочу",
                            "hide": False
                        },
                        {
                            "title": "Остановить навык",
                            "hide": False
                        },
                    ],
                'end_session': False

            }
        }

    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'остановить' in event['request'][
        'original_utterance'].lower():
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Спасибо, что воспользовались моим навыком!",
                'end_session': True
            }
        }
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'нет, не хочу' in event['request'][
        'original_utterance'].lower():
        settings['fill_color'] = "Purple"
        settings['back_color'] = "White"
        time.sleep(0.5)
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Хорошо, отправьте мне ссылку на сайт, которую вы хотите конвертировать!",

                'end_session': False
            }
        }
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'да, хочу' in event['request'][
        'original_utterance'].lower():
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Отлично, Выберите цвет заднего фона.",
                'buttons': btn_bg,
                'end_session': False
            }
        }
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'чёрный(задний фон)' in event['request'][
        'original_utterance'].lower():
        color_bg_black = "Black"
        settings['back_color'] = color_bg_black
        time.sleep(0.5)
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Хорошо,теперь выберите цвет самого QR кода!",
                'buttons': btn_code,
                'end_session': 'false'
            }
        }

    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'красный(задний фон)' in event['request'][
        'original_utterance'].lower():
        color_bg_white = "Red"
        settings['back_color'] = color_bg_white
        time.sleep(0.5)
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Хорошо,теперь выберите цвет самого QR кода!",
                'buttons': btn_code,
                'end_session': 'false'
            }
        }
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'голубой(задний фон)' in event['request'][
        'original_utterance'].lower():
        color_bg_blue = "skyblue"
        settings['back_color'] = color_bg_blue
        time.sleep(0.5)

        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Хорошо,теперь выберите цвет самого QR кода!",
                'buttons': btn_code,
                'end_session': 'false'
            }
        }
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'фиолетовый(задний фон)' in event['request'][
        'original_utterance'].lower():
        color_bg_purple = "Purple"
        settings['back_color'] = color_bg_purple
        time.sleep(0.5)

        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Хорошо,теперь выберите цвет самого QR кода! ",
                'buttons': btn_code,
                'end_session': 'false'
            }
        }
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'зеленый(задний фон)' in event['request'][
        'original_utterance'].lower():
        color_bg_green = "Lime"
        settings['back_color'] = color_bg_green
        time.sleep(0.5)
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Хорошо,теперь выберите цвет самого QR кода!",
                'buttons': btn_code,
                'end_session': 'false'
            }
        }
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'фиолетовый(цвет кода)' in event['request'][
        'original_utterance'].lower():
        color_code_purple = "Purple"
        settings['fill_color'] = color_code_purple
        time.sleep(0.5)
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Отлично, отправьте мне ссылку на сайт, которую вы хотите конвертировать!",

                'end_session': False
            }
        }
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'чёрный(цвет кода)' in event['request'][
        'original_utterance'].lower():
        color_code_black = "Black"
        settings['fill_color'] = color_code_black
        time.sleep(0.5)
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Отлично, отправьте мне ссылку на сайт, которую вы хотите конвертировать!",

                'end_session': False
            }
        }
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'голубой(цвет кода)' in event['request'][
        'original_utterance'].lower():
        color_code_blue = "skyblue"
        settings['fill_color'] = color_code_blue
        time.sleep(0.5)
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Отлично, отправьте мне ссылку на сайт, которую вы хотите конвертировать!",

                'end_session': False
            }
        }
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'красный(цвет кода)' in event['request'][
        'original_utterance'].lower():
        color_code_white = "Red"
        settings['fill_color'] = color_code_white
        time.sleep(0.5)
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Отлично, отправьте мне ссылку на сайт, которую вы хотите конвертировать!",

                'end_session': False
            }
        }

    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'зеленый(цвет кода)' in event['request'][
        'original_utterance'].lower():
        color_code_green = "Lime"
        settings['fill_color'] = color_code_green
        time.sleep(0.5)
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': "Отлично, отправьте мне ссылку на сайт, которую вы хотите конвертировать!",

                'end_session': False
            }
        }

    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and 'текст: ' in event['request'][
        'original_utterance'].lower():
        replace_text = event['request']['original_utterance'].replace("текст: ", "")
        settings['text'] = replace_text
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': f"Отлично, отправьте мне ссылку на сайт, которую вы хотите конвертировать!{settings}",

                'end_session': False
            }
        }
    if 'request' in event and \
            'original_utterance' in event['request'] \
            and len(event['request']['original_utterance']) > 0 and '://' in event['request'][
        'original_utterance'].lower():
        time.sleep(0.5)
        image_data = generate_qr_code_image(event['request']['original_utterance'], settings['fill_color'],
                                            settings['back_color'], settings['text'])
        filename = 'qr_code.png'
        image_url1 = upload_image_to_hosting_service(image_data, filename)
        image_url2 = send_photo(image_url1)
        asb = event['request']['original_utterance']
        if len(event['request']['original_utterance']) > 120:
            asb = asb[:120]
        response = {
            "version": event['version'],
            "session": event['session'],
            "response": {
                "text": "Если вы хотите закончить сейанс напишите слово стоп",
                "card": {
                    "type": "ItemsList",
                    "header": {
                        "text": "Ваш QR код готов!"
                    },

                    "items":
                        [
                            {
                                "image_id": image_url2,
                                "title": "QR код для ссылки:",
                                "description": "{}".format(asb),
                                "button": {
                                    "text": "открыть QR",
                                    "url": image_url1,
                                }
                            }
                        ],

                    "footer":
                        {
                            "text": "Создать еще QR код",
                            "button": {
                                "text": "Создать еще QR код снова"
                            }
                        },

                    "end_session": True
                },
            }, }

        return response


    else:
        text = "Извините, я не поняла вас."
        return {
            'version': event['version'],
            'session': event['session'],
            'response': {
                'text': text,
                'buttons': [
                    {
                        "title": "Начать сначала",
                        "hide": False
                    },
                    {
                        "title": "Остановить навык",
                        "hide": False
                    },
                ],
                'end_session': 'false'
            }
        }

