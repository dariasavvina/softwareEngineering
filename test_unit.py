import pytest
from model import RecipesGeneratingParameters
from recipe_generator import generation_prompt, request_in_llm

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