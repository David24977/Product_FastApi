from schemas.product_ai import ProductAIAnalysisResponse
from clients.ai_clients import AIClient


class AIService:
    def __init__(self, client: AIClient):
        self.client = client

    async def analyze_product(self, name: str, price: float, stock: int) -> ProductAIAnalysisResponse:
        system = (
            "Eres un asistente de API. Devuelve SOLO JSON válido, sin texto extra. "
            "Campos obligatorios: category (string), tags (array de strings), price_evaluation (string) "

        )

        user = (
            "Analiza este producto y devuelve el JSON:\n"
            f"name: {name}\n"
            f"price: {price}\n"
            f"stock: {stock}\n\n"
            "Reglas:\n"
            "- category debe ser uno de estos valores:\n"
            "beverage\n"
            "food\n"
            "electronics\n"
            "general\n"
            "- tags: 2 a 6 tags cortas\n"
            "- price_evaluation: very cheap | normal | expensive\n"

        )

        result = await self.client.chat_json(system=system, user=user)

        # Validación fuerte contra tu schema (si falla, explota aquí y lo detectas rápido)
        return ProductAIAnalysisResponse.model_validate(result)

