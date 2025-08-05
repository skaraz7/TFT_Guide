import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.metatft.com/'
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

comps = []

for comp in soup.select('.composition-class'):  # debes ajustar esto con la clase correcta
    name = comp.select_one('.comp-title').text
    tier = comp.select_one('.tier-label').text

    early_game = [e.text for e in comp.select('.early-unit')]
    mid_game = [m.text for m in comp.select('.mid-unit')]
    late_game = [l.text for l in comp.select('.late-unit')]

    core_items = {}  # podrías mapear esto más adelante
    augments = [a.text for a in comp.select('.augment-badge')]
    power_ups = {}  # mismo caso

    comps.append({
        "name": name,
        "tier": tier,
        "early_game": early_game,
        "mid_game": mid_game,
        "late_game": late_game,
        "core_items": core_items,
        "augments": augments,
        "power_ups": power_ups
    })

with open('comps.json', 'w', encoding='utf-8') as f:
    json.dump({"meta": {"last_update": "2025-08-04"}, "comps": comps}, f, indent=2, ensure_ascii=False)
