import telebot
from telebot import types
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import datetime
import re
import time

token = "6222023685:AAH-eQyIBRaOloTthpc9qHc1MmbJlM20o5Q"
bot = telebot.TeleBot(token)
state = 0
selected_time = ""
selected_date = ""
phone_number = ""

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\rikx0\\Desktop\\VSHP_Bit\\vshptabl-ab4a4349b400.json", scope)
client = gspread.authorize(creds)


sheet = client.open('ВШП_Таблица_запись на пиём').sheet1
user_data = {}


date_list = []
for i in range(7):
    date = datetime.date.today() + datetime.timedelta(days=i)
    if date.weekday() not in [0, 1]:
        date_list.append(date.strftime("%d.%m.%Y"))



isfio = False


def isFio(b):
    global isfio
    isfio = b


@bot.message_handler(commands=['support'])
def support(message):
    bot.send_message(message.from_user.id,"Войдите в мобильный банк\nОткройте раздел 'переводы и платежи'\nДалее выберите 'Клиенту сбербанка'\n Затем введите счет оргранизации: ")
    bot.send_message(message.from_user.id, "40802810830000053619")
    bot.send_message(message.from_user.id, "Затем введите ИНН и БИК:")
    bot.send_message(message.from_user.id, "753600712013")
    bot.send_message(message.from_user.id, "040349602")
    bot.send_message(message.from_user.id, "Далее вводите данные по имеющимся в приложении графам\nВ назанчении платежа ОБЯЗАТЕЛЬНО укажите:ФИО учащегося и номер договора")
    bot.send_message(message.from_user.id, "Квитанцию и чек после оплаты сохраните и отправьте в электронном виде на почту nochu-cit@mail.ru или в месанджер по номеру (8 988 487 2695)")

@bot.message_handler(commands=['record'])
def handle_start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton('Записаться на собеседование')
    button1 = types.KeyboardButton('назад')
    kb.add(button)
    kb.add(button1)
    bot.send_message(message.chat.id,
                     'Добро пожаловать! Чтобы записаться на собеседование, воспользуйтесь кнопкой ниже.',
                     reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'Записаться на собеседование')
def handle_registration(message):
    kb = types.InlineKeyboardMarkup(row_width=7)
    for date in date_list:
        button = types.InlineKeyboardButton(date, callback_data=date)
        kb.add(button)
    bot.send_message(message.chat.id, 'Выберите день для собеседования:', reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data in date_list)
def handle_day_selection(call):
    bot.send_message(call.message.chat.id, "Пожалуйста подождите ")
    global selected_date
    selected_date = call.data
    kb = types.InlineKeyboardMarkup(row_width=5)
    hours = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
    if not any([is_hour_available(selected_date, hour) for hour in hours]):
        bot.send_message(call.message.chat.id, 'На этот день нет свободного времени')
        return
    for hour in hours:
        if is_hour_available(selected_date, hour):
            button = types.InlineKeyboardButton(hour, callback_data=hour)
            kb.add(button)
    bot.send_message(call.message.chat.id, 'Выберите время для собеседования:', reply_markup=kb)
    bot.answer_callback_query(call.id, text='')
def is_hour_available(date, hour):
    cell_list = sheet.findall(date)
    for cell in cell_list:
        if sheet.cell(cell.row, cell.col + 1).value == hour:
            return False
    return True


