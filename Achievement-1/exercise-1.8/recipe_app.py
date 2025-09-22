import os
import sqlalchemy 
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String

#load parameters from .env 
load_dotenv()
host=os.getenv("DB_HOST")
user=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
database=os.getenv("DB_DATABASE")

#establish connection with the database
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

#example for check if connection work
with engine.connect() as connection:
    result = connection.execute(sqlalchemy.text("SELECT 1"))
    print(result.scalar())

#created session object to perform actions in the DB
Session = sessionmaker(bind = engine)
session = Session()

#created a Base object to define classes
Base = declarative_base()

#initiate a class
class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50), nullable = False)
    ingredients = Column(String(255), nullable = False)
    cooking_time = Column(Integer, nullable = False)
    difficulty = Column(String(20), nullable = True)

    def __init__ (self, name, cooking_time, ingredients, difficulty=None):
        self.name = name
        self.cooking_time = cooking_time
        self.ingredients = ingredients
        self.difficulty = difficulty

    def __repr__ (self):
        return ("Recipe ID:" + str(self.id) + '-' + self.name + '-' + self.difficulty )
    
    #return a well formatted recipe
    def __str__ (self):
        ingredients_list = "\n".join(f"   • {ingredient}" for ingredient in self.return_ingredients_as_list())
        return (
            "\n" + "=" * 50 + "\n"
            f" 🍽️  Recipe: {self.name} (ID: {self.id})\n"
            + "-" * 50 + "\n"
            f" 📝 Ingredients:\n{ingredients_list}\n"
            + "-" * 50 + "\n"
            f" ⏱️  Cooking Time : {self.cooking_time} minutes\n"
            f" 🔥 Difficulty   : {self.difficulty}\n"
            + "=" * 50 + "\n"
        ) 
    
    def calc_difficulty(self):
            num_ingredients = len(self.return_ingredients_as_list())
            if self.cooking_time < 10 and num_ingredients < 4:
                self.difficulty = "Easy"
            elif self.cooking_time < 10 and num_ingredients >= 4:
                self.difficulty = "Medium"
            elif self.cooking_time >= 10 and num_ingredients < 4:
                self.difficulty = "Intermediate"
            elif self.cooking_time >= 10 and num_ingredients >= 4:
                self.difficulty = "Hard"
            return self.difficulty
    
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return [ingredient.strip() for ingredient in self.ingredients.split(",") if ingredient.strip()]


Base.metadata.create_all(engine)

def get_name():
    while True:
        try:
            name = str(input("\nEnter the name of the recipe: "))
            if not name:
                raise ValueError ("Name cannot be empty")
            elif len(name)>50:
                raise ValueError ("Name cannot exceed 50 characters!")
            return name
        except ValueError as e:
            print(f"\n{e}")

def get_cooking_time():
     while True:
            try:
                cooking_time = int(input("\nEnter cooking time (minutes): "))
                if not cooking_time:
                    raise ValueError ("Please insert a value!")
                elif cooking_time <= 0:
                    raise ValueError ("Nothing gets cooked that fast!")
                return cooking_time
            except ValueError as e:
                print(f"\n{e}")

def get_ingredients():
    while True:
        try:
            ingredients = []
            number_ingredients = int(input("\nHow many ingredients you'd like to enter: "))
            if not number_ingredients:
                raise ValueError ("Must enter a number")
            if number_ingredients > 10:
                raise ValueError ("Maximum 10 ingredients are allowed")
            for i in range(number_ingredients):
                ingredient = str(input(f"\nEnter the {i+1} ingredient: "))
                ingredients.append(ingredient)
            return ingredients
        except ValueError as e:
            print(f"\n{e}")

def create_recipe():
    name = get_name()

    cooking_time = get_cooking_time()

    ingredients = get_ingredients()
    ingredients_str = ", ".join(ingredients)

    recipe_entry = Recipe(name, cooking_time, ingredients_str, difficulty = None)

    recipe_entry.calc_difficulty()

    session.add(recipe_entry)
    session.commit()

def view_all_recipes():
    recipes_list = session.query(Recipe).all()
    if len(recipes_list) == 0:
        print("\nNo Recipes found")
        return None
    for recipe in recipes_list:
        print(recipe.__str__())

def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("\nNo Recipes found!")

    results = session.query(Recipe.ingredients).all()
    print(results)

    all_ingredients_set = set()

    for i in results:
        all_ingredients_set.update(ing.strip() for ing in i[0].split(","))
    print(all_ingredients_set)

    all_ingredients = list(all_ingredients_set)

    print("\n---- LIST OF INGREDIENTS ----")
    print("")
    for position, name in enumerate(all_ingredients, start=1):
        print(f"{position}, {name}")

    while True:
        try:
            search_numb = (input("\nEnter the numbers of ingredients you want to search (separate them with space): "))
            if search_numb < 1 or search_numb > len(all_ingredients):
                raise ValueError 
        except ValueError:
                print("\nEnter a valid number!")
    
    

search_by_ingredients()