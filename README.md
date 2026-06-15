# neutts-test

A minimal demonstration of the **NeuTTS** text‑to‑speech pipeline from the `neutts` library. The script synthesises speech conditioned on a reference audio clip and writes the result as a WAV file.

## Overview

The repository consists of:

- **`main.py`** – a single entry point that:
  1. Detects whether a CUDA GPU is available (falls back to CPU).
  2. Instantiates a `NeuTTS` object, loading the backbone and codec models from the public GitHub repos `neuphonic/neutts-air` and `neuphonic/neucodec`.
  3. Encodes a reference audio file (`chin.wav`) and its transcript (`chin.txt`).
  4. Calls `tts.infer` with a hard‑coded utterance to generate a waveform.
  5. Persists the waveform as `chin-test.wav` using the `soundfile` library.
- **Reference data** – `chin.wav` and `chin.txt` provide speaker/style conditioning for the synthesis.
- **`pyproject.toml`** – declares the Python runtime dependencies (`neutts`, `librosa`, `soundfile`) and uses **uv** for reproducible environment management.

## Quick‑Start

```bash
# Install dependencies (creates a reproducible environment)
uv sync

# Run the demo (generates chin-test.wav)
uv run python main.py
```

The script prints `wrote chin-test.wav` on success. Play the file with any audio player, e.g.:

```bash
ffplay chin-test.wav
```

## Customising the Utterance

Edit the string passed to `tts.infer` in `main.py` (line 22) to synthesize different text. Re‑run the script after saving your changes.

## GPU vs CPU

The code automatically selects CUDA if available. To force CPU execution, replace the device detection logic in `main.py` with:

```python
device = "cpu"
```

## Development

- **Dependency management** – always use `uv sync` after modifying `pyproject.toml`.
- **Iterative testing** – modify `main.py`, run the script, and listen to the output.
- **Extending** – you can add additional reference audio‑transcript pairs and call `tts.infer` repeatedly using the same `NeuTTS` instance for batch synthesis.

## License

The repository itself does not specify a license. The `neutts` library and the model weights it loads are subject to the upstream project's licensing terms.
