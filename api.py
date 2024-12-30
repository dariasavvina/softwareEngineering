import requests
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from model import RecipesGeneratingParameters
from recipe_generator import generation_recipes
from yolo_prediction import yolo_predict


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


@app.post("/image_objects")
async def process_image(file: UploadFile = File(...)):
    image_data = await file.read()
    return yolo_predict(image_data)