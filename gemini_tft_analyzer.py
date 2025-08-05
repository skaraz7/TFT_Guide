"""
Genera un listado de composiciones TFT Set 15 con Gemini Pro.
Devuelve 20 comps ordenadas por potencia estimada y las guarda en HTML.

Requisitos:
  pip install google-generativeai
  export GOOGLE_API_KEY="tu_api_key_aqui"
"""

import json
import os
import google.generativeai as genai
from datetime import datetime

# Cambio a Gemini Pro como solicitaste
MODEL = "gemini-1.5-pro-latest"

def load_database():
    """Carga la base de datos TFT"""
    try:
        with open("TFTSet15_latest_en_us.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: No se encontró TFTSet15_latest_en_us.json")
        return None
    except json.JSONDecodeError:
        print("❌ Error: Archivo JSON inválido")
        return None

def generate_compositions(db):
    """Genera composiciones usando Gemini Pro"""
    # Configura el SDK
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY no configurada")
        return None
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL)
    
    # Prompt optimizado
    prompt = f"""
You are an expert Teamfight Tactics analyst for Set 15.

Generate exactly 20 team compositions ordered by win-rate potential (1=strongest, 20=weakest).

For each composition return:
- "name": composition name
- "tier_rank": number 1-20
- "champions": array of champion names
- "carry": main damage dealer
- "core_items": object with champion->items array
- "synergies": key trait synergies

Return ONLY valid JSON array format.

Database sample: {json.dumps(db, ensure_ascii=False)[:8000]}
"""
    
    try:
        print("🔄 Generando composiciones con Gemini Pro...")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Error en Gemini API: {e}")
        return None

def create_html_output(compositions_text):
    """Crea archivo HTML con los resultados"""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>TFT Set 15 - Composiciones Meta</title>
    <style>
        body {{ font-family: Arial; margin: 20px; background: #1a1a2e; color: #eee; }}
        .comp {{ background: #16213e; margin: 10px 0; padding: 15px; border-radius: 8px; }}
        .tier {{ color: #ffd700; font-weight: bold; }}
        .carry {{ color: #ff6b6b; }}
        pre {{ background: #0f0f23; padding: 10px; border-radius: 4px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>🏆 TFT Set 15 - Meta Compositions</h1>
    <p><strong>Generado:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Modelo:</strong> {MODEL}</p>
    
    <div class="comp">
        <h3>📊 Respuesta de Gemini Pro:</h3>
        <pre>{compositions_text}</pre>
    </div>
</body>
</html>"""
    
    with open("tft_compositions.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ Archivo HTML creado: tft_compositions.html")

def main():
    """Función principal"""
    print("🚀 Iniciando análisis TFT con Gemini Pro...")
    
    # Cargar base de datos
    db = load_database()
    if not db:
        return
    
    print(f"✅ Base de datos cargada: {len(db)} elementos")
    
    # Generar composiciones
    compositions = generate_compositions(db)
    if not compositions:
        return
    
    # Crear HTML
    create_html_output(compositions)
    print("🎉 Proceso completado!")

if __name__ == "__main__":
    main()