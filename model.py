from dataclasses import dataclass

@dataclass
class Recipes:
    recipes: [str]

@dataclass
class RecipesGeneratingParameters:
    count_recipes: int
    theme: str
    products: [str]

