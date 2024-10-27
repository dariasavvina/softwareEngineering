from fastapi import FastAPI
from pydantic import BaseModel
from model import RecipesGeneratingParameters
from recipe_generator import generation_recipes

app = FastAPI()


class RecipesGeneratingParametersBody(BaseModel):
    count_recipes: int
    theme: str
    products: list[str]


@app.post("/recipes")
def generate_recipes(body: RecipesGeneratingParametersBody):
    parameters = RecipesGeneratingParameters(body.count_recipes, body.theme, body.products)
    recipes = generation_recipes(parameters)
    return recipes
