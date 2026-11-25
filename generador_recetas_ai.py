from google import genai
from google.genai import types
import os, json

def generar_receta(ingredientes: tuple, calorias:int, num_personas:int): # recibe los ingredientes como parametro
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    generation_config = {
        "max_output_tokens" : 2000,
        "temperature":0.7,
        "thinking_config" : types.ThinkingConfig(thinking_budget=0),
        "response_mime_type": "application/json",
        "system_instruction": """
                                Eres un asistente culinario especializado en dieta mediterránea.
                                Genera exactamente 3 propuestas de recetas mediterráneas en español usando los ingredientes disponibles y ajustadas a las calorías y número de personas indicados.

                                Reglas estrictas:
                                1. Responde ÚNICAMENTE con un JSON válido, sin bloques markdown (```), saludos ni texto extra.
                                2. En cada ingrediente, usa nombres genéricos y simples en singular (ej: "pechuga de pollo", "cebolla", "champiñón") para facilitar su búsqueda en bases de datos nutricionales, e indica su peso total en gramos para toda la receta.
                                3. La preparación debe ser telegráfica (máximo 25 palabras por receta).

                                Formato JSON exacto:
                                {
                                "recetas": [
                                    {
                                    "nombre": "Nombre de la receta",
                                    "ingredientes": [
                                        {"nombre": "ingrediente 1", "gramos": 200},
                                        {"nombre": "ingrediente 2", "gramos": 100}
                                    ],
                                    "preparacion": "Pasos breves de preparación."
                                    }
                                ]
                                }
                                """,
    }
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"Ingredientes: {ingredientes}\nPara {num_personas} personas\nCalorias por ración: {calorias}",
            config=generation_config,
        )
    except Exception as e:
        print("Se ha producido un error en la petición al modelo de IA")
        raise RuntimeError("Error al generar o procesar la receta con el modelo de IA")
        
    return json.loads(response.text)