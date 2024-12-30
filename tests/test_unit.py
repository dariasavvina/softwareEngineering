import pytest
import os
import io
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


@pytest.mark.parametrize("image_name,expected_result",
                         [("apple_banana.jpg", {"apple", "banana"}),
                          ("carrot_broccoli.jpg", {"carrot", "broccoli"}),
                          ("pizza.jpg", {"pizza"})])
def test_process_image(image_name, expected_result):
    test_image_dir = os.path.join(os.path.dirname(__file__), "assets")
    image_path = os.path.join(test_image_dir, image_name)

    image_data = get_image_bytes(image_path)

    actual_result = yolo_predict(image_data).response
    assert expected_result.issubset(actual_result)


@pytest.mark.parametrize("image_name,expected_subsctrings",
                         [("apple_banana.jpg", {"яблоко", "банан"}),
                          ("carrot_broccoli.jpg", {"морковь", "брокколи"}),
                          ("pizza.jpg", {"пицца"})])
def test_generate_recipe_by_image(image_name, expected_subsctrings):
    test_image_dir = os.path.join(os.path.dirname(__file__), "assets")
    image_path = os.path.join(test_image_dir, image_name)

    image_data = get_image_bytes(image_path)

    products = list(yolo_predict(image_data).response)
    parameters = RecipesGeneratingParameters(2, 'завтрак', products)

    promt = generation_prompt(parameters)  
    actual_recipie = request_in_llm(promt)
    assert len(actual_recipie) > 0
    for subsctring in expected_subsctrings:
        assert subsctring in actual_recipie


def get_image_bytes(file_path):
    with Image.open(file_path) as img:
        byte_buffer = io.BytesIO()
        img.save(byte_buffer, format=img.format)
        byte_data = byte_buffer.getvalue()
    return byte_data