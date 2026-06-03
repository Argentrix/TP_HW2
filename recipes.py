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
        val = float(value)
        
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