import pickle

def display_recipe(recip):
    for recipe in recip :
        print("\nRecipe:", recipe["name"].capitalize())
        print("Cooking Time (min):", recipe["cooking_time"])
        print("Ingredients:")
        for ingredient in recipe["ingredients"]:
            print('- ', ingredient.capitalize())
        print("Difficulty Level: ", recipe["difficulty"])
        print("")

def search_ingredient(data):
    available_ingredients = data["ingredients"]
    for position, name in enumerate(available_ingredients, start=1):
        print(position, name)
        
    
    try:
        numb = int(input("\nPick a number from the list: "))
        ingredient_searched = available_ingredients[numb-1]
    except:
        print("\nThe number inserted is incorrect, try again")
        try: 
            numb = int(input("\nPick a number from the list: "))
            ingredient_searched = available_ingredients[numb-1]
        except:
            print("\nThe number is incorrect")
    else:
        for i in data["recipe_list"]:
            if ingredient_searched in i["ingredients"]:
                display_recipe(i)


filename = input("Enter the file you want to upload: ")
try:
    file = open(filename, 'rb')
    data = pickle.load(file)
    print("\nFile uploaded successfully.")
except:
    print("\nFile not found")
else:
    search_ingredient(data)