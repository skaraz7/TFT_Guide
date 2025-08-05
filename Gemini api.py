"""
Genera un listado de composiciones TFT Set 15 con Gemini.
Devuelve 20 comps ordenadas por potencia estimada.

Requisitos:
  pip install google-generativeai
  export GOOGLE_API_KEY="AIzaSyAoVOfxDNsEVPLGQpWRJ6BtoOoC8otieAM"
"""

import json
import os
import google.generativeai as genai

MODEL = "gemini-1.5-pro-latest"   # Cambiado a Gemini Pro como solicitaste

# 1️⃣  Carga tu base de datos local (campeones, items, traits…)
try:
    with open("TFTSet15_latest_en_us.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    print(f"✅ Base de datos cargada: {len(db)} elementos")
except FileNotFoundError:
    print("❌ Error: No se encontró TFTSet15_latest_en_us.json")
    exit(1)
except json.JSONDecodeError:
    print("❌ Error: Archivo JSON inválido")
    exit(1)

# 2️⃣  Configura el SDK
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(MODEL)
    print(f"✅ Modelo configurado: {MODEL}")
except Exception as e:
    print(f"❌ Error configurando Gemini: {e}")
    exit(1)

# 3️⃣  Crea un prompt cuidado: pedimos JSON ordenado
prompt = f"""
You are an expert Teamfight Tactics analyst.

From the following Set 15 database, generate **20 team compositions** ordered from highest to lowest expected win-rate.  
For each composition include:
  - "name"
  - "tier_rank" (1 = strongest, 30 = weakest)
  - "champions_early", "champions_mid", "champions_late" (arrays)
  - "carry" (main damage dealer)
  - "core_items" (dictionary champion→list[items])
  - "key_augments" (max 3 augments)
Output **valid JSON** only, inside a single top-level list.

Here is the database (trimmed for context):
```json
{json.dumps(db, ensure_ascii=False)[:8000]}
```
"""

# 4️⃣  Ejecuta la consulta
print("🔄 Generando composiciones con Gemini Pro...")
try:
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 4096,
        }
    )
    print("✅ Respuesta recibida de Gemini")
except Exception as e:
    print(f"❌ Error en API de Gemini: {e}")
    exit(1)

# 5️⃣  Procesa la respuesta
try:
    comps = json.loads(response.text)
    print(f"✅ Se generaron {len(comps)} composiciones")
except json.JSONDecodeError:
    print(f"❌ Respuesta no es JSON válido. Primeros 500 chars:\n{response.text[:500]}")
    comps = None

# 6️⃣  Crea archivo HTML simple
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
    <h1>🏆 TFT Set 15 - Meta Compositions</h1>
    <p><strong>Modelo:</strong> {MODEL}</p>
    
    <div class="comp">
        <h3>📊 Respuesta de Gemini Pro:</h3>
        <pre>{response.text if 'response' in locals() else 'Error: No se pudo obtener respuesta'}</pre>
    </div>
    
    {'<div class="comp"><h3>✅ Composiciones procesadas:</h3>' + '<br>'.join([f"<span class=\"tier\">#{comp.get('tier_rank', '?')}</span> {comp.get('name', 'Sin nombre')} - Carry: {comp.get('carry', 'N/A')}" for comp in (comps[:5] if comps else [])]) + '</div>' if comps else '<div class="comp"><h3>❌ No se pudieron procesar las composiciones</h3></div>'}
</body>
</html>"""

with open("tft_results.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("\n🎉 Resultados guardados en: tft_results.html")
if comps:
    print(f"\nTop 3 composiciones:")
    for comp in comps[:3]:
        print(f"  #{comp.get('tier_rank', '?')} {comp.get('name', 'Sin nombre')} — Carry: {comp.get('carry', 'N/A')}")
else:
    print("\n⚠️  No se pudieron procesar las composiciones. Revisa el archivo HTML para ver la respuesta completa.")