from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String, DateTime 
from sqlalchemy.orm import mapped_column, relationship
from db import db
from sqlalchemy.sql import functions as func
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = mapped_column(Integer, primary_key=True) 
    name = mapped_column(String(200), nullable=False, unique=True) 
    phone = mapped_column(String(20), nullable=False)
    height = mapped_column(Float, nullable=False) 
    weight = mapped_column(Float, nullable=False)
    gender = mapped_column(String(20), nullable=False)
    age = mapped_column(Integer, nullable=False)
    tdee = mapped_column(Float, nullable=True, default=2000)
    password = mapped_column(String(200), nullable=False)
    meals = relationship("Meal")

    def getTotalMacros(self):
        fat = 0
        protein = 0
        carbs = 0
        calories = 0
        for each in self.meals:
            macros = each.getMacros()
            fat += macros["fat"]
            protein += macros["protein"]
            carbs += macros["carbs"]
            calories += macros["calories"]
        return {"fat": fat, "protein": protein, "carbs": carbs, "calories": calories}

class Meal(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    user_id = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    name = mapped_column(String(200), nullable=False) 
    user = relationship("User", back_populates="meals")
    foodlist = relationship("FoodMeal", back_populates="meal")

    def getMacros(self):
        fat = 0
        protein = 0
        carbs = 0
        calories = 0
        for each in self.foodlist:
            food = each.food
            fat += food.fat * each.amount/100
            protein += food.protein * each.amount/100
            carbs += food.carbs * each.amount/100
            calories += food.calories * each.amount/100
        return {"fat": fat, "protein": protein, "carbs": carbs, "calories": calories}

class Food(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    name = mapped_column(String(200), nullable=False, unique=True) 
    calories = mapped_column(Float, nullable=False) 
    protein = mapped_column(Float, nullable=False)
    carbs = mapped_column(Float, nullable=False)
    fat = mapped_column(Float, nullable=False)

    def toDict(self):
        return {"id": self.id, "name": self.name, "calories": self.calories, "protein": self.protein, "fat": self.fat, "carbs": self.carbs}

class FoodMeal(db.Model):
    id = mapped_column(Integer, primary_key=True) 
    meal_id = mapped_column(Integer, ForeignKey(Meal.id), nullable=False)
    food_id = mapped_column(Integer, ForeignKey(Food.id), nullable=False)
    amount = mapped_column(Float, nullable=False)
    meal = relationship("Meal")
    food = relationship("Food")

# if user input about 2 eggs, that quantity will automatically be converted to 2*50g