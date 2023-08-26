import sqlite3


class RecipeManager:

    def __init__(self):
        self.conn = sqlite3.connect('recipes.db')
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                ingredients TEXT,
                steps TEXT
            );
        ''')
        self.conn.commit()

    def add_recipe(self):
        name = input("Enter recipe name: ")
        ingredients = input("Enter ingredients (comma-separated): ")
        steps = input("Enter steps: ")

        self.cursor.execute("INSERT INTO recipes (name, ingredients, steps) VALUES (?, ?, ?)", (name, ingredients, steps))
        self.conn.commit()
        print("Recipe added successfully!")

    def view_recipes(self):
        self.cursor.execute("SELECT id, name, ingredients, steps FROM recipes")
        recipes = self.cursor.fetchall()

        if not recipes:
            print("No recipes found.")
            return

        for recipe in recipes:
            print("\nID:", recipe[0])
            print("Name:", recipe[1])
            print("Ingredients:", recipe[2])
            print("Steps:", recipe[3])

    def search_recipe(self):
        name = input("Enter the recipe name to search: ")
        self.cursor.execute("SELECT id, name, ingredients, steps FROM recipes WHERE name LIKE ?", ('%' + name + '%',))
        recipes = self.cursor.fetchall()

        if not recipes:
            print(f"No recipes found for {name}.")
            return

        for recipe in recipes:
            print("\nID:", recipe[0])
            print("Name:", recipe[1])
            print("Ingredients:", recipe[2])
            print("Steps:", recipe[3])

    def delete_recipe(self):
        recipe_id = input("Enter the recipe ID to delete: ")

        self.cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        self.conn.commit()

        if self.cursor.rowcount:
            print("Recipe deleted successfully!")
        else:
            print("Recipe not found.")

    def close(self):
        self.conn.close()

    def start(self):
        print("Welcome to the Recipe Manager!")
        while True:
            print("\nChoose an option:")
            print("1. Add a new recipe")
            print("2. View all recipes")
            print("3. Search for a recipe by name")
            print("4. Delete a recipe")
            print("5. Exit")
            choice = input("> ")

            if choice == "1":
                self.add_recipe()
            elif choice == "2":
                self.view_recipes()
            elif choice == "3":
                self.search_recipe()
            elif choice == "4":
                self.delete_recipe()
            elif choice == "5":
                self.close()
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    manager = RecipeManager()
    manager.start()
