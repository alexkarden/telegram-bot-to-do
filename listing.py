import telebot
from telebot import types

bot = telebot.TeleBot('BOT-TOKEN')



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, '👋 Привет! Я твой To-Do бот-помощник! Одно сообщение в Телеграме - одна задача', parse_mode='html')

@bot.message_handler(content_types=['photo', 'video', 'audio', 'document'])
def start(message):
    bot.send_message(message.chat.id, 'Бот работает только с текстовыми сообщениями')


@bot.message_handler(content_types=['text'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Выполнить", callback_data='done')
    button2 = types.InlineKeyboardButton("❌ Удалить", callback_data='delete')
    markup.row(button1, button2)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, message.text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'delete':
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'done':
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("✔️ Выполнено", callback_data='undone')
        button2 = types.InlineKeyboardButton("❌ Удалить", callback_data='delete')
        markup.row(button1, button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='✅  <strike><em>'+ call.message.text+'</em></strike>', parse_mode='html',reply_markup=markup )
    elif call.data == 'undone':
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Выполнить", callback_data='done')
        button2 = types.InlineKeyboardButton("❌ Удалить", callback_data='delete')
        markup.row(button1, button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text[1:], parse_mode='html',reply_markup=markup )
bot.polling(none_stop=True)
