import pytest
from recipes import Ingredient, Recipe, ShoppingList

def test_ingredient_creation():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"

def test_ingredient_invalid_quantity():
    with pytest.raises(ValueError, match="Количество должно быть положительным"):
        Ingredient("Сахар", -10, "г")
    with pytest.raises(ValueError, match="Количество должно быть положительным"):
        Ingredient("Сахар", 0, "г")

def test_ingredient_str():
    ing = Ingredient("Мука", 500.0, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_ingredient_eq():
    ing1 = Ingredient("Томаты", 200, "г")
    ing2 = Ingredient("Томаты", 500, "г")
    ing3 = Ingredient("Лук", 200, "г")
    ing4 = Ingredient("Томаты", 200, "кг")
    
    assert ing1 == ing2
    assert ing1 != ing3
    assert ing1 != ing4


def test_recipe_creation():
    ing = Ingredient("Тесто", 1, "шт")
    recipe = Recipe("Пицца", [ing])
    assert recipe.title == "Пицца"
    assert len(recipe.ingredients) == 1

def test_recipe_add_ingredient():
    recipe = Recipe("Омлет")
    ing1 = Ingredient("Яйцо", 2, "шт")
    ing2 = Ingredient("Яйцо", 3, "шт")
    ing3 = Ingredient("Молоко", 100, "мл")
    
    recipe.add_ingredient(ing1)
    recipe.add_ingredient(ing2)
    recipe.add_ingredient(ing3)
    
    assert len(recipe) == 2
    assert recipe.ingredients[0].quantity == 5.0

def test_recipe_scale():
    ing = Ingredient("Сыр", 150, "г")
    recipe = Recipe("Паста", [ing])
    
    scaled = recipe.scale(2)
    assert scaled is not recipe
    assert scaled.ingredients[0].quantity == 300.0
    assert recipe.ingredients[0].quantity == 150.0 

    with pytest.raises(ValueError):
        recipe.scale(-1)

def test_shopping_list_add_and_get():
    recipe = Recipe("Кофе")
    recipe.add_ingredient(Ingredient("Молоко", 50, "мл"))
    
    shop_list = ShoppingList()
    shop_list.add_recipe(recipe, 2)
    
    final_list = shop_list.get_list()
    assert len(final_list) == 1
    assert final_list[0].name == "Молоко"
    assert final_list[0].quantity == 100.0

def test_shopping_list_invalid_portions():
    recipe = Recipe("Чай")
    shop_list = ShoppingList()
    with pytest.raises(ValueError):
        shop_list.add_recipe(recipe, 0)

def test_shopping_list_remove_recipe():
    r1 = Recipe("Суп", [Ingredient("Вода", 1, "л")])
    r2 = Recipe("Борщ", [Ingredient("Свекла", 2, "шт")])
    
    shop_list = ShoppingList()
    shop_list.add_recipe(r1, 1)
    shop_list.add_recipe(r2, 1)
    
    shop_list.remove_recipe("Суп")
    final_list = shop_list.get_list()
    assert len(final_list) == 1
    assert final_list[0].name == "Свекла"

def test_shopping_list_aggregation_and_sorting():
    r1 = Recipe("Салат", [Ingredient("Томаты", 200, "г"), Ingredient("Огурцы", 100, "г")])
    r2 = Recipe("Закуска", [Ingredient("Томаты", 100, "г")])
    
    shop_list = ShoppingList()
    shop_list.add_recipe(r1, 1)
    shop_list.add_recipe(r2, 2)
    
    final_list = shop_list.get_list()
    assert len(final_list) == 2
    assert final_list[0].name == "Огурцы"
    assert final_list[1].name == "Томаты"
    assert final_list[1].quantity == 400.0

def test_shopping_list_addition():
    sl1 = ShoppingList()
    sl1.add_recipe(Recipe("А", [Ingredient("Сахар", 10, "г")]), 1)
    
    sl2 = ShoppingList()
    sl2.add_recipe(Recipe("Б", [Ingredient("Сахар", 20, "г")]), 1)
    
    combined = sl1 + sl2
    assert combined is not sl1
    assert combined is not sl2
    
    res = combined.get_list()
    assert res[0].quantity == 30.0