@bot.callback_query_handler(
    func=lambda call: call.data in ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'])
def handle_time_selection(call):
    global selected_time
    selected_time = call.data
    bot.send_message(call.message.chat.id, 'Введите ваше ФИО:')

    isFio(True)



@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    global state
    if state < 7:
        state += 1
    else:
        state = 0

    if state == 1:
        with open("Антон.jpg", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo,caption="__АНТОН ВИКТОРОВИЧ__. \nВыпускник Санкт-Петербургского института внешнеэкономических связей, экономики и права + Государственное бюджетное образовательное учреждение дополнительного профессионального образования 'Институт развития образования' Краснодарского края.\n\nМентор ВШП: ПРОГРАММИРОВАНИЕ/ ПРОГРАММНАЯ ИНЖЕНЕРИЯ / РАЗРАБОТКА ИГР И ПРИЛОЖЕНИ; WEB РАЗРАБОТКА И ДИЗАЙН/ FRONTEND / BACKEND / FULLSTACK / СОЗДАНИЕ САЙТОВ;",parse_mode="Markdown")
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text='меня', callback_data='button_pressed')
            keyboard.add(btn)
            bot.send_message(call.message.chat.id, "нажми ее", reply_markup=keyboard)



    elif state == 2:
        with open("Евгений.jpg", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo,caption="ЕВГЕНИЙ ДЕНИСОВИЧ. \nВыпускник Федерального государственного бюджетного образовательного учреждения высшего образования 'Кубанский государственный университет'. \n\nМентор ВШП: WEB РАЗРАБОТКА И ДИЗАЙН / FRONTEND / BACKEND / FULLSTACK / СОЗДАНИЕ САЙТОВ")
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text='меня', callback_data='button_pressed')
            keyboard.add(btn)
            bot.send_message(call.message.chat.id, "нажми ее", reply_markup=keyboard)

    elif state == 3:
        with open("Егор.jpg", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo,caption="ЕГОР СЕРГЕЕВИЧ. \nВыпускник Национального исследовательского Нижегородского государственного университета имени Н.И. Лобачевского. \n\nМентор ВШП: СИСТЕМНОЕ АДМИНИСТРИРОВАНИЕ И DEVOPS 'СИСТЕМНАЯ ИНЖЕНЕРИЯ / SYSTEMS ENGINEERING'; ПРОГРАММИРОВАНИЕ/ ПРОГРАММНАЯ ИНЖЕНЕРИЯ / РАЗРАБОТКА ИГР И ПРИЛОЖЕНИЙ")
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text='меня', callback_data='button_pressed')
            keyboard.add(btn)
            bot.send_message(call.message.chat.id, "нажми ее", reply_markup=keyboard)

    elif state == 4:
        with open("Илья.jpg", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo,caption="ИЛЬЯ СЕРГЕЕВИЧ. \nФедеральное государственное бюджетное образовательное учреждение высшего образования 'Кубанский государственный университет' \n\nМентор ВШП: ПРОГРАММИРОВАНИЕ/ ПРОГРАММНАЯ ИНЖЕНЕРИЯ / РАЗРАБОТКА ИГР И ПРИЛОЖЕНИЙ; WEB РАЗРАБОТКА И ДИЗАЙН/ FRONTEND / BACKEND / FULLSTACK / СОЗДАНИЕ САЙТОВ;")
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text='меня', callback_data='button_pressed')
            keyboard.add(btn)
            bot.send_message(call.message.chat.id, "нажми ее", reply_markup=keyboard)

    elif state == 5:
        with open("Светлана.jpg", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo,caption="СВЕТЛАНА АНДРЕЕВНА. \nВыпускница государственного бюджетного образовательного учреждения дополнительного профессионального образования 'Институт развития образования' Краснодарского края + Образовательного учреждения профсоюзов высшего образования 'Академия труда и социальных отношений'. \n\nМентор ВШП: WEB РАЗРАБОТКА И ДИЗАЙН/ FRONTEND / BACKEND / FULLSTACK / СОЗДАНИЕ САЙТОВ; ГРАФИЧЕСКИЙ ДИЗАЙН / АРХИТЕКТ. ПРОЕКТИРОВАНИЕ И 3D / МУЛЬТИПЛИКАЦИЯ;")
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text='меня', callback_data='button_pressed')
            keyboard.add(btn)
            bot.send_message(call.message.chat.id, "нажми ее", reply_markup=keyboard)
    elif state == 6:
        with open("Станислав.jpg", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo,caption="СТАНИСЛАВ РУСЛАНОВИЧ. \nВыпускник Кубанского государственного технологического университета +Межрегионального центра дополнительного профессионального образования 'СЭМС'. \n\nМентор ВШП: СИСТЕМНОЕ АДМИНИСТРИРОВАНИЕ И DEVOPS 'СИСТЕМНАЯ ИНЖЕНЕРИЯ / SYSTEMS ENGINEERING'")
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text='меня', callback_data='button_pressed')
            keyboard.add(btn)
            bot.send_message(call.message.chat.id, "нажми ее", reply_markup=keyboard)
    elif state == 7:
        with open("Фавоур.jpg", "rb") as photo:
            bot.send_photo(call.message.chat.id, photo,caption="ФАВОУР ДАМИЛАРЕ. \nФедеральное государственное бюджетное образовательное учреждение высшего образования 'Кубанский государственный технологический университет'. \n\nМентор ВШП: АНГЛИЙСКИЙ ЯЗЫК / РАЗГОВОРНЫЙ / ДЕЛОВОЙ / ТЕХНИЧЕСКИЙ")
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton(text='меня', callback_data='button_pressed')
            keyboard.add(btn)
            bot.send_message(call.message.chat.id, "нажми ее", reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def get_text_message(message):

    if message.text == "О Школе":
        keys_13 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Что вы получаете")
        key2 = types.InlineKeyboardButton("Формы обучения")
        key3 = types.InlineKeyboardButton("Преподователи")
        key4 = types.InlineKeyboardButton("Методы обучения")
        key5 = types.InlineKeyboardButton("Контакты")
        key6 = types.InlineKeyboardButton("Мы в соц.сетях")
        key7 = types.InlineKeyboardButton("назад")
        keys_13.add(key1, key2)
        keys_13.add(key3, key4)
        keys_13.add(key5, key6)
        keys_13.add(key7)
        bot.send_message(message.chat.id, "Выберите одну из опций:", reply_markup=keys_13)

    if message.text == "Преподователи":
        keyboard = types.InlineKeyboardMarkup()
        btn=types.InlineKeyboardButton(text='Меня', callback_data='button_pressed')
        keyboard.add(btn)

        bot.send_message(message.chat.id, "Нажми ее", reply_markup=keyboard)

    if message.text == "Контакты":
        with open("XXXL.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo,caption="Тел.: +7 988 487 26 95 (центр);\nул. Базовская 254, Краснодар (Центральный район)\nЯндекс Карты:https://clck.ru/356pnp ",parse_mode="Markdown")
        bot.send_message(message.chat.id,"Тел.: +7 918 335 66 64 (кмр);\nул.Сормовская 163/1, Краснодар (Комсомольский район)")
        bot.send_message(message.chat.id,"График работы учебной части: со среды по воскресенье\nс 10:00 до 18:00 \nВыходные: понедельник и вторник")
        bot.send_message(message.chat.id,"email: nochu-cit@mail.ru")


    if message.text == "Мы в соц.сетях":
        key27 = types.InlineKeyboardMarkup()
        btn_vk = types.InlineKeyboardButton(text='VK', url='https://vk.com/school_programm_krd')
        btn_Instagram= types.InlineKeyboardButton(text='Instagram', url='https://www.instagram.com/itproger_krd/?hl=ru')
        btn_Telegram= types.InlineKeyboardButton(text='Telegram', url='https://t.me/itprogerkrd')
        btn_WhatsApp = types.InlineKeyboardButton(text='WhatsApp', url='https://wa.me/79884872695')
        btn_Dzen = types.InlineKeyboardButton(text='Dzen', url='https://dzen.ru/school_programmistov?share_to=link')
        btn_YouTube = types.InlineKeyboardButton(text='YouTube', url='https://www.youtube.com/channel/UCxXQLIaiezaCxV3pfVtPYpg')
        key27.add(btn_vk,btn_Instagram)
        key27.add()
        key27.add(btn_Telegram,btn_WhatsApp)
        key27.add()
        key27.add()
        key27.add(btn_YouTube,btn_Dzen)
        bot.send_message(message.chat.id, 'Нажмите на кнопку, чтобы перейти на сайт:', reply_markup=key27)

    if message.text == "Что вы получаете":
        keys_12 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Индивидуальный подход")
        key2 = types.InlineKeyboardButton("Портфолио к выпускному")
        key3 = types.InlineKeyboardButton("Современное образование")
        key4 = types.InlineKeyboardButton("Методы обучения")
        key5 = types.InlineKeyboardButton("Занятия в группах")
        key6 = types.InlineKeyboardButton("Домашняя работа")
        key7 = types.InlineKeyboardButton("<---")
        keys_12.add(key1)
        keys_12.add(key2)
        keys_12.add(key3)
        keys_12.add(key4,key5)
        keys_12.add(key6,key7)
        bot.send_message(message.from_user.id,"Выберите одну из опций:",reply_markup=keys_12)

    if message.text == "<---":
        keys_32 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Что вы получаете")
        key2 = types.InlineKeyboardButton("Формы обучения")
        key3 = types.InlineKeyboardButton("Преподователи")
        key4 = types.InlineKeyboardButton("Методы обучения")
        key5 = types.InlineKeyboardButton("Контакты")
        key6 = types.InlineKeyboardButton("Мы в соц.сетях")
        key7 = types.InlineKeyboardButton("назад")
        keys_32.add(key1,key2)
        keys_32.add(key3,key4)
        keys_32.add(key5,key6)
        keys_32.add(key7)
        bot.send_message(message.chat.id, "Выберите одну из опций:", reply_markup=keys_32)

    if message.text == "Индивидуальный подход":
        bot.send_message(message.chat.id,"Каждый учащийся уникален!\n\n● У нас качественная подача учебного материала доступным языком и на примерах, мы уделим одинаковое количество времени каждому. \n\n● При поступлении все абитуриенты проходят тестирование и собеседование - которое определяет их индивидуальный старт в рамках наших учебных программ. \n\n● Интерактивное оборудование в учебных аудиториях позволит сделать учебный процесс удобным, современным и интересным - это важно для современных абитуриентов.")
    if message.text == "Портфолио к выпускному":
        bot.send_message(message.chat.id,"На протяжении всего обучения наши учащиеся выполняют множество практических проектов, заданий и работ - все это становится элементами крутого портфолио, которое сопровождает Диплом.\n\n● Т.е. к окончанию школы выпускники имеют в своем арсенале не только крепкие теоретические знания, но и впечатляющие практические работы, которые не оставят равнодушными ни работодателей, ни приемные комиссии профильных высших учебных заведений!")
    if message.text == "Современное образование":
        bot.send_message(message.chat.id,"'Найди себя' : \n● Мы изучаем программирование, затем пробуем графический дизайн, после занимаемся веб разработкой а заканчиваем ремонтом и наладкой пк. \n\n● Только после того, как учащиеся получили корректное представление о профессиях, они делают осознанный выбор и далее занимаются узкопрофильно. \n\n● Изучают только профильные предметы с большим количеством практических занятий по выбранной специализации.")
    if message.text == "Методы обучения":
        bot.send_message(message.chat.id,"Основаны на личном опыте преподавателей. \n\n● Преподаватели - IT специалисты с большим опытом и талантами в педагогике. Программа обучения всегда актуальна времени, включает в себя современные инструменты, оборудование и материалы. \n\n● Программа разбита на модули, что сохраняет принцип в учебном процессе: 'от простого к сложному'.")
    if message.text == "Занятия в группах":
        bot.send_message(message.chat.id,"Группа—лучший способ обучения. \nСоревновательный дух, крутое комьюнити, прокачка сильных сторон и акцент на них. \n\n● Одногруппники - это ваши единомышленники и интересные личности с общими интересами и увлечениями. \n\n● Окружение влияет - помните об этом! А еще групповые занятия это - экономно! \n\n● Стоимость одного академического часа в группе всего 412 рублей (таких цен давно уже нет даже у репетиторов по школьным предметам...). \nКачественное образование доступно для всех!")
    if message.text == "Домашняя работа":
        bot.send_message(message.chat.id,"Задания на дом выдаются по практическим проектам для закрепления полученных навыков без помощи преподавателя или одногруппников. \n\n● Она не займет много времени, а еще она интересная. \nБольшой плюс для родителей наших учащихся - это то, что в учебном процессе участвует ТОЛЬКО школа и ученик, родитель наслаждается потрясающими результатами и новыми достижениями своего чада! \n\n● У нас есть ежемесячный табель успеваемости каждого учащегося, а также рейтинг в группе для дополнительной мотивации и соревновательного духа!")


    if message.text=="Формы обучения":
        bot.send_message(message.chat.id,"● Мы обучаем детей с 10 лет, подростков, молодежь и взрослых.\n● В процессе обучения подача учебного материала адаптирована для всех, рассчитана на учеников с нулевой подготовкой и с имеющейся базой в сфере IT.\n ● Учебный процесс насыщен практикой и разнообразен, он включает в себя блоки теоретических занятий, практические / семинарские занятия - которым отдается львиная доля учебной программы. \nТак же наши учащиеся получают домашние задания, сдают контрольные срезы, зачеты и экзамены, защищают курсовые и дипломные проекты.\n● "
                                         "Заниматься можно offline (живой формат обучения с посещением школы),и online (дистанционный формат образования: живые уроки но онлайн")


    if message.text == "help":
        bot.send_message(message.chat.id, "Я бот Высшей Школы Программирования.")
        bot.send_message(message.chat.id, "Часто задаваемые вопросы")
        key45 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_1 = types.InlineKeyboardButton("сколько стоят занятия")
        btn_2 = types.InlineKeyboardButton("когда начало обучения?")
        btn_3 = types.InlineKeyboardButton("как поступить в школу?")
        btn_4 = types.InlineKeyboardButton("где находиться школа?")
        btn_5 = types.InlineKeyboardButton("как записаться?")
        btn_6 = types.InlineKeyboardButton("назад")
        key45.add(btn_1)
        key45.add(btn_2)
        key45.add(btn_3)
        key45.add(btn_4)
        key45.add(btn_5)
        key45.add(btn_6)
        bot.send_message(message.chat.id, 'Нажмите на кнопку, чтобы я вам помог', reply_markup=key45)




    if message.text == "Программирование":
        keys_4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Что это такое")
        key2 = types.InlineKeyboardButton("Учебная программа")
        key3 = types.InlineKeyboardButton("Результат")
        key4 = types.InlineKeyboardButton("Что вы получите после курса")
        key5 = types.InlineKeyboardButton("Стоимость курса")
        key6 = types.InlineKeyboardButton("назад")
        keys_4.add(key1,key2)
        keys_4.add(key3,key4)
        keys_4.add(key5,key6)
        bot.send_message(message.from_user.id,"Выберите одну из опций:", reply_markup=keys_4)

    if message.text == "Что это такое":
        with open("Prog_1.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo,caption="Программирование - востребованное направление нашего времени. \n\nВ учебной программе востребованные языки программирования. \nПостроение алгоритмов работы электронных устройств: от компьютеров до космических спутников. \n\nРазработка игр и программного обеспечения для компьютерных и мобильных платформ - все это входит в тематический план данного курса.")
    if message.text == "Учебная программа":
        keys_5 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("модуль 1")
        key2 = types.InlineKeyboardButton("модуль 2")
        key3 = types.InlineKeyboardButton("модуль 3")
        key4 = types.InlineKeyboardButton("модуль 4")
        key5 = types.InlineKeyboardButton("модуль 5")
        key6 = types.InlineKeyboardButton("←")
        keys_5.add(key1,key2)
        keys_5.add(key3,key4)
        keys_5.add(key5,key6)
        bot.send_message(message.from_user.id,"Выберите одну из опций:", reply_markup=keys_5)
    if message.text == "модуль 1":
        bot.send_message(message.from_user.id,"● Пользовательский курс\n● Сети. Интернет\n● Текстовый редактор\n● Табличный редактор\n● Основа верстки. HTML\n● Создание презентаций\n● Основы работы с компьютером\n● Основы программирования. Python\n● Растровая графика. Adobe Photoshop\n● Настройка и администрирование операционной системы Windows\n● Проф. ориентация\n● Бизнес - кейс\n● Защита курсового проекта\n● Экзамен")
    if message.text == "модуль 2":
        bot.send_message(message.from_user.id,"● углубление в программировании на python\n● программирование на C++\n● unreal engine\n● бизнес кейс\n● защита курсового проект")
    if message.text == "модуль 3":
        bot.send_message(message.from_user.id,"● github\n● работа с сервером sql + firebase\n● программирование на С#\n● разработка игр на unity 3D\n● бизнес кейс\n● защита курсового проекта")
    if message.text == "модуль 4":
        bot.send_message(message.from_user.id,"● java\n● разработка мобильных приложений\n● бизнес кейс\n● защита курсового проекта")
    if message.text == "модуль 5":
        bot.send_message(message.from_user.id,"● тестирование программного обеспечения / тестировщик ПО\n● 1С конфигуратор\n● машинное обучение\n● стратегия профессионального роста\n● дипломный проект")



    if message.text == "Результат":
        with open("Prog_3.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Занятия проходят 1 раз в неделю 4 ак.часа, в месяц 16 уроков. \n\nПолный срок обучения составляет 5 лет. \n\nЗа этот срок школьники получают профессиональное образование с последующей выдачей Диплома с присвоенной квалификацией «Техник-программист» - что уже по сути является готовой профессией, которой выпускник может начать зарабатывать!")

    if message.text == "Что вы получите после курса":
        with open("Prog2.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Диплом или Свидетельство о дополнительном профессиональном образовании с правом на трудоустройство 'профессия под ключ'\n\n"
                                                           "Все лекции за 5 модулей, различные сервисы и ресурсы, практические работы выполненные в период обучения - портфолио\n\n"
                                                           "Скидка 10 % на любой наш курс для вас или члена вашей семьи образование - это лучшие инвестиции")

    if message.text == "Стоимость курса":
        with open("Prog_mani.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Стоимость обучения: 6 600 р /месяц")

    if message.text == "Назад":
        bot.send_message(message.from_user.id,"назад")




    if message.text == "Web разработка":
        keys_3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Что это")
        key2 = types.InlineKeyboardButton("Чему научим")
        key3 = types.InlineKeyboardButton("Программа обучения")
        key4 = types.InlineKeyboardButton("Что вы получите")
        key5 = types.InlineKeyboardButton("Стоимость")
        key6 = types.InlineKeyboardButton("назад")
        keys_3.add(key1, key2)
        keys_3.add(key3, key4)
        keys_3.add(key5, key6)

        bot.send_message(message.from_user.id,"Выберите одну из опций:", reply_markup=keys_3)

    if message.text == "Что это":
        with open("Web_1.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Веб дизайн — это процесс создания визуальной оболочки сайта, его структуры и навигационной системы в форме макета.")

    if message.text == "Чему научим":
        with open("Web_2.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="работать с базами данных на примере MySQL\n- стилизовать сайты при помощи CSS \n- добавлять интерактивность на ваши сайты при помощи языка JavaScript\n- пользоваться инструментами, ускоряющими процесс разработки сайтов jQuery и Bootstrap и МНОГОМУ ДРУГОМУ (смотрите программу ниже!)")
    if message.text == "Программа обучения":
        keys_7 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("1 модуль")
        key2 = types.InlineKeyboardButton("2 модуль")
        key3 = types.InlineKeyboardButton("3 модуль")
        key4 = types.InlineKeyboardButton("4 модуль")
        key5 = types.InlineKeyboardButton("5 модуль")
        key6 = types.InlineKeyboardButton("⇜")
        keys_7.add(key1, key2)
        keys_7.add(key3, key4)
        keys_7.add(key5, key6)
        bot.send_message(message.from_user.id,"Выберите одну из опций:", reply_markup=keys_7)

    if message.text == "1 модуль":
        bot.send_message(message.from_user.id,"\n● Пользовательский курс\n● Сети. Интернет\n● Текстовый редактор\n● Табличный редактор\n● Основа верстки. HTML\n● Создание презентаций\n● Основы работы с компьютером\n● Основы программирования. Python\n● Растровая графика. Adobe Photoshop\n● Настройка и администрирование операционной системы Windows\n● Проф. ориентация\n● Бизнес - кейс\n● Защита курсового проекта\n● Экзамен")
    if message.text == "2 модуль":
        bot.send_message(message.from_user.id,"\n● Github\n● CSS\n● Bootstrap фреймворк\n● Разработка Ux/Ui дизайна\n● Adobe Illustrator (xd)\n● Java script\n● Курсовой проект")
    if message.text == "3 модуль":
        bot.send_message(message.from_user.id,"\n● Jquery\n● Ajax\n● React + Nodejs\n● PHP\n● Работа с сервером mysql\n● Seo оптимизация\n● Бизнес кейс\n● Курсовой проект")
    if message.text == "4 модуль":
        bot.send_message(message.from_user.id,"\n● Конструкторы для разработки сайтов\n● Django фреймворк\n● Angular фреймворк\n● Wordpress\n● CMS Joomla\n● Разработка сайта на 1C битрикс\n● Разработка сайта на Drupal\n● Бизнес кейс\n● Защита курсового проекта")
    if message.text == "5 модуль":
        bot.send_message(message.from_user.id,"\n● Vuejs\n● Rest API + Json 1\n● Тестирование ПО / тестировщик ПО\n● Интернет маркетинг\n● Стратегия профессионального роста\n● Бизнес кейс\n● Защита дипломного проекта")

    if message.text == "Что вы получите":
        with open("Vse_diplom.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Выпускники получают диплом о дополнительном профессиональном образовании с присвоенной квалификацией по полученной it специальности")
    if message.text == "Стоимость":
        with open("Web_3.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="\n●Год '200' уроков в семестре 79 200р\n● Месяц '16 уроков в месяц' 6 600р \n● Полгода '100' уроков 39 600р")




    if message.text == "⇜":
        keys_8 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Что это")
        key2 = types.InlineKeyboardButton("Чему научим")
        key3 = types.InlineKeyboardButton("Программа обучения")
        key4 = types.InlineKeyboardButton("Что вы получите")
        key5 = types.InlineKeyboardButton("Стоимость")
        key6 = types.InlineKeyboardButton("назад")
        keys_8.add(key1, key2)
        keys_8.add(key3, key4)
        keys_8.add(key5, key6)

        bot.send_message(message.from_user.id,"Выберите одну из опций:", reply_markup=keys_8)


    if message.text == "←":
        keys_6 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Что это такое")
        key2 = types.InlineKeyboardButton("Учебная программа")
        key3 = types.InlineKeyboardButton("Результат")
        key4 = types.InlineKeyboardButton("Что вы получите после курса")
        key5 = types.InlineKeyboardButton("Стоимость курса")
        key6 = types.InlineKeyboardButton("назад")
        keys_6.add(key1, key2)
        keys_6.add(key3, key4)
        keys_6.add(key5, key6)

        bot.send_message(message.from_user.id,"Выберите одну из опций:", reply_markup=keys_6)

    if message.text == "назад":
        keys_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("help")
        key2 = types.InlineKeyboardButton("Программирование")
        key3 = types.InlineKeyboardButton("Web разработка")
        key4 = types.InlineKeyboardButton("Кибребезопасность")
        key5 = types.InlineKeyboardButton("Графический дизайн")
        key6 = types.InlineKeyboardButton("О Школе")
        key7 = types.InlineKeyboardButton("FAQ")
        key8 = types.InlineKeyboardButton("Английский язык")
        key9 = types.InlineKeyboardButton("IT Kids")
        key10 = types.InlineKeyboardButton("Записаться на собеседование")
        key11 = types.InlineKeyboardButton("Реквизиты")
        key12 = types.InlineKeyboardButton("Очная ускоренная форма обучения")
        keys_2.add(key10)
        keys_2.add(key2, key3)
        keys_2.add(key4, key5)
        keys_2.add(key12)
        keys_2.add(key8, key11, key9)
        keys_2.add(key6, key1, key7)


        bot.send_message(message.from_user.id, "Выберите одну из опций:", reply_markup=keys_2)



    if message.text == "Кибребезопасность":
        keys_9 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Что_это")
        key2 = types.InlineKeyboardButton("Чему_научим")
        key3 = types.InlineKeyboardButton("Программа_обучения")
        key4 = types.InlineKeyboardButton("Что_вы_получите?")
        key5 = types.InlineKeyboardButton("Стоимость$")
        key6 = types.InlineKeyboardButton("назад")
        keys_9.add(key1, key2)
        keys_9.add(key3, key4)
        keys_9.add(key5, key6)
        bot.send_message(message.from_user.id, "Выберите одну из опций:",reply_markup=keys_9)

    if message.text == "Что_это":
        with open("Kiber_1.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Систе́мный администра́тор, IT-администратор — работник, должностные обязанности которого подразумевают обеспечение штатной работы парка компьютерной техники, сети и программного обеспечения.")

    if message.text == "Чему_научим":
        with open("Kiber_2.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="● Администрировать операционные системы windows linux\n● заниматься информационной безопасностью\n● Создавать и обслуживать локальные сети \n● администрировать 1с\n● Работать с базами данных и многое другое")
    if message.text == "Программа_обучения":
        keys_7 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("1_модуль")
        key2 = types.InlineKeyboardButton("2_модуль")
        key3 = types.InlineKeyboardButton("3_модуль")
        key4 = types.InlineKeyboardButton("4_модуль")
        key5 = types.InlineKeyboardButton("5_модуль")
        key6 = types.InlineKeyboardButton("↫")
        keys_7.add(key1, key2)
        keys_7.add(key3, key4)
        keys_7.add(key5, key6)
        bot.send_message(message.from_user.id, "Выберите одну из опций:",reply_markup=keys_7)

    if message.text == "1_модуль":
        bot.send_message(message.from_user.id,"\n● Пользовательский курс\n● Сети. Интернет\n● Текстовый редактор\n● Табличный редактор\n● Основа верстки. HTML\n● Создание презентаций\n● Основы работы с компьютером\n● Основы программирования. Python\n● Растровая графика. Adobe Photoshop\n● Настройка и администрирование операционной системы Windows\n● Проф. ориентация\n● Бизнес - кейс\n● Защита курсового проекта\n● Экзамен")
    if message.text == "2_модуль":
        bot.send_message(message.from_user.id,"\n● Аппаратное обеспечение\n● Служба удаленного доступа\n● Администрирование баз данных\n● SQL\n● Локальные вычислительные сети\n● Сети и телекоммуникационное оборудование\n● Бизнес кейс\n● Защита курсового проекта")
    if message.text == "3_модуль":
        bot.send_message(message.from_user.id,"\n● Администрирование WinServer\n● Система управления базами данных MSAccess\n● Администрирование Linux (Ubuntu)\n● PowerShell\n● Резервное копирование / данных\n● Бизнес кейс\n● Защита курсового проекта")
    if message.text == "4_модуль":
        bot.send_message(message.from_user.id,"\n● Методики расследования хакерских инцидентов\n● Информационная безопасность\n● Бизнес кейс\n● Защита курсового проекта")
    if message.text == "5_модуль":
        bot.send_message(message.from_user.id,"\n● Администрирование 1С\n● Тестирование ПО / Тестировщик\n● Работа С Web серверами / сервисами\n● Microtik / Cisco\n● API телефония / АТС\n● Стратегия профессионального роста\n● Бизнес кейс\n● Защита дипломного проекта")

    if message.text == "Что_вы_получите?":
        with open("Vse_diplom.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Выпускники получают диплом о дополнительном профессиональном образовании с присвоенной квалификацией по полученной it специальности")
    if message.text == "Стоимость$":
        with open("Kiber_3.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="\n●Год '192' уроков в семестре 79 200р\n● Месяц '16 уроков в месяц' 6 600р \n● Семестр '96'уроков 39 600р")



    if message.text == "/start":
        bot.send_message(message.from_user.id, "Добро пожаловать в высшую школу программирования! ")

        keys_22 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("help")
        key2 = types.InlineKeyboardButton("Программирование")
        key3 = types.InlineKeyboardButton("Web разработка")
        key4 = types.InlineKeyboardButton("Кибребезопасность")
        key5 = types.InlineKeyboardButton("Графический дизайн")
        key6 = types.InlineKeyboardButton("О Школе")
        key7 = types.InlineKeyboardButton("FAQ")
        key8 = types.InlineKeyboardButton("Английский язык")
        key9 = types.InlineKeyboardButton("IT Kids")
        key10 = types.InlineKeyboardButton("Записаться на собеседование")
        key11 = types.InlineKeyboardButton("Реквизиты")
        key12 = types.InlineKeyboardButton("Очная ускоренная форма обучения")
        keys_22.add(key10)
        keys_22.add(key2, key3)
        keys_22.add(key4, key5)
        keys_22.add(key12)
        keys_22.add(key8,key11, key9)
        keys_22.add(key6, key1, key7)

        bot.send_message(message.from_user.id, "Выберите одну из опций:", reply_markup=keys_22)


    if message.text == "↫":
        keys_10 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Что_это")
        key2 = types.InlineKeyboardButton("Чему_научим")
        key3 = types.InlineKeyboardButton("Программа_обучения")
        key4 = types.InlineKeyboardButton("Что_вы_получите")
        key5 = types.InlineKeyboardButton("Стоимость$")
        key6 = types.InlineKeyboardButton("назад")
        keys_10.add(key1, key2)
        keys_10.add(key3, key4)
        keys_10.add(key5, key6)
        bot.send_message(message.from_user.id, "Выберите одну из опций:",reply_markup=keys_10)


    if message.text == "Графический дизайн":
        keys_9 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Почему дизайн?")
        key2 = types.InlineKeyboardButton("Выпускников ждет")
        key3 = types.InlineKeyboardButton("Программа_Обучения")
        key4 = types.InlineKeyboardButton("Что_вы_получите")
        key5 = types.InlineKeyboardButton("Стоимость＄")
        key6 = types.InlineKeyboardButton("назад")
        keys_9.add(key1, key2)
        keys_9.add(key3, key4)
        keys_9.add(key5, key6)
        bot.send_message(message.from_user.id,"Выберите одну из опций:",reply_markup=keys_9)

    if message.text == "Почему дизайн?":
        with open("Graf_1.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Всё что нас окружает в повседневной жизни, идеи, макеты, реклама, здания...\n\nГрафический дизайн как дисциплину можно отнести к числу художественных и профессиональных дисциплин, фокусирующих на визуальной коммуникации и представлении. \n\nРазработка фирменного стиля, дизайн интерьера, обработка видео, работа над спецэффектами.")

    if message.text == "Выпускников ждет":
        with open("Graf_2.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="По окончанию нашей Школы выпускников ждет головокружительная карьера в любых направлениях графического дизайна:\n●  Дизайн бюро\n● Архитектурная отрасль\n● Web-студии\n● Студии разработки игр или приложений\n● Любые ИТ компании\n● Рекламные агентства\n● Гос корпорации\n● Частные компании\n● Абсолютно в любой организации есть отдел дизайна и вы там точно понадобитесь")
    if message.text == "Программа_Обучения":
        keys_7 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("1 Модуль")
        key2 = types.InlineKeyboardButton("2 Модуль")
        key3 = types.InlineKeyboardButton("3 Модуль")
        key4 = types.InlineKeyboardButton("4 Модуль")
        key5 = types.InlineKeyboardButton("5 Модуль")
        key6 = types.InlineKeyboardButton("<--")
        keys_7.add(key1, key2)
        keys_7.add(key3, key4)
        keys_7.add(key5, key6)
        bot.send_message(message.from_user.id, "Выберите одну из опций:", reply_markup=keys_7)

    if message.text == "1 Модуль":
        bot.send_message(message.from_user.id,"\n● Пользовательский курс\n● Сети. Интернет\n● Текстовый редактор\n● Табличный редактор\n● Основа верстки. HTML\n● Создание презентаций\n● Основы работы с компьютером\n● Основы программирования. Python\n● Растровая графика Adobe Photoshop\n● Настройка и администрирование операционной системы Windows\n● Проф. ориентация\n● Бизнес - кейс\n● Защита курсового проекта\n● Экзамен")
    if message.text == "2 Модуль":
        bot.send_message(message.from_user.id,"\n● Adobe Photoshop\n● Технология создания компьютерных шрифтов\n● Создание цветовых схем\n● Ux/Ui дизайн / разработка\n● Indesign\n● Blender\n● Защита курсового проекта")
    if message.text == "3 Модуль":
        bot.send_message(message.from_user.id,"\n● Corel Draw\n● Cinema 4D\n● Adobe After Effects\n● Autocad\n● Защита курсового проекта")
    if message.text == "4 Модуль":
        bot.send_message(message.from_user.id,"\n● Archicad\n● Adobe Illustrator\n● Adobe Premiere Pro\n● Sony Vegas\n● Бизнес кейс\n● Защита курсового проекта")
    if message.text == "5 Модуль":
        bot.send_message(message.from_user.id,"\n● Z Brush\n● 3D Max\n● Стратегия профессионального роста\n● Бизнес кейс\n● Защита дипломного проекта")
    if message.text == "Что_вы_получите":
        with open("Vse_diplom.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Выпускники получают диплом о дополнительном профессиональном образовании с присвоенной квалификацией по полученной it специальности")
    if message.text == "Стоимость＄":
        with open("Graf_3.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="\n●Год '192' уроков в семестре 79 200р\n● Месяц '16 уроков в месяц' 6 600р \n● Полгода '96'уроков 39 600р")

    if message.text == "<--":
        keys_11 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Почему дизайн?")
        key2 = types.InlineKeyboardButton("Выпускников ждет")
        key3 = types.InlineKeyboardButton("Программа_Обучения")
        key4 = types.InlineKeyboardButton("Что_вы_получите")
        key5 = types.InlineKeyboardButton("Стоимость＄")
        key6 = types.InlineKeyboardButton("назад")
        keys_11.add(key1, key2)
        keys_11.add(key3, key4)
        keys_11.add(key5, key6)
        bot.send_message(message.from_user.id, "Выберите одну из опций:", reply_markup=keys_11)


    if message.text == "FAQ":
        keys_29 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Диплом?")
        key2 = types.InlineKeyboardButton("Расписание?")
        key3 = types.InlineKeyboardButton("Преподаватели?")
        key4 = types.InlineKeyboardButton("До какого числа подавать документы?")
        key5 = types.InlineKeyboardButton("Какие вступительные испытания?")
        key6 = types.InlineKeyboardButton("Есть занятия дистанционно?")
        key7 = types.InlineKeyboardButton("назад")
        keys_29.add(key1,key2)
        keys_29.add(key3)
        keys_29.add(key4)
        keys_29.add(key5,key6)
        keys_29.add(key7)
        bot.send_message(message.from_user.id, "Выберите одну из опций:", reply_markup=keys_29)
    if message.text == "Диплом?":
        bot.send_message(message.from_user.id,"Выпускники получают диплом установленного образца с присвоенной квалификацией - с ним можно трудоустраиваться и смело работать! \nТы готовый специалист! \n\nА еще, с ним можно поступать в профильные вузы с огромным преимуществом на фоне остальных абитуриентов.")
    if message.text == "Расписание?":
        bot.send_message(message.from_user.id,"Занятия проходят в группах, есть утренние, дневные и вечерние. \n\nДля работающих прекрасно подойдут вечерние группы (с 18-00 до 21-00). \n\nВремя занятий утверждается на 1 учебный год и далее может меняться ( не переживайте, всегда исходим из интересов и удобства учащихся). \n\nДни занятий: ср, чт, пт - живые занятия в школе, пн и вт - дни самообучения (выполнение домашних заданий, подготовка к зачетам и экзаменам и т.д.), а сб и вс - выходные.")
    if message.text == "Преподаватели?":
        bot.send_message(message.from_user.id,"У нас прекрасный штат менторов, они квалифицированы, опытны и по своему опыту знают что и как нужно изучить, чтобы работать в IT. \n\nМы не сотрудничаем с совместителями, наш педагогический состав - это профессионалы которые полностью отдаются педагогике и посвящают себя своим учащимся.")
    if message.text == "До какого числа подавать документы?":
        bot.send_message(message.from_user.id,"Прием документов осуществляется до 20 августа.")
    if message.text == "Какие вступительные испытания?":
        bot.send_message(message.from_user.id,"Перед заключением договора необходимо пройти устное собеседование и электронное тестирование 'основы работы с ПК'")
    if message.text == "Есть занятия дистанционно?":
        bot.send_message(message.from_user.id,"Обучение в нашей школе идеальный пример - современных подходов и инструментов в образовании. \n\nТы можешь работать, учиться, путешествовать и жить в любой точке мира. \n\nЗанятия в случае болезни, командировки или другой уважительной причины, можно посещать онлайн в режиме лайф ( вы не получаете видеозаписи, вы получаете живое занятие с возможностью коммуникации с преподавателем и группой).")


    if message.text == "Английский язык":
        keys_30 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Говори без акцента")
        key2 = types.InlineKeyboardButton("Расширяем горизонты знаний")
        key3 = types.InlineKeyboardButton("Информация для обучающихся ")
        key4 = types.InlineKeyboardButton("График занятий и цена")
        key5 = types.InlineKeyboardButton("назад")
        keys_30.add(key1)
        keys_30.add(key2)
        keys_30.add(key3)
        keys_30.add(key4)
        keys_30.add(key5)
        bot.send_message(message.from_user.id, "Выберите одну из опций:", reply_markup=keys_30)

    if message.text == "Говори без акцента":
        with open("Engl.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Результат – быстрое преодоление языкового барьера, расширение словарного запаса, правильное произношение и отсутствие характерного акцента.")
    if message.text == "Расширяем горизонты знаний":
        with open("Engl_2.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Изучайте английский язык с компетентными и интересными преподавателями\nКстати, наши преподаватели - это люди из другой культуры, что поддерживает вашу мотивацию для изучения английского\nCовременный формат разговорного клуба то, что нужно чтобы перенять в том числе и речевые обороты в повседневной жизни за рубежом")
    if message.text == "Информация для обучающихся":
        with open("Engl_3.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Обучение английскому с носителями языка обеспечит Вам превосходный уровень погружения в языковую среду. На занятиях Вы сможете лучше освоить настоящий живой английский язык, изучить множество полезных разговорных фраз и речевых оборотов, а также пополнить свой запас английским сленгом.\n\n"
                                                           "Долой бездумное заучивание и скучные занятия, знакомые всем со школьной скамьи. Мы – за живой язык и развитие коммуникативных навыков, потому предлагаем наиболее эффективную методику!\n\n"
                                                           "B1 (Intermediate)\n\nB2 (Upper-intermediate)\n\nC1 (Advanced)\n\nC2 (Proficiency)")
    if message.text == "График занятий и цена":
        with open("price.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="1)  Вы можете заниматься по выходным (всего раз в неделю приезжайте к нам или занимайтесь удаленно) \nЗа 3 часа мы будем качать ваши скилы в английском языке\n\n"
                                                           "2)  Хотите более плотного графика? \nУ нас есть группы , которые занимаются по будням - 2 раза в неделю по 1,5 часа\n\n"
                                                           "Стоимость:\nСрок обучения 8 месяцев \n96 ак.часов\n6 600 / 2 000 ₽ в месяц")


    if message.text == "IT Kids":
        keys_30 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Основа программы")
        key2 = types.InlineKeyboardButton("Программа")
        key5 = types.InlineKeyboardButton("назад")
        keys_30.add(key1)
        keys_30.add(key2)
        keys_30.add(key5)
        bot.send_message(message.from_user.id, "Выберите одну из опций:", reply_markup=keys_30)

    if message.text == "Основа программы":
        with open("Deti_1.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="В основе программы — проектный подход и интенсивная практика: \n\nдети научатся реализовывать свои проекты и презентовать их, займутся разработкой компьютерных игр под руководством экспертов, будут изучать основы графического дизайна,мы посвятим их в тонкости 3D моделирования, дадим возможность самостоятельно сверстать свой первый сайти введём их в мир видеоблогинга!")
    if message.text == "Программа":
        keys_33 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Лайт")
        key2 = types.InlineKeyboardButton("Профи")
        key3 = types.InlineKeyboardButton("<----")
        keys_33.add(key1,key2)
        keys_33.add(key3)
        bot.send_message(message.from_user.id, "Выберите одну из опций:", reply_markup=keys_33)
    if message.text == "Лайт":
        with open("Deti_2.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="#ЛАЙТ \n● Основы работы с компьютером\n● Видеомонтаж / Переходы / Спец эффекты\n● Обработка фотографий / Ретушь / Создание артов\n● 3D моделирование / Анимация / Мультипликация\n● Разработка сайтов / Верстка / Дизайн\n● Разработка игр / Roblox\n● Создание своего блога / Видеоблогинг\n● Работа в сети / Безопасный интернет\n● Ораторское искусство / Оформление видеопрезентаций\n● Работа с графическим планшетом / Создание стикеров")
        bot.send_message(message.from_user.id,"Занятия ср(вт) и пт(чт) по 1,5 часа / июнь, июль и август\n6,600 РУБ/МЕС\nсо 2 июня по 25 августа\n50 ак.ч.")
    if message.text == "Профи":
        with open("Deti_3.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="#ПРОФИ\n● Основы работы с компьютером\n● Видеомонтаж / Переходы / Спец эффекты\n● Обработка фотографий / Ретушь / Создание артов\n● 3D моделирование / Анимация / Мультипликация\n● 25 ТЫС РУБ/СМЕНА\n● Разработка сайтов / Верстка / Дизайн\n● Разработка игр / Roblox\n● Создание своего блога / Видеоблогинг\n● Ораторское искусство / Оформление видеопрезентаций\n● Работа в сети / Безопасный интернет \n● Работа с графическим планшетом / Создание стикеров")
            bot.send_message(message.from_user.id,"Занятия проходят ср чт пт по 4 часа / смена июнь, июль и август\n25 ТЫС РУБ/СМЕНА\n● первая смена с 7 по 30 июня \n● вторая смена с 5 по 28 июля \n● третья смена со 2 по 25 августа \n60 ак.ч")
    if message.text == "<----":
        keys_34 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Основа программы")
        key2 = types.InlineKeyboardButton("Программа")
        key5 = types.InlineKeyboardButton("назад")
        keys_34.add(key1)
        keys_34.add(key2)
        keys_34.add(key5)
        bot.send_message(message.from_user.id, "Выберите одну из опций:", reply_markup=keys_34)

    if message.text == "Реквизиты":
        bot.send_message(message.from_user.id,"Реквизиты для оплаты:\n"
                                                    "Индивидуальный Предприниматель\n" 
                                                    "Бояркин Анатолий Анатольевич\n"
                                                    "«Высшая школа программирования»\n"
                                                    "Адрес: Россия, 350002, Краснодарский край, г. Краснодар, ул. Базовская, дом 254.\n"
                                                    "E-mail: nochu-cit@mail.ru")
        bot.send_message(message.from_user.id,"ИНН 753600712013 \nОГРН 319237500024062")
        bot.send_message(message.from_user.id,"Телефон.: +7 (988) 487-26-95")
        bot.send_message(message.from_user.id,"http://it-proger.com/")
        bot.send_message(message.from_user.id,"Если вам нужна помошь в заполнении нажмите на слово -> /support")

    if message.text =="Очная ускоренная форма обучения":
        bot.send_message(message.from_user.id, "ТЫ МОЖЕШЬ получить профессию, знания, навыки и диплом ВСЕГО за 2 года вместо 5 лет университета или 4х лет колледжа")
        keys_31 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.InlineKeyboardButton("Что вы получаете")
        key3 = types.InlineKeyboardButton("Стоимость ускоренного курса")
        key4 = types.InlineKeyboardButton("Программирование")
        key5 = types.InlineKeyboardButton("Web разработка")
        key6 = types.InlineKeyboardButton("Кибребезопасность")
        key7 = types.InlineKeyboardButton("Графический дизайн")
        key8 = types.InlineKeyboardButton("назад")
        keys_31.add(key1)
        keys_31.add(key3)
        keys_31.add(key4,key5)
        keys_31.add(key6,key7)
        keys_31.add(key8)
        bot.send_message(message.from_user.id, "Выберите одну из опций:", reply_markup=keys_31)

    if message.text == "Стоимость ускоренного курса":
        bot.send_message(message.from_user.id,"Месяц:\n 48 занятий в месяц \nоплата строго до 25 числа каждого месяца")
        bot.send_message(message.from_user.id,"Семестр:\n 288 занятий в семестре \n5 модулей длительность всей учебной программы")
        bot.send_message(message.from_user.id,"Год:\n576 занятий в модуле за 2 года вы получаете 1152 академических часа концентрированного материала и практики")




    if message.text.lower() == "когда начало обучения?" or message.text.lower() == "когда начало обучения" or message.text.lower() == " начало обучения?" or message.text.lower() == " начало обучения":
        bot.send_message(message.from_user.id,"Занятия проходят в группах, есть утренние, дневные и вечерние. \n\nДля работающих прекрасно подойдут вечерние группы (с 18-00 до 21-00). \n\nВремя занятий утверждается на 1 учебный год и далее может меняться ( не переживайте, всегда исходим из интересов и удобства учащихся). \n\nДни занятий: ср, чт, пт - живые занятия в школе, пн и вт - дни самообучения (выполнение домашних заданий, подготовка к зачетам и экзаменам и т.д.), а сб и вс - выходные.")

    if message.text.lower() == "как поступить в высшую школу программирования?" or message.text.lower() == "как поступить в школу?" or message.text.lower() == "как поступить в высшую школу программирования" or message.text.upper() == "Как поступить в школу":
        bot.send_message(message.chat.id,"К нам поступить очень легко. \nЗаписываетесь на собеседование спомощью бота или по телефону ")
        bot.send_message(message.chat.id,"+7 988 487-26-95")

    if message.text.lower() == "где находиться школа?" or message.text.lower() == "где находиться школа" or message.text.lower() == "где находиться?" or message.text.lower() == "где находиться" or message.text.lower() == "пересечение улиц?" or message.text.lower() == "пересечение улиц":
        with open("XXXL.jpg", "rb") as photo:
            bot.send_photo(message.chat.id, photo,caption="Тел.: +7 988 487 26 95 (центр);\nул. Базовская 254, Краснодар (Центральный район)\nЯндекс Карты:https://clck.ru/356pnp ",parse_mode="Markdown")
        bot.send_message(message.chat.id,"Тел.: +7 918 335 66 64 (кмр);\nул.Сормовская 163/1, Краснодар (Комсомольский район)")
        bot.send_message(message.chat.id,"График работы учебной части: со среды по воскресенье\nс 10:00 до 18:00 \nВыходные: понедельник и вторник")
        bot.send_message(message.chat.id,"email: nochu-cit@mail.ru")

    if message.text.lower() == "как записаться?" or  message.text.lower() == "как записаться" or  message.text.lower() == "где записаться?" or  message.text.lower() == "где записаться":
        bot.send_message(message.chat.id,"Чтобы записаться на собеседование вы можете нажать на /record и зписаться в этом чате")
        bot.send_message(message.chat.id,"Или позвонить по номеру")
        bot.send_message(message.chat.id,"+7 988 487-26-95")


    if  message.text.lower() == "сколько стоят занятия" or message.text.lower() == "цена" or message.text.lower() == "стоимость занятий" or message.text.lower() == "стоимость занятий?" or message.text.lower() == "цена?":
        key44 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_1 = types.InlineKeyboardButton('Цена Програмирования')
        btn_2 = types.InlineKeyboardButton('Цена Web разработки')
        btn_3 = types.InlineKeyboardButton('Цена Кибербезопасности')
        btn_4 = types.InlineKeyboardButton('Цена Графического Дизайна')
        btn_5 = types.InlineKeyboardButton('<------')
        key44.add(btn_1)
        key44.add(btn_2)
        key44.add(btn_3)
        key44.add(btn_4)
        key44.add(btn_5)
        bot.send_message(message.chat.id, 'Нажмите на кнопку, чтобы перейти узнать цену', reply_markup=key44)

    if message.text == "<------":
        key46 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_1 = types.InlineKeyboardButton("сколько стоят занятия")
        btn_2 = types.InlineKeyboardButton("когда начало обучения?")
        btn_3 = types.InlineKeyboardButton("как поступить в школу?")
        btn_4 = types.InlineKeyboardButton("где находиться школа?")
        btn_5 = types.InlineKeyboardButton("как записаться?")
        btn_6 = types.InlineKeyboardButton("назад")
        key46.add(btn_1)
        key46.add(btn_2)
        key46.add(btn_3)
        key46.add(btn_4)
        key46.add(btn_5)
        key46.add(btn_6)
        bot.send_message(message.chat.id, 'Нажмите на кнопку, чтобы я вам помог', reply_markup=key46)

    if message.text == 'Цена Програмирования':
        with open("Prog_mani.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo, caption="Стоимость обучения: 6 600 р /месяц")

    if message.text == 'Цена Web разработки':
        with open("Web_3.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo,
                           caption="\n●Год '200' уроков в семестре 79 200р\n● Месяц '16 уроков в месяц' 6 600р \n● Полгода '100' уроков 39 600р")

    if message.text == 'Цена Кибербезопасности':
        with open("Kiber_3.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo,
                           caption="\n●Год '192' уроков в семестре 79 200р\n● Месяц '16 уроков в месяц' 6 600р \n● Семестр '96'уроков в семестре 39 600р")

    if message.text == 'Цена Графического Дизайна':
        with open("Graf_3.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo,
                           caption="\n●Год '192' уроков в семестре 79 200р\n● Месяц '16 уроков в месяц' 6 600р \n● Полгода '96'уроков 39 600р")

    if isfio:
        global selected_time, selected_date, phone_number,user_info

        user_info = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton("Отправить номер телефона", request_contact=True)
        markup.add(item1)
        bot.send_message(message.chat.id, 'Нажмите на кнопку "Отправить номер телефона" чтобы мы могли с вами связаться', reply_markup=markup)



@bot.message_handler(content_types=['contact'])
def save_phone_number(message):
    global selected_time, selected_date, phone_number, user_info

    phone_number = message.contact.phone_number
    print(phone_number)
    row = [selected_date, selected_time, user_info,phone_number]
    sheet.append_row(row)
    bot.send_message(message.chat.id, f'Вы успешно запланировали собеседование на {selected_date} в {selected_time}.')

    keys_41 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key1 = types.InlineKeyboardButton("help")
    key2 = types.InlineKeyboardButton("Программирование")
    key3 = types.InlineKeyboardButton("Web разработка")
    key4 = types.InlineKeyboardButton("Кибребезопасность")
    key5 = types.InlineKeyboardButton("Графический дизайн")
    key6 = types.InlineKeyboardButton("О Школе")
    key7 = types.InlineKeyboardButton("FAQ")
    key8 = types.InlineKeyboardButton("Английский язык")
    key9 = types.InlineKeyboardButton("IT Kids")
    key10 = types.InlineKeyboardButton("Записаться на собеседование")
    key11 = types.InlineKeyboardButton("Реквизиты")
    key12 = types.InlineKeyboardButton("Очная ускоренная форма обучения")
    keys_41.add(key10)
    keys_41.add(key2, key3)
    keys_41.add(key4, key5)
    keys_41.add(key12)
    keys_41.add(key8, key11, key9)
    keys_41.add(key6, key1, key7)
    bot.send_message(message.from_user.id, "Выберите одну из опций:", reply_markup=keys_41)

    selected_time = ""
    selected_date = ""
    phone_number = ""

    isFio(False)


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)

        except Exception as e:
            print(e)
            time.sleep(15)



driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'my_test_address@gmail.com'},
    fields = 'id'
).execute()


