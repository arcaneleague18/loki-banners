# Loki Title Card SVG Generator

A standalone, pure Python SVG generator that creates **100% vector, SMIL-animated title cards** inspired by the iconic font-cycling intro sequence from Marvel Studios' ***LOKI*** series.

Generates standalone, self-contained SVG files with Base64 embedded fonts, multi-pass halogen glows, time-distortion glitching, and text-clustered ambient dust particles—with **zero external JavaScript dependencies**.

<img width="700" height="83" alt="output (1)" src="https://github.com/user-attachments/assets/cb11b7f4-f406-48ef-ae4b-6f94bad53eae" />

<img width="700" height="83" alt="output" src="https://github.com/user-attachments/assets/53a56cd5-b137-41f3-b2a0-4f665084853d" />


## Features

- **Dynamic Font Cycling**: Character-by-character discrete font transitions using Google Fonts, system fonts, and local custom `.ttf` / `.otf` / `.woff` files.
- **Pure SMIL Animations**: 100% native SVG `<animate>` and `<animateTransform>` tags for smooth, continuous animation in any modern browser or SVG viewer.
- **Automatic Font Detection**: Drop any font files (`.ttf`, `.otf`, `.woff`, `.woff2`) into the `fonts/` folder—they are automatically discovered, Base64-encoded, embedded, and added to the font cycling pool.
- **Luminous Halogen Bloom**: Multi-pass Gaussian blur halo filters (`#ebfce2` core text, `#6effa0` emerald aura, `#030806` dark void background) matching the reference show aesthetic.
- **Static Text-Clustered Dust Particles**: White ambient dust particles clustered around the text with exponential Gaussian distance falloff.
- **Temporal Glitch Distortion**: Configurable fractal noise displacement map animation (`DISTORTION_AMOUNT`) simulating timeline variance glitches.
- **Dynamic Layout Scaling**: Automatic math that calculates character base size and letter spacing to fit any custom word or phrase (e.g. `"LOKI"`, `"MULTIVERSE"`, `"VARUN KARLI"`) without overlapping or clipping.
- **Fully Customizable Controls**: Intuitive configuration block for tweaking glow intensity, blur radius, glitch scale, letter gap factor, and particle counts.

---

## Project Structure

```
loki/
├── fonts/                             # Custom fonts folder (Auto-discovered)
│   ├── ARB 85 Poster Script...ttf
│   ├── CloisterBlack.ttf
│   ├── ka1.ttf
│   ├── old-english-five.regular.ttf
│   ├── orbitron.medium.ttf
│   ├── PixelPurl.ttf
│   └── usangel.ttf
├── generator.py                       # Main standalone Python SVG Generator
├── output.svg                         # Output animated vector SVG
└── README.md                          # Project documentation
```

---

## Quick Start

### Prerequisites
- **Python 3.7+**
- Uses **only standard Python library modules** (`math`, `random`, `html`, `os`, `base64`). No `pip install` required!

### Running the Generator

```bash
python generator.py
```

This will automatically scan the `fonts/` directory, process the configuration, and output `output.svg`. Open `output.svg` in any web browser (Chrome, Edge, Firefox, Safari) to view the animation.

---

## 🎛️ Configuration Guide

All settings are exposed in the **Configuration Block** at the top of [`generator.py`](file:///c:/Users/varun/OneDrive/Desktop/hehe/loki/generator.py):

```python
# =============================================================================
# CONFIGURATION BLOCK
# =============================================================================

TEXT = "LOKI"               # Word or phrase to animate
OUTPUT = "output.svg"        # Output SVG file path
WIDTH = 1800                # SVG ViewBox canvas width
HEIGHT = 500                # SVG ViewBox canvas height
BACKGROUND = "#030806"       # Dark void background color
TEXT_COLOR = "#ebfce2"       # Main mint-white text face color
GREEN_MAGIC = "#6effa0"      # Luminous green glow halo color

DURATION = 12.0             # Full animation cycle duration in seconds
SEED = 0                    # Random seed for reproducible font sequences & particles

ENABLE_GLOW = True           # Toggle green halo bloom
ENABLE_FONT_CYCLING = True   # Toggle character font-cycling animation
ENABLE_TIME_DISTORTION = True# Toggle temporal glitch warp filter

# Glow & Shine Controls
GLOW_INTENSITY = 0.5        # Glow brightness multiplier (0.2 = subtle, 1.0 = normal, 2.0 = radiant)
GLOW_RADIUS = 1.5           # Glow halo blur spread radius multiplier (0.5 to 2.5)

# Time Distortion Controls
DISTORTION_AMOUNT = 0.5     # Glitch/warp displacement scale (0.0 = off, 0.5 = subtle, 2.5 = heavy warp)

# Typography Gap & Spacing Controls
LETTER_GAP_FACTOR = 1.35    # Gap multiplier between letters (1.0 = compact, 1.35 = spacious)

# Ambient White Particle Effect Controls
ENABLE_PARTICLES = True     # Toggle ambient white dust particles
PARTICLE_COUNT = 30         # Number of text-clustered static white particles
```

---

## Adding Custom Fonts

To add your own custom fonts to the font-cycling animation:

1. Copy any `.ttf`, `.otf`, `.woff`, or `.woff2` font file into the `fonts/` directory.
2. Run `python generator.py`.
3. The script will automatically detect the new font, Base64 encode it, inject `@font-face` rules into the SVG `<style>`, and include it in the active font cycling pools!

---

## License

Created for pair programming & creative demonstration purposes. Open source under the MIT License.
