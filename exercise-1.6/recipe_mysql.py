import mysql.connector

# connect to database
conn = mysql.connector.connect(
    host="localhost",
    user="cf-python",
    password="password",
    database="task_database"
)

cursor = conn.cursor()

# function to insert a recipe and save it in the DB
def create_recipe(conn, cursor):
    name = str(input("\nEnter the name of the recipe: "))

    while True:
        try:
            cooking_time = int(input("Enter the cooking time (min): "))
            if cooking_time <= 0 :
                raise ValueError
            break
        except ValueError:
            print("Please enter a correct cooking time (min): ")
    
    while True:
        try:        
            ingredients_list = [ingredient.strip() for ingredient in input("Enter the ingredients needed (separated by comma): ").split(',')]
            if len(ingredients_list) == 0 or any(i == "" for i in ingredients_list) or any(not i.replace(" ", "").isalpha() for i in ingredients_list):
                    raise ValueError
            break
        except ValueError:
            print("\nMust be a sequence of ingredients separeted by a comma")
            

    difficulty = calc_difficulty(cooking_time, ingredients_list)
    ingredients = ", ".join(ingredients_list)

    query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    data = (name, ingredients, cooking_time, difficulty)
    
    cursor.execute(query, data)
    conn.commit()

    return
   
# function to search for a recipe by an ingredient
def search_recipe(conn, cursor):
    query = "SELECT ingredients FROM Recipes"
    cursor.execute(query)
    results = cursor.fetchall()
    print("Results: ", results)
    all_ingredients = set() # creates a set object with ingredients
    for row in results:
         ingredients_str = row[0] # select the tuple in each row
         ingredients = [i.strip() for i in ingredients_str.split(",")] # creates a list of ingredient for each tuple
         all_ingredients.update(ingredients)
         all_ingredients_list = list(all_ingredients) # convert the set object into a list which is subscriptable

    print ("All ingredients", all_ingredients)
    
    print("\n---- LIST OF INGREDIENTS ----")
    print("")
    for position, name in enumerate(all_ingredients_list, start=1):
         print(f"{position}, {name}")

    numb = int(input("\nEnter the number of ingredient you want to search: "))
    search_ingredient = str(all_ingredients_list[numb-1])
    query_search = f"SELECT name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE '%{search_ingredient}%'"
    cursor.execute(query_search)
    recipe = cursor.fetchall()
    print(f"\nList of recipes with {search_ingredient}")
    for row in recipe:
         print("\nName:", row[0])
         print("Ingredients:", row[1])
         print("Cooking Time:", row[2])
         print("Difficulty:", row[3])

    return

# function to update a certain recipe 
def update_recipe(conn, cursor):
    query = "SELECT id, name FROM Recipes"
    cursor.execute(query)
    list_recipes = cursor.fetchall()
    print("\nID    Name") # print names of recipes with their ID
    list_id =[]
    for i in list_recipes:
         list_id.append(i[0])
         print(f"\n {i[0]}    {i[1]}")

    while True:
        try:  
            id = int(input("\nEnter the ID number of the recipe you'd like to update: ")) # check that the input is valid
            if not id in list_id:
                 raise ValueError
            break
        except ValueError:
             print("\nPlease make sure you select an exisiting ID")
        
    while True:
        params = ["Name", "Cooking time", "Ingredients"]
        try:
            param_change = str(input("\nWhat parameter you would like to change between 'Name', 'Cooking time', 'Ingredients': "))
            if not param_change in params:
                 raise ValueError
            break
        except ValueError:
            print("Make sure you insert the right parameter")
    
    query = f"SELECT {param_change} FROM Recipes WHERE id={id}"

    return
    
def delete_recipe(conn, cursor):
        return


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




def main_menu(conn, cursor):   
    choice = ''
    while (choice != 'quit'):
        print('\nMain Menu')
        print("\n", 20*"-")
        print("\nPick a choice:")
        print("\n.   1. Create a new recipe")
        print("\n.   2. Search for a recipe by ingredient")
        print("\n.   3. Update an existing recipe")
        print("\n.   4. Delete a recipe")
        print("\nType 'quit' to exit the program.")
        choice = input("\nType your choice: ")

        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "quit":
            conn.commit()
            conn.close()
            print("Recipe saved")

main_menu(conn, cursor)