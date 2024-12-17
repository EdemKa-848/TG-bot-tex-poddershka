import telebot
from config import *
from logic import *
from config import *

TOKEN = (TOKEN)
bot = telebot.TeleBot(TOKEN)



QA = {
    "Как оформить заказ?": "Для оформления заказа, пожалуйста, выберите интересующий вас товар и нажмите кнопку 'Добавить в корзину', затем перейдите в корзину и следуйте инструкциям для завершения покупки.",
    "Как узнать статус моего заказа?": "Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем сайте и перейдя в раздел 'Мои заказы'. Там будет указан текущий статус вашего заказа.",
    "Как отменить заказ?": "Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержи как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки.",
    "Что делать, если товар пришел поврежденным?": "При получении поврежденного товара, пожалуйста, сразу свяжитесь с нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара.",
    "Как связаться с вашей технической поддержкой?": "Вы можете связаться с нашей технической поддержкой через телефон на нашем сайте или написать нам в чат-бота.",
    "Как узнать информацию о доставке?": "Информацию о доставке вы можете найти на странице оформления заказа на нашем сайте. Там указаны доступные способы доставки и сроки."
}


@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Проблемы с товаром', 'Технические проблемы', 'Часто задаваемые вопросы')
    bot.send_message(message.chat.id, "Привет! Выберите область проблемы:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.lower()
    if user_text in QA:
        bot.reply_to(message, QA[user_text])
    elif user_text == 'проблемы с товаром':
        department = 'продажи'
        bot.send_message(message.chat.id, "Опишите свою проблему с товаром:")
        bot.register_next_step_handler(message, process_request, department)
    elif user_text == 'технические проблемы':
        department = 'техника'
        bot.send_message(message.chat.id, "Опишите техническую проблему:")
        bot.register_next_step_handler(message, process_request, department)
    elif user_text == 'часто задаваемые вопросы':
        faq_message = "Вот список часто задаваемых вопросов:\n\n"
        for question, answer in QA.items():
            faq_message += f"*Вопрос:* {question}\n*Ответ:* {answer}\n\n"
        bot.send_message(message.chat.id, faq_message, parse_mode='Markdown')
    else:
        bot.reply_to(message, "Извините, я не понимаю.")

    
    
        
        bot.send_message(message.chat.id, faq_message, parse_mode='Markdown')

def process_request(message, department):
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text
    add_request(user_id, username, text, department)
    bot.send_message(message.chat.id, f"Ваш запрос передан специалистам отдела {department}. Скоро с вами свяжутся.")

# Инициализация БД при запуске
setup_database()

# Запуск бота
bot.polling(none_stop=True)
