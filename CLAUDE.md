# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick‑start commands

| Goal | Command | Notes |
|------|---------|-------|
| Install / update dependencies | `uv sync` | Uses the `pyproject.toml` and the pinned `uv.lock`. All required packages (`neutts`, `librosa`, `soundfile`, etc.) are pulled automatically. |
| Run the demo script | `uv run python main.py` | Executes the single‑file entry point that generates `hus-test.wav`. |
| Re‑run with a custom phrase | `uv run python -c "from main import main; main()"` *(or edit `main.py`)* | Change the string passed to `tts.infer` in `main.py` to test other utterances. |
| Clean generated audio files | `rm -f *.wav` | Removes the output files (`hus-test.wav`, `new.wav`, `out.wav`, …). |
| Inspect the generated audio | `ffplay hus-test.wav`  *(or any audio player)* | Verify the result visually/audibly. |

*There is currently no automated test suite; the script itself serves as the functional test.*  

## High‑level architecture

```
└─ repository root
   ├─ pyproject.toml            ← project metadata, dependencies, uv lock source
   ├─ main.py                   ← single entry point
   └─ data files (hus.wav, hus.txt, …)  ← reference audio & transcript used by the demo
```

### Core flow (as implemented in `main.py`)

1. **Instantiate NeuTTS** –  
   ```python
   tts = NeuTTS(
       backbone_repo="neuphonic/neutts-air", backbone_device="cuda",
       codec_repo="neuphonic/neucodec",      codec_device="cuda",
   )
   ```
   *`NeuTTS`* (from the external `neutts` package) loads a pre‑trained TTS backbone and codec. Both are pulled from the specified GitHub repositories on first use.

2. **Prepare reference conditioning** –  
   ```python
   ref_codes = tts.encode_reference("hus.wav")
   ref_text  = open("hus.txt").read().strip()
   ```
   The reference audio (`hus.wav`) is encoded to obtain conditioning codes; the matching transcript (`hus.txt`) is read for optional textual guidance.

3. **Generate speech** –  
   ```python
   wav = tts.infer(
       "Hello I am hussain ...",   # user‑provided utterance
       ref_codes,
       ref_text
   )
   ```
   `tts.infer` synthesises a waveform (`numpy` array) conditioned on the reference.

4. **Persist the result** –  
   ```python
   sf.write("hus-test.wav", wav, 24000)
   ```
   The waveform is saved as a 24 kHz WAV file using the `soundfile` library.

5. **Entry point** –  
   The script runs `main()` when invoked as a module (`if __name__ == "__main__":`).

### External dependencies

| Package | Purpose |
|---------|---------|
| `neutts` (git source) | Provides the `NeuTTS` class and model loading logic. |
| `librosa` | Audio utilities used internally by `neutts`. |
| `soundfile` | Writes the final WAV file. |
| `uv` (CLI, not a Python package) | Recommended package manager for reproducible environments; already locked in `uv.lock`. |

## Development tips specific to this repo

* **Dependency management** – The project is built around **uv**. Running `uv sync` is the canonical way to create a reproducible environment; avoid mixing `pip install` unless you explicitly need an editable install.
* **Adding new functionality** – Extend `main.py` or create additional modules that import `NeuTTS`. Follow the same pattern: instantiate once, reuse the instance for multiple `infer` calls if you need batch synthesis.
* **Testing variations** – Since there is no test harness, a quick sanity check is to edit the string passed to `tts.infer` and rerun the script. If you need automated regression testing later, consider adding a `tests/` folder with `pytest` and using `uv run pytest`.
* **GPU vs CPU** – The script defaults to `cuda`. On a CPU‑only machine, replace `"cuda"` with `"cpu"` in the `NeuTTS` constructor.

## Repository metadata

* **Project name** – `neutts-test` (as defined in `pyproject.toml`).
* **License / contribution** – Not specified in the current files; follow the upstream `neutts` repository’s licensing when redistributing models or code.

---

*Claude Code can rely on the above sections to understand the build/run workflow, the primary code path, and how to extend or test the project.*