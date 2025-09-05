import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, or_
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.types import Integer, String

#load parameters from .env 
load_dotenv()
host=os.getenv("DB_HOST")
user=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
database=os.getenv("DB_DATABASE")

#establish connection with the database
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

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

    #validate user input
    while True:
        try:
            name = str(input("\nEnter the name of the recipe: "))
            if not name:
                raise ValueError ("Name cannot be empty")
            elif len(name)>50:
                raise ValueError ("Name cannot exceed 50 characters!")
            
            #return the value
            return name
        except ValueError as e:
            print(f"\n{e}")

def get_cooking_time():
     
     #validate input
     while True:
            try:
                raw_input = input("\nEnter cooking time (minutes): ")
                try:
                    cooking_time = int(raw_input)
                except ValueError:
                    print("\nPlease enter a number, no text or symbols, or empty value!")
                    continue
                if not cooking_time:
                    raise ValueError ("Nothing gets cooked that fast!")
                
                #return the value
                return cooking_time
            except ValueError as e:
                print(f"\n{e}")

def get_ingredients():

    #validate user input
    while True:
        try:
            raw_input = input("\nHow many ingredients you'd like to enter: ")
            try:
                number_ingredients = int(raw_input)
            except ValueError:
                print("\nPlease enter a number, no text or symbols, or empty value!")
                continue
            if not number_ingredients:
                raise ValueError ("Must enter a number")
            if number_ingredients > 10:
                raise ValueError ("Maximum 10 ingredients are allowed")
            
            #creates empty list of ingredient
            ingredients = []

            #add ingredients to the list
            for i in range(number_ingredients):
                ingredient = str(input(f"\nEnter ingredient n-{i+1}: "))
                ingredients.append(ingredient)

            #return the value
            return ingredients
        except ValueError as e:
            print(f"\n{e}")

def create_recipe():
    name = get_name()

    cooking_time = get_cooking_time()

    ingredients = get_ingredients()
    #convert list into a tuple containing a string of ingredients
    ingredients_str = ", ".join(ingredients)

    #creates an entry following the object method
    recipe_entry = Recipe(name, cooking_time, ingredients_str, difficulty = None)

    #calculate difficulty
    recipe_entry.calc_difficulty()

    session.add(recipe_entry)
    session.commit()

def view_all_recipes():

    #check if there are recipes in the DB
    recipes_list = session.query(Recipe).all()
    if len(recipes_list) == 0:
        print("\n\t---- No Recipes Found ----")
        return None
    
    #print all recipes
    for recipe in recipes_list:
        print(recipe.__str__())

def search_by_ingredients():

    #check if there are recipes in the DB
    if session.query(Recipe).count() == 0:
        print("\n\t---- No Recipes Found ----")
        return None

    #obtain object with all recipes
    results = session.query(Recipe.ingredients).all()

    all_ingredients_set = set()

    for i in results:
        all_ingredients_set.update(ing.strip() for ing in i[0].split(","))

    #sort the ingredients of each recipe
    all_ingredients = sorted(list(all_ingredients_set))

    print("\n---- LIST OF INGREDIENTS ----")
    print("")
    for position, name in enumerate(all_ingredients, start=1):
        print(f"{position}, {name}")

    #validate user input
    while True:
        try:
            raw_input = input("\nEnter the numbers of ingredients you want to search (separate them with space): ").split()
            try:
                search_numb = list(map(int,raw_input))
            except ValueError:
                print("\nPlease enter a number, no text or symbols, or empty value!")
                continue
            if len(search_numb) == 0:
                raise ValueError ("Please enter at least one number!")
            for i in search_numb:
                if i <= 0 or i > len(all_ingredients):
                    raise ValueError("Please pick a number from the list")
            break
        except ValueError as e:
            print(f"\n{e}")

    #creates a list with the ingredients to be search         
    search_ingredients =[]
    for i in search_numb:
        search_ingredients.append(all_ingredients[i-1])

    #creates a list for the condition use to query DB
    condition = []
    for i in search_ingredients:
        condition.append(Recipe.ingredients.like(f'%{i}%'))
    #query DB
    results = session.query(Recipe).filter(or_(*condition)).all()
    #print results
    print(f"\n---- Recipes ----")
    for result in results:
        print(result.__str__())

