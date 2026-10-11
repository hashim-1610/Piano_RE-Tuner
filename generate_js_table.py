"""
Rebuild everything that depends on tuning.yaml:
  - tuning_table.json
  - harmonic_compass.html  (from harmonic_compass.template.html)

Usage (from this folder):   python generate_js_table.py
Requires:                   pip install pyyaml
"""

import json
from pathlib import Path

from johnston_tuning import JOHNSTON_TUNING, key_to_midi, standard_12tet_hz, cents_deviation

HERE = Path(__file__).parent
PLACEHOLDER = "__TUNING_TABLE__"

table = {}
for key, (name, target_hz) in JOHNSTON_TUNING.items():
    midi = key_to_midi(key)
    table[midi] = {
        "name": name,
        "johnstonHz": target_hz,
        "standardHz": round(standard_12tet_hz(midi), 3),
    }

(HERE / "tuning_table.json").write_text(json.dumps(table, indent=2), encoding="utf-8")

template = (HERE / "harmonic_compass.template.html").read_text(encoding="utf-8")
if PLACEHOLDER not in template:
    raise SystemExit(f"{PLACEHOLDER} not found in harmonic_compass.template.html")
html = template.replace(PLACEHOLDER, json.dumps(table))
(HERE / "harmonic_compass.html").write_text(html, encoding="utf-8")

print(f"Built tuning_table.json and harmonic_compass.html from tuning.yaml ({len(table)} keys).")
for key in (1, 37, 40, 88):
    name, hz = JOHNSTON_TUNING[key]
    cents = cents_deviation(hz, standard_12tet_hz(key_to_midi(key)))
    print(f"  key {key:2d} {name:>2s}: {hz} Hz ({cents:+.1f} cents from standard)")
