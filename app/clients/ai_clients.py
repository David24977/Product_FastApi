# clients/ai_client.py

from typing import Any, Dict, Optional
import json
import httpx

from core.config import settings


class AIClient:
    """
    Cliente genérico estilo 'OpenAI-compatible'.
    Sirve para Groq/DeepSeek/Ollama/OpenAI si exponen endpoint compatible.
    """

    def __init__(self, timeout: float = 20.0):

        self.api_key = settings.ai_api_key
        self.base_url = settings.ai_base_url.rstrip("/")
        self.model = settings.ai_model

        if not self.base_url:
            raise RuntimeError("Falta AI_BASE_URL en .env")

        if not self.model:
            raise RuntimeError("Falta AI_MODEL en .env")

        if not self.api_key:
            raise RuntimeError("Falta AI_API_KEY en .env")

        self.timeout = timeout

    async def chat_json(
            self,
            system: str,
            user: str,
            temperature: float = 0.2,
            extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Pide al modelo una respuesta JSON.
        OJO: no todos los proveedores soportan 'response_format'. Si no lo soporta,
        seguiremos pidiendo JSON por prompt.
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature
        }

        # Algunos proveedores soportan esto (OpenAI y compatibles modernos).
        # Si tu proveedor no lo soporta, lo ignorará o dará error.

        if extra:
            payload.update(extra)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}/chat/completions"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            r = await client.post(url, json=payload, headers=headers)
            print(r.text)
            r.raise_for_status()
            data = r.json()

        # Formato OpenAI-compatible:
        # data["choices"][0]["message"]["content"] debe ser JSON (string)
        content = data["choices"][0]["message"]["content"]

        # Convertimos a dict

        return json.loads(content)
