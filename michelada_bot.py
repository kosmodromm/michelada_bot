import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

API_TOKEN = '7416668237:AAHUaBCu5OmZXuoR6AEZ245zOR_WXMvu840'

bot = telebot.TeleBot(API_TOKEN)

recipes = {
    "Classic": {
        "description": "The classic michelada is a traditional Mexican cocktail based on beer, lime and Worcestershire sauce.",
        "ingredients": "Beer, lime juice, Worcestershire sauce, Tabasco sauce, salt, pepper.",
        "image": "assets/classic_michelada.jpg"
    },
    "Spicy": {
        "description": "Spicy michelada is for those who like it spicy! Add more Tabasco and enjoy the fiery flavor.",
        "ingredients": "Beer, lime juice, Tabasco sauce, chili, salt and pepper.",
        "image": "assets/spicy_michelada.jpg"
    },
    "Fruit": {
        "description": "Fruity michelada is a refreshing and sweet version with added fruit.",
        "ingredients": "Beer, lime juice, mango juice, strawberries, salt and pepper.",
        "image": "assets/fruit_michelada.jpg"
    }
}

# Main page
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    for recipe_name in recipes.keys():
        markup.add(InlineKeyboardButton(recipe_name, callback_data=f"select_{recipe_name}"))

    bot.send_photo(message.chat.id, open('assets/michelada_main.jpg', 'rb'),
                   caption="Choose the type of michelada to get the recipe!",
                   reply_markup=markup)

# Processing of the michelada selection
@bot.callback_query_handler(func=lambda call: call.data.startswith('select_'))
def show_recipe(call):
    recipe_name = call.data.split('_')[1]
    recipe = recipes[recipe_name]

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Description", callback_data=f"desc_{recipe_name}"))
    markup.add(InlineKeyboardButton("Ingredients", callback_data=f"ingr_{recipe_name}"))
    markup.add(InlineKeyboardButton("Back", callback_data="back"))

    bot.edit_message_media(media=InputMediaPhoto(open(recipe['image'], 'rb')),
                           chat_id=call.message.chat.id,
                           message_id=call.message.message_id,
                           reply_markup=markup)

# Display description or ingredients
@bot.callback_query_handler(func=lambda call: call.data.startswith('desc_') or call.data.startswith('ingr_'))
def show_details(call):
    recipe_name = call.data.split('_')[1]
    recipe = recipes[recipe_name]

    if call.data.startswith('desc_'):
        text = recipe['description']
    else:
        text = recipe['ingredients']

    bot.edit_message_caption(caption=text,
                             chat_id=call.message.chat.id,
                             message_id=call.message.message_id,
                             reply_markup=call.message.reply_markup)

# Back btn
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def go_back(call):
    send_welcome(call.message)

bot.polling()