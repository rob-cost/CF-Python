# Recipe Collector

A simple Python terminal-based program that allows users to input and display recipes.

## Features

- Add one or more recipes by entering:
  - The recipe name
  - Cooking time
  - A list of ingredients
- Automatically validates ingredient input to avoid empty or invalid entries
- Automatically calculate a difficulty level
- Displays all collected recipes in a clean and readable format

## How It Works

1. The program asks the user how many recipes they want to enter.
2. For each recipe, it prompts for:
   - The name of the recipe
   - The cooking time of the recipe
   - A comma-separated list of ingredients
3. Once all recipes are entered, the program prints them out with proper formatting, together with a list of all the ingredients for all the recipes.

## Example

```bash
Enter the number of recipes you want to add: 2

--- Recipe 1 ---
Enter the name of the recipe: lasagna
Enter the cooking time (in min): 60
Enter the ingredients needed (separated by comma): pasta sheets, tomato sauce, cheese, minced meat

--- Recipe 2 ---
Enter the name of the recipe: salad
Enter the cooking time (in min): 10
Enter the ingredients needed (separated by comma): lettuce, tomato, olive oil, salt

--- All Recipes ---
1. Lasagna
   Ingredients:
   - Pasta Sheets
   - Tomato Sauce
   - Cheese
   - Minced Meat
   Difficulty Level: Hard

2. Salad
   Ingredients:
   - Lettuce
   - Tomato
   - Olive Oil
   - Salt
   Difficulty Level: Medium
```
