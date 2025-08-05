"""
Genera un listado de composiciones TFT Set 15 con Gemini Pro.
Versión corregida con manejo de errores y salida HTML.
"""

import json
import os
import sys

# Configurar codificación para Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer)

try:
    import google.generativeai as genai
except ImportError:
    print("[ERROR] google-generativeai no instalado. Ejecuta: pip install google-generativeai")
    exit(1)

MODEL = "gemini-1.5-pro-latest"

print("[INFO] Iniciando análisis TFT con Gemini Pro...")
print(f"[INFO] Modelo seleccionado: {MODEL}")

# 1️⃣ Carga base de datos
try:
    with open("TFTSet15_latest_en_us.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    print(f"[OK] Base de datos cargada: {len(db)} elementos")
except FileNotFoundError:
    print("[ERROR] No se encontró TFTSet15_latest_en_us.json")
    print("[INFO] Usando datos de ejemplo para la prueba...")
    db = {
        "champions": [{"name": "Jinx", "cost": 4, "traits": ["Rebel", "Blaster"]}],
        "items": [{"name": "Infinity Edge", "description": "Critical strikes deal more damage"}],
        "traits": [{"name": "Rebel", "description": "Rebels gain attack damage"}]
    }

# 2️⃣ Configura SDK
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("[ERROR] GOOGLE_API_KEY no configurada")
    print("[INFO] Usando respuesta simulada...")
    simulate_response = True
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(MODEL)
        simulate_response = False
        print(f"[OK] Modelo configurado: {MODEL}")
    except Exception as e:
        print(f"[ERROR] Error configurando Gemini: {e}")
        simulate_response = True

# 3️⃣ Prompt
prompt = f"""
You are an expert Teamfight Tactics analyst.

From the following Set 15 database, generate **20 team compositions** ordered from highest to lowest expected win-rate.  
For each composition include:
  - "name"
  - "tier_rank" (1 = strongest, 20 = weakest)
  - "champions_early", "champions_mid", "champions_late" (arrays)
  - "carry" (main damage dealer)
  - "core_items" (dictionary champion→list[items])
  - "key_augments" (max 3 augments)
Output **valid JSON** only, inside a single top-level list.

Database: {json.dumps(db, ensure_ascii=False)[:8000]}
"""

# 4️⃣ Ejecuta consulta
print("[INFO] Generando composiciones...")

if simulate_response:
    print("[INFO] Simulando respuesta de Gemini Pro...")
    class MockResponse:
        text = '''[
  {
    "name": "Jinx Rebel Carry",
    "tier_rank": 1,
    "champions_early": ["Ziggs", "Malphite"],
    "champions_mid": ["Jinx", "Vi"],
    "champions_late": ["Jinx", "Vi", "Ekko", "Gangplank"],
    "carry": "Jinx",
    "core_items": {"Jinx": ["Infinity Edge", "Last Whisper", "Giant Slayer"]},
    "key_augments": ["Rebel Heart", "Combat Training", "Cybernetic Uplink"]
  },
  {
    "name": "Reroll Comp Example",
    "tier_rank": 2,
    "champions_early": ["Powder", "Steb"],
    "champions_mid": ["Powder", "Steb", "Vander"],
    "champions_late": ["Powder", "Steb", "Vander", "Caitlyn"],
    "carry": "Powder",
    "core_items": {"Powder": ["Deathblade", "Infinity Edge", "Bloodthirster"]},
    "key_augments": ["Family", "Sniper Focus", "Combat Training"]
  }
]'''
    response = MockResponse()
    print("[OK] Respuesta simulada generada")
else:
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 4096,
            }
        )
        print("[OK] Respuesta recibida de Gemini")
    except Exception as e:
        print(f"[ERROR] Error en API de Gemini: {e}")
        exit(1)

# 5️⃣ Procesa respuesta
try:
    comps = json.loads(response.text)
    print(f"[OK] Se generaron {len(comps)} composiciones")
except json.JSONDecodeError:
    print("[ERROR] Respuesta no es JSON válido:")
    print(response.text[:500])
    comps = None

# 6️⃣ Crea HTML
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>TFT Set 15 - Composiciones</title>
    <style>
        body {{ font-family: Arial; margin: 20px; background: #1a1a2e; color: #eee; }}
        .comp {{ background: #16213e; margin: 10px 0; padding: 15px; border-radius: 8px; }}
        .tier {{ color: #ffd700; font-weight: bold; }}
        pre {{ background: #0f0f23; padding: 10px; border-radius: 4px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>TFT Set 15 - Meta Compositions</h1>
    <p><strong>Modelo:</strong> {MODEL}</p>
    
    <div class="comp">
        <h3>Respuesta de Gemini Pro:</h3>
        <pre>{response.text if 'response' in locals() else 'Error: No se pudo obtener respuesta'}</pre>
    </div>
    
    {('<div class="comp"><h3>Composiciones procesadas:</h3>' + '<br>'.join([f'<span class="tier">#{comp.get("tier_rank", "?")}</span> {comp.get("name", "Sin nombre")} - Carry: {comp.get("carry", "N/A")}' for comp in (comps[:5] if comps else [])]) + '</div>') if comps else '<div class="comp"><h3>No se pudieron procesar las composiciones</h3></div>'}
</body>
</html>"""

with open("tft_results.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("\n[OK] Resultados guardados en: tft_results.html")
if comps:
    print("\nTop 3 composiciones:")
    for comp in comps[:3]:
        print(f"  #{comp.get('tier_rank', '?')} {comp.get('name', 'Sin nombre')} - Carry: {comp.get('carry', 'N/A')}")
else:
    print("\n[WARNING] No se pudieron procesar las composiciones. Revisa el archivo HTML.")