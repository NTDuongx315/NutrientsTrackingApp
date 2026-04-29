import csv
import random
from sqlalchemy.sql import functions as func
from db import db
from models import User, Meal, Food, FoodMeal
from app import app

def GetUser():
    with open("./data/users.csv", "r") as f:
        data = csv.DictReader(f)
        for each in data:
            obj = User(name=each["name"], phone=each["phone"], 
                       height=each["height"], weight=each["weight"], 
                       gender=each["gender"], age=each["age"],
                       tdee=each["tdee"], password=each["password"])
            db.session.add(obj)
        db.session.commit()

def GetFood():
    with open("./data/food.csv", "r") as f:
        data = csv.DictReader(f)
        for each in data:
            obj = Food(name=each["name"], calories=each["calories"], 
                       protein=each["protein"], fat=each["fat"], 
                       carbs=each["carbs"])
            db.session.add(obj)
        db.session.commit()

def GetMeal():
    with open("./data/meals.csv", "r") as f:
        data = csv.DictReader(f)
        for each in data:
            obj = Meal(name=each["name"], user_id=each["user_id"])
            db.session.add(obj)
        db.session.commit()

def GetFoodMeal():
    with open("./data/foodmeal.csv", "r") as f:
        data = csv.DictReader(f)
        for each in data:
            obj = FoodMeal(meal_id=each["meal_id"], food_id=each["food_id"], 
                           amount=each["amount"])
            db.session.add(obj)
        db.session.commit()

def LoadData():
    with app.app_context():
        db.drop_all()
        db.create_all() 
        GetUser()
        GetFood()
        GetMeal()
        GetFoodMeal()

if __name__ == "__main__":
    LoadData()
    with app.app_context():
        # a = db.get_or_404(User, 2)
        # print(a.name)
        # print(a.meals)
        # for each in a.meals:
        #     print(each.name)
        #     print(each.foodlist)
        #     for food in each.foodlist:
        #         tmp = db.get_or_404(Food, food.food_id)
        #         print(f"   {tmp.id}: {tmp.name} {food.amount}g")
        #     print()
        # food_list = Food.query.all()
        # food_list_dict = [each.toDict() for each in food_list]
        # print(food_list_dict)
        pass
    app.run(debug=True, port=8888)