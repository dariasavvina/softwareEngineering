from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from model import RecipesGeneratingParameters
from recipe_generator import generation_recipes
from yolo_prediction import yolo_predict
import markdown


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


@app.post("/image_recipes", response_class=HTMLResponse)
async def generate_recipe_by_image(count_recipes: str, theme: str, file: UploadFile = File(...)):
    image_data = await file.read()
    products = list(yolo_predict(image_data).response)
    parameters = RecipesGeneratingParameters(count_recipes, theme, products)
    recipes = generation_recipes(parameters)
    return get_markdown_recipes(recipes.recipes)

def get_markdown_recipes(recipes):
    content = markdown.markdown(recipes)
    return HTMLResponse(content, media_type="text/html")