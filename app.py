from flask import *

from sqlalchemy import select
from pathlib import Path
from db import db
from models import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


def updateFoolMealCSV():
    data = "meal_id,food_id,amount"
    for each in FoodMeal.query.all():
        data += f"\n{each.meal_id},{each.food_id},{each.amount}"
    with open("data/foodmeal.csv", "w") as f:
        f.write(data)

def updateMealCSV():
    data = "user_id,name"
    for each in Meal.query.all():
        data += f"\n{each.user_id},{each.name}"
    with open("data/meals.csv", "w") as f:
        f.write(data)
    updateFoolMealCSV()

def updateUsersCSV():
    data = "name,phone,height,weight,gender,age,tdee,password"
    for each in User.query.all():
        data += f"\n{each.name},{each.phone},{each.height},{each.weight},{each.gender},{each.age},{each.tdee},{each.password}"
    with open("data/users.csv", "w") as f:
        f.write(data)

def updateFoodCSV():
    data = "name,calories,protein,fat,carbs"
    for each in Food.query.all():
        data += f"\n{each.name},{each.calories},{each.protein},{each.fat},{each.carbs}"
    with open("data/food.csv", "w") as f:
        f.write(data)

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretAgileCourse"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.instance_path = Path(".").resolve()

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/addnew")
def add_new():
    return render_template("addnew.html")

@app.route("/users")
def users_list():
    statement = select(User).order_by(User.id)
    records = db.session.execute(statement)
    data = records.scalars().all()
    return render_template("users.html", users = data)

@app.route("/food")
def food_list():
    statement = select(Food).order_by(Food.id)
    records = db.session.execute(statement)
    data = records.scalars().all()
    return render_template("food.html", food = data)

@app.route("/users/<int:user_id>")
@login_required
def user_info(user_id):
    statement = select(User).where(User.id == user_id)
    records = db.session.execute(statement)
    data = records.scalars().first()
    food_list = Food.query.all()
    food_list_dict = [each.toDict() for each in food_list]
    return render_template("user_info.html", user = data, food_list = food_list, food_list_dict = food_list_dict)

@app.route('/users/<int:user_id>/deletefoodmeal/<int:food_id>', methods=['POST'])
def delete_foodmeal(user_id, food_id):
    foodmeal = db.get_or_404(FoodMeal, food_id)
    db.session.delete(foodmeal)
    db.session.commit()

    updateFoolMealCSV()
    
    return redirect(url_for('user_info', user_id=user_id))

@app.route('/users/<int:user_id>/adjustfoodmeal/<int:food_id>', methods=['POST'])
def adjust_foodmeal(user_id, food_id):
    foodmeal = db.get_or_404(FoodMeal, food_id)
    foodmeal.amount = request.form["amount"]
    db.session.commit()

    updateFoolMealCSV()

    return redirect(url_for('user_info', user_id=user_id))

@app.route('/users/<int:user_id>/addfoodmeal/<int:meal_id>', methods=['POST'])
def add_foodmeal(user_id, meal_id):
    foodlist = request.form.getlist("food_id")
    amountlist = request.form.getlist("amount")
    for food_id, amount in zip(foodlist, amountlist):
        foodmeal = FoodMeal(meal_id=meal_id, food_id=food_id, amount=amount)
        db.session.add(foodmeal)
    db.session.commit()

    updateFoolMealCSV()

    return redirect(url_for('user_info', user_id=user_id))

@app.route('/users/<int:user_id>/deletemeal/<int:meal_id>', methods=['POST'])
def delete_meal(user_id, meal_id):
    meal = db.get_or_404(Meal, meal_id)
    for each in meal.foodlist:
        db.session.delete(each)
    db.session.delete(meal)
    db.session.commit()

    updateMealCSV()

    return redirect(url_for('user_info', user_id=user_id))

@app.route('/users/<int:user_id>/addmeal', methods=['POST'])
def add_meal(user_id):
    name = request.form["name"]
    foodlist = request.form.getlist("food_id")
    amountlist = request.form.getlist("amount")
    meal = Meal(name=name, user_id=user_id)
    db.session.add(meal)
    db.session.commit()

    lastmeal = db.session.query(Meal).filter(Meal.name == name).first()

    for food_id, amount in zip(foodlist, amountlist):
        foodmeal = FoodMeal(meal_id=lastmeal.id, food_id=food_id, amount=amount)
        db.session.add(foodmeal)
    db.session.commit()

    updateMealCSV()

    return redirect(url_for('user_info', user_id=user_id))

@app.route("/adduser", methods=["POST"])
def add_user():
    name = request.form["name"]
    password = request.form["password"]
    phone = request.form["phone"]
    height = request.form["height"]
    weight = request.form["weight"]
    gender = request.form["gender"]
    age = request.form["age"]
    activity_level = request.form["activity_level"]

    if gender == "male":
        bmr = 66.5 + 13.75 * int(weight) + 5.003 * int(height) - 6.75 * int(age)
    else:
        bmr = 655.1 + 9.563 * int(weight) + 1.850 * int(height) - 4.676 * int(age)
    tdee = bmr * float(activity_level)

    user = User(name=name, phone=phone, height=height, weight=weight, gender=gender, age=age, tdee=tdee, password=password)
    db.session.add(user)
    db.session.commit()

    updateUsersCSV()
    
    return redirect(url_for("login"))

@app.route("/addfood", methods=["POST"])
def add_food():
    name = request.form["name"]
    calories = request.form["calories"]
    protein = request.form["protein"]
    fat = request.form["fat"]
    carbs = request.form["carbs"]

    food = Food(name=name, calories=calories, protein=protein, fat=fat, carbs=carbs)
    db.session.add(food)
    db.session.commit()

    updateFoodCSV()

    return redirect(url_for("food_list"))

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loginpost", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    statement = select(User).where(User.name == username, User.password == password)
    records = db.session.execute(statement)
    user = records.scalars().first()

    if not user:
        flash("Invalid username or password")
        return redirect(url_for("login"))
    login_user(user)
    return redirect(url_for("user_info", user_id=user.id))

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))