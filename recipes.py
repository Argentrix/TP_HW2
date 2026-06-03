class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self._quantity = None
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self) -> float:
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        try:
            val = float(value)
        except (ValueError, TypeError):
            raise ValueError("Количество должно быть числом")
        
        if val <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = val

    def __str__(self) -> str:
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self) -> str:
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit
    

class Recipe:
    def __init__(self, title: str, ingredients: list = None):
        self.title = title
        if ingredients is None:
            self.ingredients = []
        else:
            self.ingredients = list(ingredients)

    def add_ingredient(self, ingredient: Ingredient):
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio) -> bool:
        if type(ratio) == bool:
            return False
        val = float(ratio)
        return val > 0

    def scale(self, ratio: float):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Коэффициент масштабирования должен быть положительным числом")
        scaled_ingredients = []
        for ing in self.ingredients:
            scaled_ingredients.append(Ingredient(ing.name, ing.quantity * ratio, ing.unit))
        
        return Recipe(self.title, scaled_ingredients)

    def __len__(self) -> int:
        return len(self.ingredients)

    def __str__(self) -> str:
        result = f"Рецепт: {self.title}"
        for ing in self.ingredients:
            result += f"\n  - {ing}"
        return result
    
class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        
        scaled_recipe = recipe.scale(portions)
        for ing in scaled_recipe.ingredients:
            self._items.append((ing, recipe.title))

    def remove_recipe(self, title: str):
        new_items = []
        for item in self._items:
            if item[1] != title:
                new_items.append(item)
        self._items = new_items

    def get_list(self) -> list:
        reworked = {}
        for item in self._items:
            ing = item[0]
            key = (ing.name, ing.unit)
            if key in reworked:
                reworked[key] += ing.quantity
            else:
                reworked[key] = ing.quantity
        
        result_ingredients = []
        for (name, unit), qty in reworked.items():
            result_ingredients.append(Ingredient(name, qty, unit))
        
        result_ingredients.sort(key=lambda x: x.name)
        return result_ingredients
    def __add__(self, other: 'ShoppingList') -> 'ShoppingList':
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list
    
class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients: list = None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        scaled_ingredients = []
        for ing in self.ingredients:
            scaled_ingredients.append(Ingredient(ing.name, ing.quantity * ratio, ing.unit))
        
        return DietaryRecipe(self.title, self.diet_type, scaled_ingredients)

    def __str__(self) -> str:
        return f"[{self.diet_type}] {self.title}"