def edit_recipe():

    #get all recipes from DB
    result = session.query(Recipe).all()

    #check if there are recipes in the DB
    if not result:
        print("\n\t---- No Recipes Found ----")
        return None
    
    #creates a list with id and name of existing recipes
    results = []
    for i in result:
        results.append(i.id)
        results.append(i.name)
        print(i.__str__())

    #validate user input
    while True:
        try:
            raw_input = input("\nEnter the id number of the recipe you'd like to edit: ")
            try:
                choose_id = int(raw_input)
            except ValueError:
                print("\nPlease enter a number, no text or symbols!")
                continue
            if not choose_id:
                raise ValueError ("\nPlease insert a correct ID")
            elif not choose_id in results:
                print("\nItem not in the list!")
                return None
            break
        except ValueError as e:
            print(f"\n{e}")
    
    #retrieve corresponding recipe to edit
    recipe_to_edit = session.query(Recipe.name, Recipe.ingredients, Recipe.cooking_time).filter(Recipe.id == choose_id).one()
    for position, (col, val) in enumerate(recipe_to_edit._mapping.items(), start=1):
        print(f"\n{position}. Recipe {col.capitalize()}: {val}")

    #validate user input
    while True:
        try:
            raw_input = input("\nEnter the number of the attribute you'd like to edit: ")
            try:
                choose_attribute = int(raw_input)
            except ValueError:
                print("\nPlease enter a number, no text or symbols!")
                continue
            if not choose_attribute:
                raise ValueError ("\nPlease insert a correct attribute!")
            elif choose_attribute > 3 or choose_attribute < 1:
                raise ValueError ("\nPlease pick an attribute from the list!")
            break
        except ValueError as e:
            print(f"\n{e}")

    #retrieve all recipe to edit
    recipe = session.query(Recipe).filter(Recipe.id == choose_id).one()

    #updates recipes and save it
    if choose_attribute == 1:
        new_name = get_name()
        recipe.name = new_name
        
    elif choose_attribute == 2:
        new_ingredients = get_ingredients()
        new_ingredients_str = ", ".join(new_ingredients)
        recipe.ingredients = new_ingredients_str

    elif choose_attribute == 3:
        new_cooking_time = get_cooking_time()
        recipe.cooking_time = new_cooking_time

    if choose_attribute in (2,3):
        recipe.calc_difficulty()

    session.commit()
    
    #print new recipe
    print("\n\t---- New Updated Recipe ----")
    print(recipe.__str__())

def delete_recipe():

    #get all recipes from DB
    result = session.query(Recipe).all()

    #check if there are recipes in the DB
    if not result:
        print("\n\t---- No Recipes Found ----")
        return None

    #creates a list with id and name of existing recipes
    results = []
    for i in result:
        results.append(i.id)
        results.append(i.name)
        print(i.__str__())

    #validate user input
    while True:
        try:
            raw_input = input("\nEnter the id number of the recipe you'd like to delete: ")
            try:
                choose_id = int(raw_input)
            except ValueError:
                print("\nPlease enter a number, no text or symbols!")
                continue
            if not choose_id:
                raise ValueError ("\nPlease insert a correct ID")
            elif not choose_id in results:
                print("\nItem not in the list!")
                return None
            break
        except ValueError as e:
            print(f"\n{e}")
    
    #query to delete the specified recipe
    recipe_to_delete = session.query(Recipe).filter(Recipe.id == choose_id).one()

    #extra validation 
    user_input = input("\nAre you sure you want to delete this recipe? (YES or NO): ").lower()
    if user_input == "yes":
        #delete recipe
        session.delete(recipe_to_delete)
        session.commit()
        print("\n\t---- Recipe deleted ----")
    else:
        return None
        

def main_menu():   
    choice = ''
    while (choice != 'quit'):
        print('\nMain Menu')
        print("\n", 20*"-")
        print("\nPick a choice:")
        print("\n.   1. Create a new recipe")
        print("\n.   2. View all recipes")
        print("\n.   3. Search for a recipe by ingredient")
        print("\n.   4. Edit a recipe")
        print("\n.   5. Delete a recipe")
        print("\nType 'quit' to exit the program.")
        choice = input("\nType your choice: ").strip().lower()

        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice != "quit":
            print("\nPlease pick one of those options!")
        elif choice == "quit":
            session.close()
        

main_menu()