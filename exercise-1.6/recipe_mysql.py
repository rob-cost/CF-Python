import mysql.connector
from dotenv import load_dotenv
import os 

load_dotenv()

# connect to database
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Recipes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        ingredients VARCHAR(255),
        cooking_time INT,
        difficulty VARCHAR(20)
    )
""")

conn.commit()
print("\nDatabase and Table are ready to use!")

def get_name():
    while True:
        try:
            name = str(input("\nEnter the name of the recipe: "))
            if not name:
                raise ValueError
            return name
        except ValueError:
            print("\nName cannot be empty!") 

def get_cooking_time():
     while True:
            try:
                cooking_time = int(input("\nEnter cooking time (in min): "))
                if not cooking_time or cooking_time <= 0:
                    raise ValueError
                return cooking_time
            except ValueError:
                print("\nEnter a correct cooking time: ")
            

def get_ingredients():
    while True:
        try:
            ingredients_input = input("\nEnter the ingredients needed (separated by comma): ")
            if not ingredients_input:
                raise ValueError
            ingredients_list = [ingredient.strip() for ingredient in ingredients_input.split(",")]
            if any (not ingredient for ingredient in ingredients_list):
                raise ValueError
            
            return ingredients_list
        except ValueError:
            print(("\nMust be a sequence of ingredients separated by commas, no empty ingredients."))


# function to insert a recipe and save it in the DB
def create_recipe():

    name = get_name()

    cooking_time = get_cooking_time()
    
    ingredients_list = get_ingredients()
            
    difficulty = calc_difficulty(cooking_time, ingredients_list)
    ingredients_formatted = ", ".join(ingredients_list)

    query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    data = (name, ingredients_formatted, cooking_time, difficulty)
    cursor.execute(query, data)
    print("\n---- NEW RECIPE CREATED ----")

    return
   
# function to search for a recipe by an ingredient
def search_recipe():
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    all_ingredients = set() # creates a set object with ingredients
    for row in results:
         ingredients_str = row[0] # select the tuple in each row
         ingredients_list = [i.strip() for i in ingredients_str.split(",")] # creates a list of ingredient for each tuple
         all_ingredients.update(ingredients_list)
    
    all_ingredients_list = list(all_ingredients) # convert the set object into a list which is subscriptable
    
    print("\n---- LIST OF INGREDIENTS ----")
    print("")
    for position, name in enumerate(all_ingredients_list, start=1):
         print(f"{position}, {name}")

    while True:
        try:
            search_numb = int(input("\nEnter the number of ingredient you want to search: "))
            if search_numb < 1 or search_numb > len(all_ingredients_list):
                raise ValueError
            break
        except ValueError:
            print("\nEnter a valid number!")

    search_ingredient = str(all_ingredients_list[search_numb-1])
    query_search = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    cursor.execute(query_search, (f"%{search_ingredient}%",))
    result = cursor.fetchall()
    print(f"\nList of recipes with {search_ingredient}")
    print_recipe(result)

    return

# function to update a certain recipe 
def update_recipe():
    cursor.execute("SELECT id, name FROM Recipes")
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
        column_to_update = {"name": "name", "cooking time": "cooking_time", "ingredients": "ingredients"}
        try:
            user_input = input(f"\nWhat parameter would you like to change between {', '.join(column_to_update.keys())}: ").lower().strip()
            if user_input not in column_to_update:
                 raise ValueError
            break
        except ValueError:
            print("\nMake sure you choose an element from the list!")
    
    if user_input == "name":
        new_name = get_name()
        query_update = (f"UPDATE Recipes SET name = %s WHERE id = %s")
        cursor.execute(query_update, (new_name, id))
       
    elif user_input == "cooking time":
        new_cooking_time = get_cooking_time()
        query_update = ("UPDATE Recipes SET cooking_time = %s WHERE id = %s")
        cursor.execute(query_update, (new_cooking_time, id))

    elif user_input == "ingredients":
        new_ingredients = get_ingredients()
        new_ingredients_str =  ", ".join(new_ingredients)
        query_update = ("UPDATE Recipes SET ingredients = %s WHERE id = %s")
        cursor.execute(query_update, (new_ingredients_str, id))

    if user_input in ("name", "ingredients"):
        cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (id,))
        result = cursor.fetchone()
        ingredients_list = [i.strip() for i in result[1].split(",")]
        difficulty = calc_difficulty(result[0], ingredients_list)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (difficulty, id))


    conn.commit()
    cursor.execute("SELECT * FROM Recipes WHERE id = %s", (id,))
    result = cursor.fetchall()
    print("\n", 20*"-")
    print("\nNEW UPDATED ITEM:")
    print_recipe(result)
 
    return

# function to delete a row from DB
def delete_recipe():
    query_select = "SELECT id, name FROM Recipes"
    query_delete = "DELETE FROM Recipes WHERE id = %s"
    cursor.execute(query_select)
    list_recipes = cursor.fetchall()
    print("\nID    Name") # print names of recipes with their ID
    list_id =[]
    for i in list_recipes:
         list_id.append(i[0])
         print(f"\n {i[0]}    {i[1]}")

    while True:
        try:  
            id = int(input("\nEnter the ID number of the recipe you'd like to delete: ")) # check that the input is valid
            if not id in list_id:
                 raise ValueError
            break
        except ValueError:
             print("\nPlease make sure you select an exisiting ID")

    while True:       
        try:
            response = str(input("\nAre you sure you want to delete this recipe? (YES or NO) ").lower())
            if response == "yes":
                cursor.execute(query_delete, (id,))
                print("\nRecipe deleted successfully!")
            elif response == "no":
                print("\nOk, see you soon!")
            else:
                raise ValueError
            break
        except ValueError:
            print("\nEnter yes or no")

    conn.commit()      
    return

#function that calculated difficulty of the recipe
def calc_difficulty(cooking_time, ingredients):
        num_ingredients = len(ingredients)
        if cooking_time < 10 and num_ingredients < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and num_ingredients >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and num_ingredients < 4:
            difficulty = "Intermediate"
        elif cooking_time >= 10 and num_ingredients >= 4:
            difficulty = "Hard"
        return difficulty

#function that prints recipes fromn DB
def print_recipe(result):
    for row in result:
         print("\nID:", row[0])
         print("Name:", row[1])
         print("Ingredients:", row[2])
         print("Cooking Time:", row[3])
         print("Difficulty:", row[4])


def main_menu():   
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
            create_recipe()
        elif choice == "2":
            search_recipe()
        elif choice == "3":
            update_recipe()
        elif choice == "4":
            delete_recipe()
        elif choice == "quit":
            conn.commit()
            conn.close()
            print("Recipe saved")

main_menu()