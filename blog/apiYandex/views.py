import html
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import re

API_KEY = 'AQVNwYeUAGm8OLn53qnnjNx6c5cElvABxraMJTpK'
ENDPOINT = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'


@api_view(['POST'])
def generate_text(request):
    if request.method == 'POST':
        topic = request.data.get('topic')

        if not topic:
            return Response({'error': 'Topic is required'}, status=400)

        headers = {
            'Authorization': f'Api-Key  {API_KEY}',
            'Content-Type': 'application/json',
        }

        payload = {
            "modelUri": "gpt://b1goruoj4gq85o7bkvk5/yandexgpt-lite/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": 200
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Ты — опытный копирайтер. Напиши  текст для поста учитывая заголовоек пользователя, а также, чтобы текст был завершенным"
                },
                {
                    "role": "user",
                    "text": f"Привет, напиши пост тему: {topic}"
                }
            ]
        }

        response = requests.post(ENDPOINT, json=payload, headers=headers)

        if response.status_code == 200:
            # Парсим JSON ответ
            data = response.json()

            # Извлекаем текст из JSON
            text = data['result']['alternatives'][0]['message']['text']

            # Отправляем текст в ответе Django
            return JsonResponse({'text': text})
        else:
            # Если запрос завершился с ошибкой, возвращаем ошибку
            return JsonResponse({'error': 'Failed to generate text'}, status=response.status_code)

