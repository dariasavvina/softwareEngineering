import pytest
from model import RecipesGeneratingParameters
from recipe_generator import generation_prompt, request_in_llm
from yolo_prediction import yolo_predict
from PIL import Image

# Модульные тесты

true_prompt = ('Я передам тебе слова на английском языке, тебе необходимо отобрать из них продукты и написать '
               'мне следующее количество рецептов на русском языке: 2. По теме: завтрак. '
               'Набор продуктов: морковь, яблоко, сметана.')


def test_generate_correct_promt():
    parameters = RecipesGeneratingParameters(2, 'завтрак', ['морковь', 'яблоко', 'сметана'])
    promt = generation_prompt(parameters)
    assert promt == true_prompt


def test_generate_answer_by_promt():
    answer = request_in_llm(true_prompt)
    assert len(answer) > 0


@pytest.mark.parametrize("image_path,expected_result",
                         [("./assets/apple_banana.jpg", {"apple", "banana"}),
                          ("./assets/carrot_broccoli.jpg", {"carrot", "broccoli"}),
                          ("./assets/pizza.jpg", {"pizza"})])
def test_process_image(image_path, expected_result):
    image_data = Image.open(image_path)
    actual_result = yolo_predict(image_data).response
    assert actual_result == expected_result