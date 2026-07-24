"""
===============================================================================
Animated SVG Title Generator (Loki Series Aesthetic)
===============================================================================
Generates a clean, high-impact animated SVG title card inspired by the
Marvel Loki title sequence:
  - Asynchronous font cycling per character across diverse typefaces
  - Shifting character weights, sizes, and font-families
  - Metallic gold lettering with subtle green magic glow
  - Dark cinematic background with subtle central aura
  - Pure SVG SMIL animations (10-second loop)

Run:
  python generator.py

Output:
  output.svg
===============================================================================
"""

import base64
import math
import random
import html
import os

# =============================================================================
# CONFIGURATION BLOCK
# =============================================================================

TEXT = "L O K I"
OUTPUT = "output.svg"
WIDTH = 1800
HEIGHT = 900
BACKGROUND = "#030806"
TEXT_COLOR = "#ebfce2"
PRIMARY_GOLD = "#d4af37"
SECONDARY_GOLD = "#f6e27a"
GREEN_MAGIC = "#6effa0"
GLOW_AURA = "#45e87a"

DURATION = 12.0
SEED = 2

ENABLE_GLOW = True
ENABLE_FONT_CYCLING = True
ENABLE_TIME_DISTORTION = True

# Glow & Shine Controls for Glowing Letters
GLOW_INTENSITY = 0.5   # Glow brightness multiplier (e.g. 0.2 = subtle, 1.0 = normal, 2.0 = ultra radiant)
GLOW_RADIUS = 1.5      # Glow halo blur spread radius multiplier (e.g. 0.5 to 2.5)

# Time Distortion Controls
DISTORTION_AMOUNT = 0.5  # Glitch/warp displacement scale multiplier (e.g. 0.0 = off, 0.5 = subtle, 1.0 = default, 2.5 = heavy warp)

# Custom local fonts folder
FONTS_DIR = "fonts"

# Custom local fonts configuration: List of (font_family_name, font_file_path)
# Any .ttf or .otf files placed in FONTS_DIR will also be auto-discovered!
CUSTOM_FONTS = [
    ("Old English Five", "old-english-five.regular.ttf"),
    ("usangel", "usangel.ttf"),
    ("ARB 85 Poster Script JAN-39 FRE", "ARB 85 Poster Script JAN-39 FRE.ttf"),
    ("CloisterBlack", "CloisterBlack.ttf"),
]

# =============================================================================
# FONTS & STYLES
# =============================================================================

# Comprehensive pool of Google and System font families
BASE_FONT_POOL = [
    # Google Fonts
    "Cinzel Decorative", "Cinzel", "Playfair Display", "Orbitron", "Montserrat",
    "MedievalSharp", "Pirata One", "Audiowide", "Oswald", "Bebas Neue",
    "Fira Code", "Exo 2", "Rajdhani", "Syne", "Chakra Petch", "UnifrakturMaguntia",
    # System Fonts
    "Georgia", "Garamond", "Times New Roman", "Impact", "Trebuchet MS",
    "Courier New", "Papyrus", "Copperplate", "Verdana", "Comic Sans MS", "Arial Black"
]

# Default hero fonts pool to cycle through for settled character states
BASE_HERO_FONTS_POOL = [
    "Cinzel Decorative", "Orbitron", "MedievalSharp", "Playfair Display",
    "UnifrakturMaguntia", "Bebas Neue", "Audiowide", "Montserrat",
    "Pirata One", "Syne", "Oswald", "Chakra Petch", "Exo 2"
]

# Dynamic pools populated at runtime including all custom fonts
FONT_POOL = list(BASE_FONT_POOL)
HERO_FONTS_POOL = list(BASE_HERO_FONTS_POOL)

