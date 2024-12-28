import requests
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from model import RecipesGeneratingParameters, ImageObjectsResponse
from recipe_generator import generation_recipes


app = FastAPI()

YOLOv10_URl = "https://8001/yolov10"

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

    response = requests.post(YOLOv10_URl, files={"file": ("image.jpg", image_data, "image/jpeg")})
    ImageObjectsResponse

    if response.status_code == 200:
        return ImageObjectsResponse(response = response.text)
    else:
        return {"error": "Failed to process image"}