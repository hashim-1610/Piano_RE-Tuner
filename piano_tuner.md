# Piano Tuner: how the pipeline works

This document explains the whole system from the keys of the piano to the sound from the speakers, and why it was built this way.

## 1. The problem

Ben Johnston's *Sonata for Microtonal Piano* does not use standard piano tuning. The score includes a "Retuning the Piano" table listing a target frequency in hertz for each of the 88 keys. In the original setup the pianist retunes the strings with an electronic tuner (the table also lists switch settings for a Motorola Scalatron tuner) and then plays the piece on that retuned acoustic piano.

The goal of this project: hear and study that tuning **without retuning a physical piano**, by playing a digital piano and having a program produce the sound at Johnston's frequencies.

## 2. Key idea: MIDI carries no pitch

A MIDI keyboard does not send a frequency. When you press a key it sends a short message:

| Byte | Meaning | Example |
| --- | --- | --- |
| status | "note on", channel 1 | `144` (`0x90`) |
| data 1 | key number | `60` (middle C) |
| data 2 | velocity (how hard) | `85` |

Releasing the key sends a "note off" for the same key number. Whatever makes the sound decides what frequency "key 60" means. Standard instruments use equal temperament. This program uses Johnston's table instead. **That substitution is the retuning.**

## 3. The pipeline

```
digital piano --USB MIDI--> browser (Web MIDI API) --> JavaScript app
                                                          |
                                      look up key in Johnston table
                                                          |
                                   Web Audio oscillator at that frequency
                                                          |
                                                  laptop speakers
```

1. **Digital piano.** Only senses which keys are pressed. Its own sound is not used, so "Local Control" is switched off.
2. **USB MIDI.** Modern Windows treats most pianos as standard USB-MIDI devices; no driver or MIDI software is needed.
3. **Web MIDI API (Chrome, Edge).** Lets a web page receive MIDI messages directly. The page registers a handler that is called for every message.
4. **Lookup.** The handler reads the key number and finds that key's entry in the tuning table.
5. **Web Audio API.** The app creates an oscillator whose frequency is set to the exact Hz from the table, gives it a volume from the velocity, and connects it to the audio output.
6. **Release.** On note-off the oscillator fades out quickly. If the sustain pedal (MIDI controller 64) is down, the fade-out waits until the pedal is released.

## 4. Key numbering

The book numbers the keys 1 to 88 (key 1 = A0, the lowest A; key 88 = C8). MIDI numbers the same keys 21 to 108. So:

```
MIDI note = book key number + 20
```

For example key 37 (A3) is MIDI note 57 and its target is 220 Hz, which equals standard tuning and serves as an anchor.

## 5. Standard frequency and cents

For comparison, the standard (equal temperament) frequency of a MIDI note `n` with A4 = 440 Hz is:

```
f_standard = 440 * 2^((n - 69) / 12)
```

The difference between Johnston's pitch and the standard one is measured in **cents** (100 cents = 1 semitone):

```
cents = 1200 * log2(f_johnston / f_standard)
```

Examples from the table:

| Key | Note | Johnston (Hz) | Standard (Hz) | Offset |
| --- | --- | --- | --- | --- |
| 1 | A0 | 26.62 | 27.50 | about -56 cents |
| 37 | A3 | 220.00 | 220.00 | 0 cents |
| 40 | C4 (middle C) | 263.97 | 261.63 | about +15 cents |
| 88 | C8 | 4630.40 | 4186.01 | about +175 cents |

The extremes differ a lot from standard tuning. That comes from the table in the score; it is not a calculation error.

## 6. Why not pitch bend?

A first idea was to send MIDI pitch-bend messages so a normal synthesizer would shift each note. That approach has problems:

- Pitch bend applies to **every note on a channel at once**, so two held notes with different offsets cannot be bent independently (this would need one channel per note, or MPE).
- The standard bend range is only +/- 2 semitones (200 cents), and key 88 needs about +175 cents, which is close to the limit.

Generating each tone directly at its target frequency avoids both problems: every held key has its own oscillator with its own frequency, and any offset is possible.

## 7. The data and how it is built

- `tuning.yaml` holds the 88 `key / name / hz` values. It is the only place numbers are edited.
- `johnston_tuning.py` loads the YAML and **validates** it: exactly keys 1 to 88, no duplicates, positive frequencies.
- `generate_js_table.py` converts it to a table indexed by MIDI note (with the standard frequency added) and writes it into `harmonic_compass.template.html`, producing the finished `harmonic_compass.html` and `tuning_table.json`.
- The built page is self-contained: no internet, no libraries.

The values were checked against the printed table in the score. The Scalatron switch-setting column is not used, because it only applies to the original hardware tuner.

## 8. The interface

- **Johnston / Standard switch:** the same keys use either column of the table, so the tunings can be compared by ear.
- **Now playing:** note name, key number, frequency, and offset in cents, with a needle on a -200 to +200 cent gauge.
- **88-key keyboard:** keys light up as played; it can also be played with the mouse or computer keyboard for testing without a piano.
- **Tuning table:** all 88 keys with Johnston Hz, standard Hz and offset; the row for the last played note is highlighted.
- **Tone options:** sine (pure, best for checking pitch with a tuner app), triangle, and a softer mix of a triangle and two quiet overtones. These are synthesised, not sampled piano sounds.

## 9. How to check that it works

1. With the computer keyboard or piano, play key 37 (A3). The page should show 220.00 Hz and offset 0.
2. Play key 40 (middle C). The page should show 263.97 Hz and about +15.4 cents.
3. Choose the **sine** tone and hold a key next to a phone tuner app. The tuner should read the table frequency, not the standard one. Switch to **Standard** to see it move to the equal-temperament value.
4. Hold two keys with different offsets (for example keys 40 and 44). Both should keep their own pitch.

## 10. Limitations

- The sound is a simple synthesised tone rather than a piano sample.
- There is a small latency (a few milliseconds) from key press to sound.
- Notes outside the 88-key range are ignored.
- It is a simulation: the strings of an acoustic piano are not changed.
- Only the Johnston table is supported so far.
- Real-piano testing depends on the piano's MIDI support; the on-screen keyboard is the fallback.

## 11. Possible next steps

Sampled piano sounds, support for several tuning files, a parser for Johnston's accidental notation (so other tunings can be generated rather than typed), unit tests, and a Python version that retunes MIDI for an external synth. See `CONTRIBUTING.md`.

## 12. Source

Frequencies: the "Retuning the Piano" table in Ben Johnston, *Sonata for Microtonal Piano* (scan not included in the repository for copyright reasons).
