# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# start building your API here
@app.route('/games')
def games():

    games = []
    for game in Game.query.all():
        game_dict = game.to_dict()
        games.append(game_dict)

    response = make_response(
        jsonify(games),
        200
    )

    return response

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response



@app.route('/games/users/<int:id>')
def game_users_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    users = [user.to_dict(rules=("-reviews",)) for user in game.users]
    response = make_response(
        users,
        200
    )

    return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)

