import requests
from app.core.config import settings


def get_services_by_symptoms(symptoms: list[str], services: list[dict]) -> str:
    prompt = f"Пользователь сообщил симптомы: {', '.join(symptoms)}.\nНайди подходящие услуги из списка ниже и выведи только их названия, без лишних пояснений:\n"
    for s in services:
        prompt += f"- {s['name']}: {s.get('description', '')}\n"

    headers = {
        "Authorization": f"Api-Key {settings.YA_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "modelUri": f"gpt://{settings.YA_FOLDER_ID}/yandexgpt-lite/latest",
        "completionOptions": {"stream": False, "temperature": 0.3, "maxTokens": 1000},
        "messages": [
            {"role": "system",
             "text": "Ты помогаешь подобрать медицинские услуги по симптомам. Ответь только списком подходящих услуг без пояснений или дополнительной информации."},
            {"role": "user", "text": prompt}
        ]
    }

    response = requests.post("https://llm.api.cloud.yandex.net/foundationModels/v1/completion", headers=headers,
                             json=data)

    # Обработка ответа, если что-то лишнее все-таки вернулось
    result = response.json()["result"]["alternatives"][0]["message"]["text"]
    services_only = '\n'.join(
        [line.strip() for line in result.split('\n') if line.strip() and not line.startswith("*")])

    return services_only
