import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

url = '/recipes'


def test_generate_recipes():
    response = client.post(url,
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
    response = client.post(url,
                           json={"count_recipes": count_recipes, "theme": theme, "products": products}
                           )
    assert response.status_code != 200
