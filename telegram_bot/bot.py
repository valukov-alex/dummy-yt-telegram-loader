import telebot
import os
from Constant import Constant
from postgres_id import PostgresID


def read_data(path):
    with open(path, "r") as f:
        return f.read().strip()


bot_folder = os.path.dirname(os.path.realpath(__file__))

token_path = os.path.join(bot_folder, Constant.TOKEN_PATH)
psw_path = os.path.join(bot_folder, Constant.PASSWORD_PATH)
data_folder = os.path.join(bot_folder, Constant.DATA_FOLDER)

token = read_data(token_path)
password = read_data(psw_path)

print(Constant.DB_HOST)
users_db = PostgresID(
    dbname = Constant.DB_NAME,
    user = Constant.DB_USER,
    password = Constant.DB_PASSWORD,
    host = Constant.DB_HOST,
    port = Constant.DB_PORT
)
users_db.connect_to_db()
print("connect to postgres!")

users_db.create_table(Constant.DB_TABLE_NAME)

bot = telebot.TeleBot(token)
print("start bot")


def save_data(image_data, image_type, title):
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)

    if not os.listdir(data_folder):
        data_id = 0
    else:
        data_id = max([int(id_) for id_ in os.listdir(data_folder)]) + 1
    
    data_id_folder = os.path.join(data_folder, str(data_id))
    os.mkdir(data_id_folder)

    image_path = os.path.join(data_id_folder, "image."+image_type)
    title_path = os.path.join(data_id_folder, "title.txt")
    
    with open(image_path, "wb") as f:
        f.write(image_data)
    
    with open(title_path, "w") as f:
        f.write(title)


def get_password(message):
    if message.text == password:
        users_db.insert_user(Constant.DB_TABLE_NAME, message.from_user.id)
        bot.send_message(message.from_user.id, "Найс, я тебя зарегал\nЧтобы грузануть на канал, пришли картинку и в caption название видоса.\nВидос зальется не сразу, а станет в очередь. Видосы заливаются каждые 15 мин.")
    else:
        bot.send_message(message.from_user.id, "Неверный пароль, чучело...")


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.from_user.id, "Здарова, напиши /reg, чтобы я тебя зарегал")


@bot.message_handler(content_types=['text', 'photo', 'document'])
def get_content_message(message):
    if message.text == "/reg":
        if users_db.is_user_exists(Constant.DB_TABLE_NAME, message.from_user.id):
            bot.send_message(message.from_user.id, "Дядя, я тебя уже зарегал, куда ты лезешь?")
        else:
            bot.send_message(message.from_user.id, "Давай пароль вводи")
            bot.register_next_step_handler(message, get_password)
    else:
        if not users_db.is_user_exists(Constant.DB_TABLE_NAME, message.from_user.id):
            bot.send_message(message.from_user.id, "Тебя в базе нет, зарегайся через /reg")
        else:
            if message.photo is not None:
                bot.send_message(message.from_user.id, "Пришли фото без сжатия")
            elif message.document is None:
                bot.send_message(message.from_user.id, "Пришли фотку и название, токо не сжимай")
            elif message.caption is None:
                bot.send_message(message.from_user.id, "Не вижу название ролика")
            elif message.document.mime_type.split("/")[0] != "image":
                bot.send_message(message.from_user.id, "Пришли фотку, а не другой файл")
            else:
                file_info = bot.get_file(message.document.file_id)
                image_data = bot.download_file(file_info.file_path)

                image_type = message.document.file_name.split(".")[-1]
                title = message.caption

                save_data(image_data, image_type, title)

                bot.send_message(message.from_user.id, "Супер!")

            print("caption:", message.caption)
            print("photo:", message.photo)
            print("document:", message.document)
            print("text:", message.text)
            #file_info = bot.get_file(message.document.file_id)
            #file_info = bot.get_file(message.photo[0].file_id)

bot.polling(none_stop=True, interval=0)