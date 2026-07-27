"""
===============================================================================
Animated SVG Title Generator (Loki Series Aesthetic)
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

TEXT = "LOKI"
OUTPUT = "output.svg"
WIDTH = 8000
HEIGHT = 500
BACKGROUND = "#030806"
TEXT_COLOR = "#ebfce2"
PRIMARY_GOLD = "#d4af37"
SECONDARY_GOLD = "#f6e27a"
GREEN_MAGIC = "#6effa0"
GLOW_AURA = "#45e87a"

DURATION = 15.0
SEED = 1

ENABLE_GLOW = True
ENABLE_FONT_CYCLING = True
ENABLE_TIME_DISTORTION = True

# Glow & Shine Controls for Glowing Letters
GLOW_INTENSITY = 0.5   # Glow brightness multiplier (e.g. 0.2 = subtle, 1.0 = normal, 2.0 = ultra radiant)
GLOW_RADIUS = 3.0      # Glow halo blur spread radius multiplier (e.g. 0.5 to 2.5)

# Time Distortion Controls
DISTORTION_AMOUNT = 1.0  # Glitch/warp displacement scale multiplier (e.g. 0.0 = off, 0.5 = subtle, 1.0 = default, 2.5 = heavy warp)

# Typography Size, Gap & Canvas Controls
FONT_SIZE = 700.0         # Target text font size in pixels (e.g. 180.0 = compact, 280.0 = default, 450.0 = massive)
LETTER_GAP_FACTOR = 1.35  # Gap ratio multiplier between letters (e.g., 1.0 = normal, 1.35 = spacious gap, 2.0 = extra wide spacing)
AUTO_EXPAND_CANVAS = True # Automatically expand SVG canvas width & height if text length exceeds base canvas bounds

# Ambient White Particle Effect Controls
ENABLE_PARTICLES = True
PARTICLE_COUNT = 1000  # Number of static white particles (e.g. 0 = none, 30 = subtle, 60 = normal, 120 = dense cosmic dust)

# Custom local fonts folder
FONTS_DIR = "fonts"

# Custom local fonts configuration (OPTIONAL)
# NOTE: All .ttf, .otf, .woff, .woff2 files in the 'fonts/' folder are AUTOMATICALLY detected & used!
CUSTOM_FONTS = []

# =============================================================================
# FONTS & STYLES
# =============================================================================

# Comprehensive pool of Google and System font families
BASE_FONT_POOL = [
    # Google Fonts
    "Orbitron", "MedievalSharp", "Pirata One", "Audiowide",
    "Exo 2", "Syne Tactile", "UnifrakturMaguntia", "Bitcount Grid Double" ,
    # System Fonts
    "Garamond", "Courier New", "Papyrus", "Comic Sans MS", "Broadway"
]

# Default hero fonts pool to cycle through for settled character states
BASE_HERO_FONTS_POOL = [

]

# Dynamic pools populated at runtime including all custom fonts
FONT_POOL = list(BASE_FONT_POOL)
HERO_FONTS_POOL = list(BASE_HERO_FONTS_POOL)

# Character-specific hero font overrides (optional dictionary fallback)
HERO_CHARACTER_FONTS = {
    'L': "Dune Rise",
    'O': "Rune1",
    'K': "Dynamix",
    'I': "Cloisterblack"
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def load_custom_fonts() -> tuple[str, list[str]]:
    """
    Automatically scans FONTS_DIR folder (and working directory) for all font files (.ttf, .otf, .woff, .woff2),
    encodes them into Base64 Data URIs, generates @font-face CSS rules, and registers font-family names into pools.
    """
    css_rules = []
    loaded_font_names = []

    # Map of (abs_font_path) -> list of font_family_name aliases
    discovered = {}

    search_dirs = [FONTS_DIR, "."] if os.path.exists(FONTS_DIR) else ["."]

    # Process explicitly declared CUSTOM_FONTS first (if any)
    for font_name, font_path in CUSTOM_FONTS:
        resolved = None
        if os.path.exists(font_path):
            resolved = font_path
        elif os.path.exists(os.path.join(FONTS_DIR, font_path)):
            resolved = os.path.join(FONTS_DIR, font_path)
        elif os.path.exists(os.path.join(FONTS_DIR, os.path.basename(font_path))):
            resolved = os.path.join(FONTS_DIR, os.path.basename(font_path))
        if resolved:
            abs_p = os.path.abspath(resolved)
            discovered.setdefault(abs_p, [])
            if font_name not in discovered[abs_p]:
                discovered[abs_p].append(font_name)

    # Automatically scan directories for any font files
    for sdir in search_dirs:
        try:
            for fname in os.listdir(sdir):
                if fname.lower().endswith((".ttf", ".otf", ".woff", ".woff2")):
                    full_path = os.path.abspath(os.path.join(sdir, fname))
                    stem = fname.rsplit(".", 1)[0]
                    clean_name = stem.replace("-", " ").replace("_", " ").replace(".", " ").title().strip()
                    primary_name = clean_name if clean_name else stem

                    aliases = discovered.setdefault(full_path, [])
                    if primary_name and primary_name not in aliases:
                        aliases.append(primary_name)
        except Exception as e:
            print(f"Warning scanning font folder '{sdir}': {e}")

    for font_path, font_names in discovered.items():
        try:
            ext = font_path.lower().rsplit(".", 1)[-1]
            fmt = "opentype" if ext == "otf" else ("woff2" if ext == "woff2" else ("woff" if ext == "woff" else "truetype"))
            mime = f"font/{ext}"

            with open(font_path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode("utf-8")

            for fname in font_names:
                css_rules.append(
                    f"    @font-face {{\n"
                    f"      font-family: '{fname}';\n"
                    f"      src: url('data:{mime};charset=utf-8;base64,{b64_data}') format('{fmt}');\n"
                    f"      font-weight: normal;\n"
                    f"      font-style: normal;\n"
                    f"    }}\n"
                    f"    @font-face {{\n"
                    f"      font-family: '{os.path.splitext(os.path.basename(font_path))[0]}';\n"
                    f"      src: url('data:{mime};charset=utf-8;base64,{b64_data}') format('{fmt}');\n"
                    f"      font-weight: normal;\n"
                    f"      font-style: normal;\n"
                    f"    }}\n"
                )
                if fname not in loaded_font_names:
                    loaded_font_names.append(fname)

            print(f"Auto-detected custom font: {os.path.basename(font_path)} -> registered as '{font_names[0]}'")
        except Exception as e:
            print(f"Warning: Could not load custom font '{font_path}': {e}")

    return "".join(css_rules), loaded_font_names


def compute_layout() -> tuple[float, float, float, float, float, float]:
    """
    Computes SVG canvas dimensions (width, height) and typography placement math based on:
    - Base canvas dimensions (WIDTH, HEIGHT)
    - FONT_SIZE and LETTER_GAP_FACTOR
    - AUTO_EXPAND_CANVAS setting

    Returns: (actual_width, actual_height, start_x, center_y, letter_spacing_px, char_base_size)
    """
    text_chars = [c for c in TEXT if c != ' ']
    n_chars = len(text_chars)
    if n_chars == 0:
        return float(WIDTH), float(HEIGHT), float(WIDTH) / 2.0, float(HEIGHT) / 2.0, 0.0, FONT_SIZE

    target_char_size = max(30.0, float(FONT_SIZE))
    gap_mult = max(0.5, float(LETTER_GAP_FACTOR))

    letter_spacing_px = (target_char_size / 1.05) * gap_mult
    total_text_width = (n_chars - 1) * letter_spacing_px if n_chars > 1 else 0.0
    margin_x = target_char_size * 1.25

    needed_width = total_text_width + (margin_x * 2.0)
    needed_height = max(float(HEIGHT), target_char_size * 2.2)

    if AUTO_EXPAND_CANVAS:
        actual_width = max(float(WIDTH), needed_width)
        actual_height = max(float(HEIGHT), needed_height)
        char_base_size = target_char_size
    else:
        actual_width = float(WIDTH)
        actual_height = float(HEIGHT)
        max_allowed_w = actual_width * 0.86
        if total_text_width > max_allowed_w and n_chars > 1:
            letter_spacing_px = max_allowed_w / (n_chars - 1)
            char_base_size = (letter_spacing_px / gap_mult) * 1.05
            total_text_width = (n_chars - 1) * letter_spacing_px
        else:
            char_base_size = target_char_size

    start_x = (actual_width - total_text_width) / 2.0 if n_chars > 1 else actual_width / 2.0
    center_y = actual_height / 2.0 + (char_base_size * 0.06)

    return actual_width, actual_height, start_x, center_y, letter_spacing_px, char_base_size


def build_svg_header(canvas_w: float, canvas_h: float) -> str:
    """Generate SVG root tag with dynamic viewBox, dimensions, and styling."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {canvas_w:.1f} {canvas_h:.1f}" width="100%" height="100%" '
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

    # Atmospheric Green Halo Glow Filter (Generous filter bounds to eliminate box edge clipping)
    if ENABLE_GLOW:
        blur1 = max(1.0, 6.0 * GLOW_RADIUS)
        blur2 = max(2.0, 22.0 * GLOW_RADIUS)
        blur3 = max(5.0, 50.0 * GLOW_RADIUS)
        defs.append(
            '  <filter id="loki-green-glow" x="-200%" y="-200%" width="500%" height="500%">\n'
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

    # 3D Metallic Emboss Bevel Filter
    defs.append(
        '  <filter id="loki-emboss" x="-200%" y="-200%" width="500%" height="500%">\n'
        '    <feGaussianBlur stdDeviation="1" result="blur"/>\n'
        '    <feSpecularLighting in="blur" surfaceScale="4" specularConstant="1.4" specularExponent="22" lighting-color="#ffffff" result="spec">\n'
        '      <feDistantLight azimuth="135" elevation="50"/>\n'
        '    </feSpecularLighting>\n'
        '    <feComposite in="spec" in2="SourceAlpha" operator="in" result="specOut"/>\n'
        '    <feComposite in="SourceGraphic" in2="specOut" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" result="lit"/>\n'
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
            f'  <filter id="loki-time-distortion" x="-200%" y="-200%" width="500%" height="500%">\n'
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


def build_background(canvas_w: float, canvas_h: float) -> str:
    """Generate dark background covering the full canvas."""
    return (
        '<!-- Background -->\n'
        f'<rect width="{canvas_w:.1f}" height="{canvas_h:.1f}" fill="{BACKGROUND}" />\n'
        f'<rect width="{canvas_w:.1f}" height="{canvas_h:.1f}" fill="url(#loki-bg-glow)" />\n'
    )


def build_particles(canvas_w: float, canvas_h: float, start_x: float, center_y: float, letter_spacing_px: float, char_base_size: float) -> str:
    """
    Generate static white ambient particles clustered around text coordinates,
    fading and reducing in density as distance from text increases.
    """
    if not ENABLE_PARTICLES or PARTICLE_COUNT <= 0:
        return ""

    prng = random.Random(SEED + 999)
    p_elements = ['<!-- Static White Text-Clustered Particles -->\n', '<g id="loki-particles-group">\n']

    text_chars = [c for c in TEXT if c != ' ']
    n_chars = len(text_chars)
    if n_chars == 0:
        return ""

    total_width = (n_chars - 1) * letter_spacing_px if n_chars > 1 else 0.0

    for i in range(PARTICLE_COUNT):
        # Pick a random character anchor
        char_idx = prng.randint(0, max(0, n_chars - 1))
        anchor_x = start_x + char_idx * letter_spacing_px

        # Distance distribution: concentrated near (anchor_x, center_y) with falloff
        offset_x = prng.gauss(0, letter_spacing_px * 0.85) if n_chars > 1 else prng.gauss(0, char_base_size * 0.85)
        offset_y = prng.gauss(0, char_base_size * 0.65)

        cx = min(canvas_w - 15, max(15, anchor_x + offset_x))
        cy = min(canvas_h - 15, max(15, center_y + offset_y))

        # Calculate radial/vertical distance from nearest text region
        dist_x = max(0, abs(cx - (start_x + total_width / 2)) - total_width / 2) if n_chars > 1 else abs(cx - start_x)
        dist_y = abs(cy - center_y)
        dist_tot = math.sqrt(dist_x**2 + dist_y**2)

        # Exponential falloff for opacity and size as distance increases
        falloff = math.exp(-dist_tot / (char_base_size * 0.65 + 50))
        base_op = prng.uniform(0.2, 0.9) * falloff
        op = max(0.08, min(0.95, base_op))

        # Particles close to text are slightly larger/brighter
        r = prng.uniform(0.7, 3.2) * (0.6 + 0.4 * falloff)

        p_elements.append(
            f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.2f}" fill="#ffffff" opacity="{op:.2f}" />\n'
        )

    p_elements.append('</g>\n')
    return "".join(p_elements)


def build_typography(canvas_w: float, canvas_h: float, start_x: float, center_y: float, letter_spacing_px: float, char_base_size: float) -> str:
    """Generate character-by-character Loki font-cycling typography with unified group filters."""
    typo_elements = ['<!-- Animated Typography -->\n', '<g id="loki-title-group">\n']

    prng = random.Random(SEED + 42)
    text_chars = list(TEXT)
    n_chars = len(text_chars)
    if n_chars == 0:
        return ""

    def font_canonical(name: str) -> str:
        return name.lower().replace(" ", "").replace("-", "").replace("_", "").replace(".", "")

    # Combine font pools to ensure maximum variety of candidate hero fonts
    candidate_hero_fonts = []
    seen_canonical = set()
    for f in (HERO_FONTS_POOL + FONT_POOL):
        canon = font_canonical(f)
        if canon not in seen_canonical:
            seen_canonical.add(canon)
            candidate_hero_fonts.append(f)

    # Assign guaranteed unique settled hero font to each character
    used_hero_canonical = set()
    hero_font_assignments = {}

    for i, char in enumerate(text_chars):
        if char == ' ':
            continue

        selected_hero = None
        # Check if character has an explicit override in HERO_CHARACTER_FONTS that is still unused
        if char in HERO_CHARACTER_FONTS:
            override = HERO_CHARACTER_FONTS[char]
            if font_canonical(override) not in used_hero_canonical:
                selected_hero = override

        # Select next available unique font from candidate list
        if not selected_hero:
            for font in candidate_hero_fonts:
                if font_canonical(font) not in used_hero_canonical:
                    selected_hero = font
                    break

        # Fallback if text has more characters than total available unique fonts in all pools
        if not selected_hero:
            selected_hero = candidate_hero_fonts[i % len(candidate_hero_fonts)]

        used_hero_canonical.add(font_canonical(selected_hero))
        hero_font_assignments[i] = selected_hero

    # Pre-calculate character keyframes and font/weight sequences for sync
    char_data = []
    for i, char in enumerate(text_chars):
        if char == ' ':
            continue

        char_x = start_x + i * letter_spacing_px
        char_y = center_y
        hero_font = hero_font_assignments[i]

        cycling_fonts = []
        keytimes = []

        n_p1 = 25
        for s in range(n_p1):
            kt = (s / n_p1) * 0.45
            keytimes.append(kt)
            cycling_fonts.append(prng.choice(FONT_POOL))

        n_p2 = 10
        for s in range(n_p2):
            kt = 0.45 + (s / n_p2) * 0.30
            keytimes.append(kt)
            cycling_fonts.append(hero_font)

        n_p3 = 15
        for s in range(n_p3):
            kt = 0.75 + (s / n_p3) * 0.25
            keytimes.append(kt)
            cycling_fonts.append(prng.choice(FONT_POOL))

        keytimes.append(1.0)
        cycling_fonts.append(cycling_fonts[0])

        keytimes_str = "; ".join(f"{kt:.3f}" for kt in keytimes)
        fonts_str = "; ".join(cycling_fonts)
        weights = [prng.choice(["400", "700", "900", "800", "300"]) for _ in range(len(keytimes))]
        weights_str = "; ".join(weights)

        char_data.append({
            'index': i,
            'char': char,
            'x': char_x,
            'y': char_y,
            'hero_font': hero_font,
            'keytimes_str': keytimes_str,
            'fonts_str': fonts_str,
            'weights_str': weights_str,
        })

    print(f"Settled Hero Fonts (Guaranteed Unique for each letter in '{TEXT}'):")
    for cd in char_data:
        print(f"  Letter '{cd['char']}' (pos {cd['index'] + 1}) -> Settles on: '{cd['hero_font']}'")

    # Pass 1: Unified Luminous Outer Green Bloom Halo across ALL letters
    if ENABLE_GLOW:
        glow1_op = min(1.0, max(0.0, 0.85 * GLOW_INTENSITY))
        typo_elements.append(
            f'  <!-- Pass 1: Unified Outer Green Bloom Halo -->\n'
            f'  <g id="loki-glow-outer-group" filter="url(#loki-green-glow)" opacity="{glow1_op:.2f}">\n'
        )
        for cd in char_data:
            typo_elements.append(
                f'    <g transform="translate({cd["x"]:.1f}, {cd["y"]:.1f})">\n'
                f'      <text x="0" y="0" class="loki-text" font-size="{char_base_size:.1f}" fill="{GREEN_MAGIC}">{html.escape(cd["char"])}\n'
            )
            if ENABLE_FONT_CYCLING:
                typo_elements.append(
                    f'        <animate attributeName="font-family" calcMode="discrete" values="{cd["fonts_str"]}" keyTimes="{cd["keytimes_str"]}" dur="{DURATION}s" repeatCount="indefinite" />\n'
                )
            typo_elements.append('      </text>\n    </g>\n')
        typo_elements.append('  </g>\n')

        # Pass 2: Unified Soft Inner Mint Glow Halo across ALL letters
        glow2_op = min(1.0, max(0.0, 0.9 * GLOW_INTENSITY))
        typo_elements.append(
            f'  <!-- Pass 2: Unified Inner Mint Glow Halo -->\n'
            f'  <g id="loki-glow-inner-group" filter="url(#loki-green-glow)" opacity="{glow2_op:.2f}">\n'
        )
        for cd in char_data:
            typo_elements.append(
                f'    <g transform="translate({cd["x"]:.1f}, {cd["y"]:.1f})">\n'
                f'      <text x="0" y="0" class="loki-text" font-size="{char_base_size:.1f}" fill="{TEXT_COLOR}">{html.escape(cd["char"])}\n'
            )
            if ENABLE_FONT_CYCLING:
                typo_elements.append(
                    f'        <animate attributeName="font-family" calcMode="discrete" values="{cd["fonts_str"]}" keyTimes="{cd["keytimes_str"]}" dur="{DURATION}s" repeatCount="indefinite" />\n'
                )
            typo_elements.append('      </text>\n    </g>\n')
        typo_elements.append('  </g>\n')

    # Pass 3: Core Radiant Mint-White Text Face with Bevel Emboss & Time Distortion
    filter_attr = 'filter="url(#loki-time-distortion) url(#loki-emboss)"' if (ENABLE_TIME_DISTORTION and DISTORTION_AMOUNT > 0.0) else 'filter="url(#loki-emboss)"'
    typo_elements.append(
        f'  <!-- Pass 3: Core Radiant Text Face -->\n'
        f'  <g id="loki-core-text-group" {filter_attr}>\n'
    )
    for cd in char_data:
        typo_elements.append(
            f'    <g id="letter-group-{cd["index"]}" transform="translate({cd["x"]:.1f}, {cd["y"]:.1f})">\n'
            f'      <text x="0" y="0" class="loki-text" font-size="{char_base_size:.1f}" fill="{TEXT_COLOR}">{html.escape(cd["char"])}\n'
        )
        if ENABLE_FONT_CYCLING:
            typo_elements.append(
                f'        <animate attributeName="font-family" calcMode="discrete" values="{cd["fonts_str"]}" keyTimes="{cd["keytimes_str"]}" dur="{DURATION}s" repeatCount="indefinite" />\n'
                f'        <animate attributeName="font-weight" calcMode="discrete" values="{cd["weights_str"]}" keyTimes="{cd["keytimes_str"]}" dur="{DURATION}s" repeatCount="indefinite" />\n'
            )
        typo_elements.append('      </text>\n    </g>\n')
    typo_elements.append('  </g>\n')

    typo_elements.append('</g>\n')
    return "".join(typo_elements)


def build_svg() -> str:
    """Assemble standalone SVG string with dynamic auto-expanding canvas."""
    random.seed(SEED)

    canvas_w, canvas_h, start_x, center_y, letter_spacing_px, char_base_size = compute_layout()

    svg_parts = []
    svg_parts.append(build_svg_header(canvas_w, canvas_h))
    svg_parts.append(build_svg_defs())
    svg_parts.append(build_background(canvas_w, canvas_h))
    svg_parts.append(build_particles(canvas_w, canvas_h, start_x, center_y, letter_spacing_px, char_base_size))
    svg_parts.append(build_typography(canvas_w, canvas_h, start_x, center_y, letter_spacing_px, char_base_size))
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