# Character-specific hero font overrides (optional dictionary fallback)
HERO_CHARACTER_FONTS = {
    'L': "Old English Five",
    'O': "Orbitron",
    'K': "MedievalSharp",
    'I': "Playfair Display"
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def load_custom_fonts() -> tuple[str, list[str]]:
    """
    Scans configured CUSTOM_FONTS, the FONTS_DIR folder, and current directory for .ttf/.otf files,
    encodes them into Base64 @font-face CSS rules, and returns (css_string, font_names).
    """
    css_rules = []
    loaded_font_names = []
    font_entries = list(CUSTOM_FONTS)

    # Search directories for auto-discovery
    search_dirs = [FONTS_DIR, "."] if os.path.exists(FONTS_DIR) else ["."]
    for sdir in search_dirs:
        try:
            for fname in os.listdir(sdir):
                if fname.lower().endswith((".ttf", ".otf")):
                    rel_path = os.path.join(sdir, fname) if sdir != "." else fname
                    if not any(fpath == fname or fpath == rel_path for _, fpath in font_entries):
                        clean_name = fname.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title()
                        font_entries.append((clean_name, rel_path))
        except Exception:
            pass

    for font_name, font_path in font_entries:
        # Resolve path: try exact path, then FONTS_DIR/font_path, then basename in FONTS_DIR
        resolved_path = None
        if os.path.exists(font_path):
            resolved_path = font_path
        elif os.path.exists(os.path.join(FONTS_DIR, font_path)):
            resolved_path = os.path.join(FONTS_DIR, font_path)
        elif os.path.exists(os.path.join(FONTS_DIR, os.path.basename(font_path))):
            resolved_path = os.path.join(FONTS_DIR, os.path.basename(font_path))

        if resolved_path:
            try:
                ext = resolved_path.lower().rsplit(".", 1)[-1]
                fmt = "opentype" if ext == "otf" else "truetype"
                mime = f"font/{ext}"

                with open(resolved_path, "rb") as f:
                    b64_data = base64.b64encode(f.read()).decode("utf-8")

                css_rules.append(
                    f"    @font-face {{\n"
                    f"      font-family: '{font_name}';\n"
                    f"      src: url('data:{mime};charset=utf-8;base64,{b64_data}') format('{fmt}');\n"
                    f"      font-weight: normal;\n"
                    f"      font-style: normal;\n"
                    f"    }}\n"
                )
                if font_name not in loaded_font_names:
                    loaded_font_names.append(font_name)
            except Exception as e:
                print(f"Warning: Could not load custom font '{font_path}': {e}")

    return "".join(css_rules), loaded_font_names


def build_svg_header() -> str:
    """Generate SVG root tag with viewBox, dimensions, and styling."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" width="100%" height="100%" '
        f'style="background-color: {BACKGROUND}; width: 100%; height: 100%; display: block;">\n'
    )


def build_svg_defs() -> str:
    """Build SVG styles, gradients, and filters."""
    global FONT_POOL, HERO_FONTS_POOL
    defs = ["<defs>\n"]

    # Load and Base64 embed all custom fonts
    custom_css, custom_font_names = load_custom_fonts()

    # Prepend all discovered custom fonts to the active font pools
    for cname in reversed(custom_font_names):
        if cname not in FONT_POOL:
            FONT_POOL.insert(0, cname)
        if cname not in HERO_FONTS_POOL:
            HERO_FONTS_POOL.insert(0, cname)

    # Google Fonts Import & CSS Definitions
    defs.append(
        '  <style type="text/css">\n'
        f'{custom_css}'
        '    @import url("https://fonts.googleapis.com/css2?family=Audiowide&amp;family=Bebas+Neue&amp;family=Chakra+Petch:wght@700&amp;family=Cinzel+Decorative:wght@700;900&amp;family=Cinzel:wght@700;900&amp;family=Exo+2:wght@800&amp;family=Fira+Code:wght@700&amp;family=MedievalSharp&amp;family=Montserrat:wght@800;900&amp;family=Orbitron:wght@700;900&amp;family=Oswald:wght@700&amp;family=Pirata+One&amp;family=Playfair+Display:wght@900&amp;family=Rajdhani:wght@700&amp;family=Syne:wght@800&amp;family=UnifrakturMaguntia&amp;display=swap");\n'
        '    .loki-text { text-anchor: middle; dominant-baseline: central; font-weight: 900; }\n'
        '  </style>\n'
    )

    # Metallic Gold Linear Gradient
    defs.append(
        '  <linearGradient id="loki-gold-grad" x1="0%" y1="0%" x2="100%" y2="100%">\n'
        '    <stop offset="0%" stop-color="#4a3508" />\n'
        f'    <stop offset="20%" stop-color="{PRIMARY_GOLD}" />\n'
        '    <stop offset="40%" stop-color="#fff8d6" />\n'
        '    <stop offset="60%" stop-color="#8a6314" />\n'
        f'    <stop offset="80%" stop-color="{SECONDARY_GOLD}" />\n'
        '    <stop offset="100%" stop-color="#ffd700" />\n'
        '  </linearGradient>\n'
    )

    # Metallic Bevel Stroke Gradient
    defs.append(
        '  <linearGradient id="loki-bevel-grad" x1="0%" y1="100%" x2="100%" y2="0%">\n'
        '    <stop offset="0%" stop-color="#2a1d04" />\n'
        f'    <stop offset="50%" stop-color="{PRIMARY_GOLD}" />\n'
        '    <stop offset="100%" stop-color="#ffffff" />\n'
        '  </linearGradient>\n'
    )

    # Background Radial Vignette & Aura Gradient
    defs.append(
        '  <radialGradient id="loki-bg-glow" cx="50%" cy="50%" r="65%">\n'
        f'    <stop offset="0%" stop-color="#0f2619" stop-opacity="0.75" />\n'
        f'    <stop offset="45%" stop-color="#08140d" stop-opacity="0.85" />\n'
        f'    <stop offset="80%" stop-color="{BACKGROUND}" stop-opacity="1" />\n'
        '  </radialGradient>\n'
    )

    # Atmospheric Green Halo Glow Filter (Matches reference screenshot bloom)
    if ENABLE_GLOW:
        blur1 = max(1.0, 6.0 * GLOW_RADIUS)
        blur2 = max(2.0, 22.0 * GLOW_RADIUS)
        blur3 = max(5.0, 50.0 * GLOW_RADIUS)
        defs.append(
            '  <filter id="loki-green-glow" x="-80%" y="-80%" width="260%" height="260%">\n'
            f'    <feGaussianBlur stdDeviation="{blur1:.1f}" result="blur1" />\n'
            f'    <feGaussianBlur stdDeviation="{blur2:.1f}" result="blur2" />\n'
            f'    <feGaussianBlur stdDeviation="{blur3:.1f}" result="blur3" />\n'
            '    <feMerge>\n'
            '      <feMergeNode in="blur3" />\n'
            '      <feMergeNode in="blur2" />\n'
            '      <feMergeNode in="blur1" />\n'
            '      <feMergeNode in="SourceGraphic" />\n'
            '    </feMerge>\n'
            '  </filter>\n'
        )

    # 3D Metallic Emboss Bevel & Shadow Filter
    defs.append(
        '  <filter id="loki-emboss" x="-20%" y="-20%" width="140%" height="140%">\n'
        '    <feGaussianBlur stdDeviation="1" result="blur"/>\n'
        '    <feSpecularLighting in="blur" surfaceScale="4" specularConstant="1.4" specularExponent="22" lighting-color="#ffffff" result="spec">\n'
        '      <feDistantLight azimuth="135" elevation="50"/>\n'
        '    </feSpecularLighting>\n'
        '    <feComposite in="spec" in2="SourceAlpha" operator="in" result="specOut"/>\n'
        '    <feComposite in="SourceGraphic" in2="specOut" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" result="lit"/>\n'
        '    <feDropShadow dx="0" dy="14" stdDeviation="12" flood-color="#000000" flood-opacity="0.95"/>\n'
        '  </filter>\n'
    )

    # Time Distortion / Glitch Filter
    if ENABLE_TIME_DISTORTION and DISTORTION_AMOUNT > 0.0:
        base_scale = max(0.0, 25.0 * DISTORTION_AMOUNT)
        s1 = max(0.0, 35.0 * DISTORTION_AMOUNT)
        s2 = max(0.0, 2.0 * DISTORTION_AMOUNT)
        s3 = max(0.0, 28.0 * DISTORTION_AMOUNT)
        s4 = max(0.0, 1.0 * DISTORTION_AMOUNT)
        s5 = max(0.0, 35.0 * DISTORTION_AMOUNT)
        defs.append(
            f'  <filter id="loki-time-distortion" x="-30%" y="-30%" width="160%" height="160%">\n'
            f'    <feTurbulence type="fractalNoise" baseFrequency="0.04 0.8" numOctaves="2" result="noise">\n'
            f'      <animate attributeName="baseFrequency" values="0.02 0.8; 0.1 0.05; 0.01 0.9; 0.02 0.8" keyTimes="0; 0.35; 0.7; 1" dur="{DURATION}s" repeatCount="indefinite"/>\n'
            f'    </feTurbulence>\n'
            f'    <feDisplacementMap in="SourceGraphic" in2="noise" scale="{base_scale:.1f}" xChannelSelector="R" yChannelSelector="G" result="warped">\n'
            f'      <animate attributeName="scale" values="{s1:.1f}; {s2:.1f}; {s3:.1f}; {s4:.1f}; {s5:.1f}" keyTimes="0; 0.3; 0.55; 0.85; 1" dur="{DURATION}s" repeatCount="indefinite"/>\n'
            f'    </feDisplacementMap>\n'
            f'  </filter>\n'
        )

    defs.append("</defs>\n")
    return "".join(defs)


def build_background() -> str:
    """Generate dark background."""
    return (
        '<!-- Background -->\n'
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{BACKGROUND}" />\n'
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#loki-bg-glow)" />\n'
    )


def build_typography() -> str:
    """Generate character-by-character Loki font-cycling typography for any arbitrary word/text."""
    typo_elements = ['<!-- Animated Typography -->\n', '<g id="loki-title-group">\n']

    prng = random.Random(SEED + 42)
    text_chars = list(TEXT)
    n_chars = len(text_chars)
    if n_chars == 0:
        return ""

    # Dynamic Layout math: scale font-size and spacing to fit any word length within canvas width
    max_text_width = WIDTH * 0.86
    if n_chars > 1:
        letter_spacing_px = min(260.0, max_text_width / (n_chars - 1))
    else:
        letter_spacing_px = 0.0

    char_base_size = min(320.0, letter_spacing_px * 1.25) if n_chars > 1 else 320.0
    total_width = (n_chars - 1) * letter_spacing_px
    start_x = (WIDTH - total_width) / 2
    center_y = HEIGHT / 2 + (char_base_size * 0.06)

    for i, char in enumerate(text_chars):
        if char == ' ':
            continue

        char_x = start_x + i * letter_spacing_px
        char_y = center_y

        # Determine settled hero font for this character
        if char in HERO_CHARACTER_FONTS:
            hero_font = HERO_CHARACTER_FONTS[char]
        else:
            hero_font = HERO_FONTS_POOL[i % len(HERO_FONTS_POOL)]

        cycling_fonts = []
        keytimes = []

        # Phase 1: Rapid cycling (25 shifts)
        n_p1 = 25
        for s in range(n_p1):
            kt = (s / n_p1) * 0.45
            keytimes.append(kt)
            cycling_fonts.append(prng.choice(FONT_POOL))

        # Phase 2: Settled Hero Font (10 shifts holding hero font)
        n_p2 = 10
        for s in range(n_p2):
            kt = 0.45 + (s / n_p2) * 0.30
            keytimes.append(kt)
            cycling_fonts.append(hero_font)

        # Phase 3: Rapid cycling again (15 shifts)
        n_p3 = 15
        for s in range(n_p3):
            kt = 0.75 + (s / n_p3) * 0.25
            keytimes.append(kt)
            cycling_fonts.append(prng.choice(FONT_POOL))

        # Final keyTime at 1.0
        keytimes.append(1.0)
        cycling_fonts.append(cycling_fonts[0]) # Loop seamlessly back to initial font

        keytimes_str = "; ".join(f"{kt:.3f}" for kt in keytimes)
        fonts_str = "; ".join(cycling_fonts)

        # Font weight variation sequence matching keytimes
        weights = [prng.choice(["400", "700", "900", "800", "300"]) for _ in range(len(keytimes))]
        weights_str = "; ".join(weights)

        filter_attr = 'filter="url(#loki-time-distortion) url(#loki-emboss)"' if (ENABLE_TIME_DISTORTION and DISTORTION_AMOUNT > 0.0) else 'filter="url(#loki-emboss)"'

        typo_elements.append(f'  <!-- Letter {html.escape(char)} -->\n')
        typo_elements.append(f'  <g id="letter-group-{i}" transform="translate({char_x:.1f}, {char_y:.1f})">\n')

        # Layer 1: Luminous Outer Green Bloom Halo
        if ENABLE_GLOW:
            glow1_op = min(1.0, max(0.0, 0.85 * GLOW_INTENSITY))
            typo_elements.append(
                f'    <text x="0" y="0" class="loki-text" font-size="{char_base_size:.1f}" '
                f'fill="{GREEN_MAGIC}" opacity="{glow1_op:.2f}" filter="url(#loki-green-glow)">{html.escape(char)}\n'
            )
            if ENABLE_FONT_CYCLING:
                typo_elements.append(
                    f'      <animate attributeName="font-family" calcMode="discrete" values="{fonts_str}" keyTimes="{keytimes_str}" dur="{DURATION}s" repeatCount="indefinite" />\n'
                )
            typo_elements.append('    </text>\n')

        # Layer 2: Soft Inner Mint Glow Halo
        glow2_op = min(1.0, max(0.0, 0.9 * GLOW_INTENSITY))
        typo_elements.append(
            f'    <text x="0" y="0" class="loki-text" font-size="{char_base_size:.1f}" '
            f'fill="{TEXT_COLOR}" opacity="{glow2_op:.2f}" filter="url(#loki-green-glow)">{html.escape(char)}\n'
        )
        if ENABLE_FONT_CYCLING:
            typo_elements.append(
                f'      <animate attributeName="font-family" calcMode="discrete" values="{fonts_str}" keyTimes="{keytimes_str}" dur="{DURATION}s" repeatCount="indefinite" />\n'
            )
        typo_elements.append('    </text>\n')

        # Layer 3: Core Radiant Mint-White Text Face
        typo_elements.append(
            f'    <text x="0" y="0" class="loki-text" font-size="{char_base_size:.1f}" '
            f'fill="{TEXT_COLOR}" {filter_attr}>{html.escape(char)}\n'
        )
        if ENABLE_FONT_CYCLING:
            typo_elements.append(
                f'      <animate attributeName="font-family" calcMode="discrete" values="{fonts_str}" keyTimes="{keytimes_str}" dur="{DURATION}s" repeatCount="indefinite" />\n'
            )
            typo_elements.append(
                f'      <animate attributeName="font-weight" calcMode="discrete" values="{weights_str}" keyTimes="{keytimes_str}" dur="{DURATION}s" repeatCount="indefinite" />\n'
            )
        typo_elements.append('    </text>\n')

        typo_elements.append('  </g>\n')

    typo_elements.append('</g>\n')
    return "".join(typo_elements)


def build_svg() -> str:
    """Assemble standalone SVG string."""
    random.seed(SEED)

    svg_parts = []
    svg_parts.append(build_svg_header())
    svg_parts.append(build_svg_defs())
    svg_parts.append(build_background())
    svg_parts.append(build_typography())
    svg_parts.append('</svg>\n')

    return "".join(svg_parts)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print(f"Generating Loki title card SVG for: '{TEXT}'...")
    svg_content = build_svg()

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(svg_content)

    file_size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"Successfully generated '{OUTPUT}' ({file_size_kb:.1f} KB).")


if __name__ == "__main__":
    main()
