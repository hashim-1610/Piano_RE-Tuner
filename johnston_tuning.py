"""
Ben Johnston - Sonata for Microtonal Piano: tuning table loader.

The 88 frequencies live in tuning.yaml (next to this file). Edit that file to
correct values; this module just loads and validates it.

Piano key number 1..88 (1 = A0). MIDI note number = key_number + 20.
"""

import math
from pathlib import Path

import yaml

YAML_PATH = Path(__file__).with_name("tuning.yaml")


def load_tuning(path=YAML_PATH):
    """Return {key_number: (note_name, target_hz)}, validated."""
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    table = {}
    for entry in data["keys"]:
        key = int(entry["key"])
        hz = float(entry["hz"])
        if key in table:
            raise ValueError(f"tuning.yaml: key {key} appears more than once")
        if hz <= 0:
            raise ValueError(f"tuning.yaml: key {key} has non-positive hz ({hz})")
        table[key] = (str(entry["name"]), hz)

    missing = sorted(set(range(1, 89)) - set(table))
    extra = sorted(set(table) - set(range(1, 89)))
    if missing or extra:
        raise ValueError(f"tuning.yaml must have keys 1..88 exactly. Missing: {missing}, unexpected: {extra}")
    return dict(sorted(table.items()))


JOHNSTON_TUNING = load_tuning()


def key_to_midi(key_number: int) -> int:
    return key_number + 20


def standard_12tet_hz(midi_note: int, a4_hz: float = 440.0) -> float:
    return a4_hz * (2 ** ((midi_note - 69) / 12))


def cents_deviation(target_hz: float, reference_hz: float) -> float:
    return 1200 * math.log2(target_hz / reference_hz)
