import requests
from backend.app.core.config import settings

def run_ai_task(prompt: str):
    headers = {
        "Authorization": f"Bearer {settings.FEATHERLESS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": settings.AI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.7
    }
    try:
        response = requests.post(
            f"{settings.FEATHERLESS_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        data = response.json()
        if "choices" not in data:
            return f"AI Response: {data.get('error', 'No response from model')}"
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"AI Task completed: {prompt} (Error: {str(e)})"