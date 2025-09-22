import pickle

def display_recipe(recipe):
        print("\nRecipe:", recipe["name"].capitalize())
        print("Cooking Time (min):", recipe["cooking_time"])
        print("Ingredients:")
        for ingredient in recipe["ingredients"]:
            print('- ', ingredient.capitalize())
        print("Difficulty Level: ", recipe["difficulty"])
        print("")

def search_ingredient(data):
    available_ingredients = data["all_ingredients"]
    print("\n ---- FULL INGREDIENTS LIST ---- \n")
    for position, name in enumerate(available_ingredients, start=1):
        print(f"{position}. {name}")
        
    try:
        numb = int(input("\nEnter the number of ingredient you want to search: "))
        ingredient_searched = str(available_ingredients[numb-1])
    except:
        print("\nThe number inserted is incorrect, try again")
        try: 
            numb = int(input("\nEnter the number of ingredient you want to search: "))
            ingredient_searched = str(available_ingredients[numb-1])
        except:
            print("\nThe number is incorrect")
    else:
        print(f"\n ---- RECIPES FOUND CONTAINING '{ingredient_searched}' ----")
        for i in data["recipes_list"]:
            if ingredient_searched in i["ingredients"]:
                display_recipe(i)


filename = input("Enter the file you want to upload: ")
try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        print("\nFile uploaded successfully.")
        print(data)
except FileNotFoundError:
    print("\nFile not found")
else:
    search_ingredient(data)