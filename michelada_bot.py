from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder='assets')

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

@app.route('/')
def index():
    return render_template('index.html', recipes=recipes)

@app.route('/recipe/<name>', methods=['GET'])
def get_recipe(name):
    recipe = recipes.get(name, {})
    return jsonify(recipe)

if __name__ == '__main__':
    app.run(debug=True)
