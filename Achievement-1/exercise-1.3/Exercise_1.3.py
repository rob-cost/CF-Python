import sys

# Initiate two variable list
recipes_list = []
ingredients_list = []

# function that take details of a recipe
def take_recipe():
    name = str(input("Enter the name of the recipe: "))

    try:
        cooking_time = int(input("Enter the cooking time (min): "))
        if cooking_time <= 0 :
            raise ValueError("Must be longer than that")
    except ValueError:
        try:
            cooking_time = int(input("Please enter a correct cooking time (min): "))
            if cooking_time <= 0 :
                print("Invalid input. Exiting program.")
                sys.exit()
        except ValueError:
            print("Invalid input. Exiting program.")
            sys.exit()   

    try:        
        ingredients = [ingredient.strip() for ingredient in input("Enter the ingredients needed (separated by comma): ").split(',')]
        if len(ingredients) == 0 or any(i == "" for i in ingredients) or any(not i.replace(" ", "").isalpha() for i in ingredients):
                raise ValueError("Must be a sequence of word") 
    except ValueError:
        try:
            print("Must be a sequence of ingredients")
            ingredients = [ingredient.strip() for ingredient in input("Enter the ingredients needed (separated by comma): ").split(',')]
            if len(ingredients) == 0 or any(i == "" for i in ingredients) or any(not i.replace(" ", "").isalpha() for i in ingredients):
                print("Invalid input. Exiting program.")
                sys.exit()
        except ValueError:
            print("Invalid input. Exiting program.")
            sys.exit()

    
    recipe = {"name" : name, "cooking_time" : cooking_time, "ingredients" : ingredients}
    print("")
    return recipe

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


# add ingredients to a list of ingredients
for i in range(n) :
    recipe = take_recipe()
    for ing in recipe["ingredients"]:
        if ing not in ingredients_list:
            ingredients_list.append(ing)
    recipes_list.append(recipe)
    

# evaluate the difficulty of the recipe   
for i in recipes_list :
    if i["cooking_time"] < 10 and len(i["ingredients"]) < 4:
        i["difficulty"] = "Easy"
    elif i["cooking_time"] < 10 and len(i["ingredients"]) >= 4:
        i["difficulty"] = "Medium"
    elif i["cooking_time"] >= 10 and len(i["ingredients"]) < 4:
        i["difficulty"] = "Intermediate"
    elif i["cooking_time"] >= 10 and len(i["ingredients"]) >= 4:
        i["difficulty"] = "Hard"


# print the details of each recipe
for recipe in recipes_list :
    print("Recipe:", recipe["name"].capitalize())
    print("Cooking Time (min):", recipe["cooking_time"])
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print('- ', ingredient.capitalize())
    print("Difficulty Level: ", recipe["difficulty"])
    print("")


# print all the ingredients 
print("Ingredients Available Across All Recipes")
print("----------------------------------------")
ingredients_list.sort()
for ingredient in ingredients_list :
    print('- ', ingredient.capitalize())