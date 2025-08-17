import pickle
import sys

# Initiate two variable list
recipes_list = []
ingredients_list = []

# number of recipes to insert
try:
    n = int(input("How many recipes would you like to enter? "))
    if n < 0 :
        raise ValueError("Must be a positive number")
except ValueError :
    try:
        n = int(input("Please enter a positive number: "))
        if n < 0 :
            print("Invalid input. Exiting program.")
            sys.exit()
    except ValueError:
        print("Invalid input. Exiting program.")
        sys.exit()  

# function that take details of a recipe
def take_recipe(i):
    print(f"\nRecipe {i+1}: ")
    name = str(input("Enter the name of the recipe: "))

    try:
        cooking_time = int(input("Enter the cooking time (min): "))
        if cooking_time <= 0 :
            raise ValueError
    except ValueError:
        try:
            cooking_time = int(input("\nPlease enter a correct cooking time (min): "))
            if cooking_time <= 0 :
                print("\nInvalid input. Exiting program.")
                sys.exit()
        except ValueError:
            print("\nInvalid input. Exiting program.")
            sys.exit()   

    try:        
        ingredients = [ingredient.strip() for ingredient in input("Enter the ingredients needed (separated by comma): ").split(',')]
        if len(ingredients) == 0 or any(i == "" for i in ingredients) or any(not i.replace(" ", "").isalpha() for i in ingredients):
                raise ValueError
    except ValueError:
        try:
            print("\nMust be a sequence of ingredients")
            ingredients = [ingredient.strip() for ingredient in input("Enter the ingredients needed (separated by comma): ").split(',')]
            if len(ingredients) == 0 or any(i == "" for i in ingredients) or any(not i.replace(" ", "").isalpha() for i in ingredients):
                print("\nInvalid input. Exiting program.")
                sys.exit()
        except ValueError:
            print("\nInvalid input. Exiting program.")
            sys.exit()


    difficulty = calc_difficulty(cooking_time, ingredients)

    
    return {"name" : name, "cooking_time" : cooking_time, "ingredients" : ingredients, "difficulty" : difficulty}
    


#function that calculated difficulty of the recipe
def calc_difficulty(cooking_time, ingredients):
        if cooking_time < 10 and len(ingredients) < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and len(ingredients) >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and len(ingredients) < 4:
            difficulty = "Intermediate"
        elif cooking_time >= 10 and len(ingredients) >= 4:
            difficulty = "Hard"
        return difficulty

for i in range(n) :
    recipe = take_recipe(i)
    recipes_list.append(recipe)
    for ing in recipe["ingredients"]:
        if ing not in ingredients_list:
            ingredients_list.append(ing)

data = {"recipe_list" : recipes_list, "ingredients" : ingredients_list}


filename = input("\nPlease enter the file you want to use: ")
try:
    file = open(filename, 'rb')
    data = pickle.load(file)
    print('\n---\nData loaded successfully.')
except FileNotFoundError:
    data = {"recipe_list" : recipes_list, "ingredients" : ingredients_list}
    print("\n---\nFile not found. New data dictionary will be created and saved as {filename}.")
except:
    data = {"recipe_list" : [], "ingredients" : []}
    print("\n---\nAn error occured. New data dictionary created")
else:
    file.close()
    print("\n---\nFile closed.")
finally:
    recipe_list = []
    ingredients_list = []
    for i in data["recipe_list"]:
        recipe_list.append(i)
    for i in data["ingredients"]:
        ingredients_list.append(i)
    file = open(filename, 'wb')
    pickle.dump(data, file)
    file.close()
    print("\n---\nFile updated and saved successfully.")

    
 

    




