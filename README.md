# Harmonic Compass

A browser app that plays a digital piano in **Ben Johnston's retuned piano tuning** from his *Sonata for Microtonal Piano*. You play a MIDI keyboard; the sound you hear is generated at Johnston's target frequency for each of the 88 keys instead of standard equal temperament.

The original piece asks the pianist to physically retune the strings of an acoustic piano. This project reproduces that tuning electronically, so it can be heard and studied without retuning an instrument.

## Quick start

1. Open `harmonic_compass.html` in **Chrome or Edge** (Firefox and Safari do not support Web MIDI).
2. Plug in a digital piano via USB, reload the page, allow the MIDI permission, pick the piano and click **Connect**.
3. Switch **Local Control off** on the piano so you do not also hear its own untuned sound.
4. Play. Use the **Johnston / Standard** switch to compare the two tunings.

No piano yet? Click the on-screen keys, or use the computer keyboard (`A` to `K` for white keys, `W E T Y U` for black keys, `Z` / `X` to change octave).

No installation is needed to play. If the piano is not detected when you open the file directly, run `python -m http.server 8000` in this folder and open `http://localhost:8000/harmonic_compass.html`.

## How it works, in short

Piano key press, then a MIDI note-on message (key number and velocity), read by the browser through the Web MIDI API. The app looks up the key in the Johnston table and the Web Audio API plays a tone at exactly that frequency. The full explanation is in [piano_tuner.md](piano_tuner.md).

## Project layout

| File | Purpose |
| --- | --- |
| `tuning.yaml` | The 88 target frequencies. **The single source of truth: edit values here.** |
| `johnston_tuning.py` | Loads and validates `tuning.yaml`; helper functions for MIDI numbers and cents. |
| `generate_js_table.py` | Rebuilds `tuning_table.json` and `harmonic_compass.html` from the YAML. |
| `harmonic_compass.template.html` | The app's source (HTML, CSS, JavaScript). Edit this, not the built page. |
| `harmonic_compass.html` | The built, self-contained app. Generated; do not edit directly. |
| `tuning_table.json` | Generated lookup table (MIDI note to Johnston and standard Hz). |
| `piano_tuner.md` | Detailed write-up of the pipeline and design decisions. |
| `CONTRIBUTING.md` | How to help, and a list of open tasks. |

## Rebuilding after editing the tuning

```bash
pip install -r requirements.txt
python generate_js_table.py
```

## Data source

The frequencies come from the "Retuning the Piano" table printed with Ben Johnston's *Sonata for Microtonal Piano*. The scan of that page is not included in this repository because it is copyrighted. All 88 values were checked against the printed table. The table's Scalatron switch settings are not used.

## About `tuning.yaml` and reuse

`tuning.yaml` was created by the project author from the "Retuning the Piano" table in the library copy of Johnston's score. The author photographed the page, and the 88 frequencies were transcribed from that photo into the YAML file and checked against the printed table. Johnston's piece is the only data set so far.

The retuner itself is not tied to this one piece. The app only needs a table that maps each of the 88 keys to a frequency, so the same code can play other tunings: swap or extend `tuning.yaml` (or add further tuning files) and the same keys, MIDI input and sound engine retune to different notes. The file can be changed or expanded for other pieces, scales and tuning systems, depending on the use case. See [CONTRIBUTING.md](CONTRIBUTING.md) for ideas.

## Status and known limits

- Sound is a simple synthesised tone, not a sampled piano. The goal so far is pitch accuracy.
- Tested with the computer keyboard and on-screen keys; real-piano testing is in progress.
- Only this one tuning is supported at the moment.

## License

MIT. See the `LICENSE` file.
