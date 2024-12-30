import pytest
from fastapi.testclient import TestClient
from api import app
from PIL import Image

client = TestClient(app)

recipes_url = '/recipes'

image_objects_url = '/image_objects'


def test_generate_recipes():
    response = client.post(recipes_url,
                           json={"count_recipes": 1, "theme": "завтрак", "products": ['морковь', 'яблоко', 'сметана']})
    assert response.status_code == 200
    result = response.json()
    recipes = result['recipes']
    assert 'рецепт' in recipes


@pytest.mark.parametrize("count_recipes,theme,products",
                         [(None, None, None),
                          (1, None, None),
                          (None, "завтрак", None),
                          (None, None, ['Морковь'])])
def test_error_when_any_parameters_none(count_recipes, theme, products):
    response = client.post(recipes_url,
                           json={"count_recipes": count_recipes, "theme": theme, "products": products}
                           )
    assert response.status_code != 200


# @pytest.mark.parametrize("image_path,expected_result",
#                          [("./assets/apple_banana.jpg", ["apple", "banana"]),
#                           ("./assets/carrot_broccoli.jpg", ["carrot", "broccoli"]),
#                           ("./assets/pizza.jpg", ["pizza"])])
# def test_process_image(image_path, expected_result):
#     image_data = Image.open(image_path)
#     print(image_data.len())
