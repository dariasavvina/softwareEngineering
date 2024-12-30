from model import RecipesGeneratingParameters
from model import Recipes
import requests
import os

token = "sk-0cPj93t2aM0U8PYIiLogcgfOae854MDC"
if token is None or token == '':
    raise ValueError('TOKEN environment variable is not set')

def generation_prompt(parameters: RecipesGeneratingParameters) -> str:
    products_str = ', '.join(parameters.products)
    return (f'Я передам тебе слова на английском языке, тебе необходимо отобрать из них продукты '
            f'и написать мне следующее количество рецептов на русском языке: {parameters.count_recipes}.'
            f' По теме: {parameters.theme}. Набор продуктов: {products_str}.')


def request_in_llm(prompt: str) -> str:
    response = requests.post('https://api.proxyapi.ru/openai/v1/chat/completions',
                      headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
                      json={
                          "model": "gpt-4o",
                          "messages": [{"role": "user",
                                        "content": prompt}]
                      })
    response_json = response.json()
    answer = response_json['choices'][0]['message']['content']
    return answer


def generation_recipes(recipes_generating_parameters: RecipesGeneratingParameters) -> Recipes:
    prompt = generation_prompt(recipes_generating_parameters)
    recipes = request_in_llm(prompt)
    return Recipes(recipes=recipes)

