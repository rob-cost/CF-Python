class Recipe():
    all_ingredients = set()

    def __init__(self, name, ingredients, cooking_time):

        self.name = name
        self.ingredients = [str(i) for i in ingredients]
        self.cooking_time = cooking_time
        self.difficulty = self.calculate_difficulty()
        self.update_all_ingredients()

    def __str__(self):
        output = "----------" "\nRecipe: " + str(self.name) + "\nCooking time: " + str(self.cooking_time) + "\nDifficulty: " + str(self.difficulty) + "\nIngredients: " + str(self.ingredients)
        return output

    def add_ingredients(self, *ingredients):
            for ingredient in ingredients:
                self.ingredients.append(ingredient)
            self.update_all_ingredients()

    def get_ingredients(self):
        print("length", len(self.ingredients))
        output = "List of ingredients: " + str(self.ingredients)
        return output
    
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            return "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            return "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            return "Hard"

    def search_ingredient(self, search_term):
        return any(ingredient.lower() == search_term.lower() for ingredient in self.ingredients)
        
    def update_all_ingredients(self):
        self.all_ingredients.update(self.ingredients)

def recipe_search():
    search_term = str(input("\nEnter the ingredient you want to search: "))
    found = False
    for recipe in recipes_list:
        if recipe.search_ingredient(search_term):
            print(recipe)
            found = True
    if not found:
        print("No recipes found containing", search_term)
        
    
recipe_1 = Recipe("Tea", ["Tea Leaves", "Sugar", "Water"], 5)
recipe_2 = Recipe("Coffee", ["Coffee Powder", "Sugar", "Water"], 5)
recipe_3 = Recipe("Cake", ["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"], 5)
recipe_4 = Recipe("Banana Smoothie", ["Bananas", "Milk", "Peanut" "Butter", "Sugar", "Ice Cubes"], 5)

recipes_list = [recipe_1, recipe_2, recipe_3, recipe_4]

for recipe in recipes_list:
    print(recipe)

print("\nList of all ingredients:", "\n------------")
for i in Recipe.all_ingredients:
    print("-", i)

recipe_search()




