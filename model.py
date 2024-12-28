from dataclasses import dataclass
from typing import Dict

@dataclass
class Recipes:
    recipes: [str]

@dataclass
class RecipesGeneratingParameters:
    count_recipes: int
    theme: str
    products: [str]

@dataclass
class ImageObjectsResponse:
    response: Dict[str, int]

