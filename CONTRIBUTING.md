# Contributing

Thanks for wanting to help. This is a small student project, so the process is light.

## Getting set up

1. Clone the repository.
2. `pip install -r requirements.txt` (only needed to rebuild the page).
3. Open `harmonic_compass.html` in Chrome or Edge to try the app.

## Ground rules

- **Edit the sources, not the build.** Change `tuning.yaml` for data and `harmonic_compass.template.html` for the app, then run `python generate_js_table.py`. Do not hand-edit `harmonic_compass.html` or `tuning_table.json`.
- **Do not add the book scan or other copyrighted material.** The score page is intentionally in `.gitignore`.
- **Say how you tested.** For example "played keys 37 and 40 and checked with a tuner app" in your pull request.
- Keep pull requests small and about one thing.

## Changing a tuning value

Edit the `hz` number on that key's line in `tuning.yaml`, rebuild, and include the book page or reasoning that supports the change.

## Open tasks

Each of these is meant to be doable in an afternoon or a few evenings. Say which one you are taking so two people don't do the same thing.

**Sound**
- [ ] Replace the synthesised tone with sampled piano notes, played at the Johnston frequencies (the sample's pitch has to be shifted to the exact Hz in the table).
- [ ] Add a sustain-pedal test and a note-off envelope that sounds less abrupt.

**Tuning data**
- [ ] Support several tuning files with a dropdown to switch between them (for example a just-intonation scale or quarter-tones).
- [ ] Add a "compare" view that plots Johnston against equal temperament for all 88 keys.

**Notation (the larger task)**
- [ ] Write a parser that turns Johnston's accidental symbols into frequency ratios, so tunings for other pieces can be generated instead of typed in.

**Quality**
- [ ] Add unit tests for `johnston_tuning.py` (88 keys present, no duplicates, key 37 is 220 Hz, cents maths).
- [ ] Add a check that `harmonic_compass.html` is up to date with `tuning.yaml`.

**Other platforms**
- [ ] A Python version using `mido` and `python-rtmidi` that receives MIDI, retunes it, and sends it on to a software synth.

**Documentation**
- [ ] A short beginner explanation of just intonation and cents, with diagrams.
- [ ] Notes on which digital pianos and USB adapters have been tested.

## Questions

Open an issue, or ask the project author directly.
