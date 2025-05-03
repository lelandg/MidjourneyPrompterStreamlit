import itertools
import json
from pathlib import Path

import streamlit as st

from version import __version__

# Must be the first Streamlit command!
st.set_page_config(
    page_title=f"Midjourney Prompter {__version__} (Editable)",
    layout="centered",
)
st.title(f"Midjourney Prompter v{__version__}")

# --------------------------- Load editable values ---------------------------
HERE = Path(__file__).parent


def load_json(name: str):
    path = HERE / "data" / f"{name}.json"
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        st.error(f"Couldn’t find {path}")
        return []


artists = load_json("artists")
styles = load_json("styles")
mediums = load_json("mediums")
moods = load_json("moods")
lighting = load_json("lighting")
colors = load_json("colors")  # << new color schemes

# ------------------------------ UI – Tabs -----------------------------------
tab1, tab2, tab3 = st.tabs(["🎯 Single Prompt", "🌀 Batch Mode", "🛠️ Edit Lists"])

# ============================================================================ #
#                               🎯 Single Prompt                                #
# ============================================================================ #
with tab1:
    st.header("Build a Single Prompt")

    # ---------------------------------------------------------------- “Core”
    subject = st.text_input("Subject")

    mood = st.selectbox("Mood", moods)
    lighting_sel = st.selectbox("Lighting", lighting)

    # ----------------вля Color Scheme -----------------------------------
    st.subheader("Color Scheme")
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_scheme = st.selectbox(
            "Choose a predefined scheme",
            [scheme["name"] for scheme in colors]
        )
    with col2:
        show_preview = st.checkbox("Show Preview", value=False)

    custom_input = st.text_input(
        "Or enter custom hex codes (comma-separated)",
        help="e.g., #FF0000, #00FF00, #0000FF"
    )

    if custom_input.strip():
        color = custom_input
        preview_colors = [c.strip() for c in custom_input.split(",") if c.strip()]
    else:
        color = selected_scheme
        preview_colors = next(
            scheme["colors"] for scheme in colors if scheme["name"] == selected_scheme
        )

    # Optional little color preview
    if show_preview:
        cols = st.columns(max(1, len(preview_colors)))
        for col, hexcode in zip(cols, preview_colors):
            col.markdown(
                f"<div style='background:{hexcode};width:40px;height:40px;"
                "border:1px solid #ccc;border-radius:4px;'></div>",
                unsafe_allow_html=True,
            )

    # ----------------------- Style / Medium / Artist ------------------------
    styles_sel = st.multiselect(
        "Styles",                        # keep the same visible label
        styles,
        default=["Cyberpunk", "Fantasy"],
        key="styles_sel"                 # NEW: unique key
    )
    mediums_sel = st.multiselect("Mediums", mediums, default=[m for m in ["Digital Art", "3D render"] if m in mediums], key="mediums_sel")
    artists_sel = st.multiselect("Artists", artists,  key="artists_sel")

    # ----------------------- Midjourney Parameters --------------------------
    st.subheader("Midjourney Parameters")

    col_p1, col_p2, col_p3 = st.columns(3)

    with col_p1:
        version = st.selectbox("Model Version (--v)", ["6", "5.2", "5.1", "5", "4"])
        aspect = st.selectbox("Aspect Ratio (--ar)", ["1:1", "16:9", "4:5", "2:3", "3:2", "9:16"])
        quality = st.selectbox("Quality (--q)", ["1", "0.5", "0.25", "2"], index=0)

    with col_p2:
        stylize = st.slider("Stylize (--stylize)", 0, 1000, 100, step=10)
        chaos = st.slider("Chaos (--chaos)", 0, 100, 0, step=5)
        weird = st.slider("Weird (--weird)", 0, 3000, 0, step=50)

    with col_p3:
        seed = st.text_input("Seed (--seed)", placeholder="Leave blank for random")
        stop = st.slider("Stop (% | --stop)", 10, 100, 100, step=5)
        tile = st.checkbox("Tile (--tile)", value=False)

    # Negative prompt / “no”
    no_prompt = st.text_input("Negative Prompt (--no)", placeholder="e.g., text, watermark")

    # Image weight
    iw = st.number_input("Image Weight (--iw)", min_value=0.0, max_value=2.0, value=1.0, step=0.1)

    # ----------------------- Build final prompt -----------------------------
    base_parts = [subject, mood, lighting_sel, color]
    base_parts.extend(mediums_sel)
    base_parts.extend(styles_sel)
    base_parts.extend(f"by {a}" for a in artists_sel)
    prompt = ", ".join(filter(None, base_parts))

    # Build parameter section
    params = [f"--v {version}", f"--ar {aspect}"]

    if quality != "1":
        params.append(f"--q {quality}")
    if stylize:
        params.append(f"--stylize {stylize}")
    if chaos:
        params.append(f"--chaos {chaos}")
    if weird:
        params.append(f"--weird {weird}")
    if seed.strip():
        params.append(f"--seed {seed.strip()}")
    if stop != 100:
        params.append(f"--stop {stop}")
    if tile:
        params.append("--tile")
    if iw != 1.0:
        params.append(f"--iw {iw}")
    if no_prompt.strip():
        params.append(f"--no {no_prompt.strip()}")

    final = f"{prompt} {' '.join(params)}"
    st.text_area("Final Prompt", final, height=120)

# ============================================================================ #
#                              🌀 Batch Prompt Generator                        #
# ============================================================================ #
with tab2:
    st.header("Batch Prompt Generator")
    st.markdown("Enter comma-separated values for batch combination:")

    col1, col2 = st.columns(2)
    with col1:
        subjects = st.text_input("Subjects", "robot, dragon, astronaut")
        moods_batch = st.multiselect("Moods", moods, default=["Serene", "Dystopian"], key="moods_batch")
        styles_batch = st.multiselect(
            "Styles",                        # label can stay identical
            styles,
            default=["Cyberpunk", "Fantasy"],
            key="styles_batch"               # NEW: different unique key
        )
    with col2:
        lightings_batch = st.multiselect("Lighting", lighting, default=["Cinematic lighting"], key="lighting_batch")
        mediums_batch = st.multiselect("Mediums", mediums, default=[m for m in ["Digital Art"] if m in mediums], key="mediums_batch")
        artists_batch = st.multiselect("Artists", artists,  key="artists_batch")

    # -------- Shared parameters for all prompts in the batch ---------------
    st.subheader("Shared Midjourney Parameters")
    col_b1, col_b2, col_b3 = st.columns(3)

    with col_b1:
        version_b = st.selectbox("Model Version (--v)", ["6", "5.2", "5.1", "5", "4"], key="ver_b")
        aspect_b = st.selectbox("Aspect Ratio (--ar)", ["1:1", "16:9", "4:5", "2:3", "3:2", "9:16"], key="ar_b")
        quality_b = st.selectbox("Quality (--q)", ["1", "0.5", "0.25", "2"], key="q_b")

    with col_b2:
        stylize_b = st.slider("Stylize (--stylize)", 0, 1000, 100, step=10, key="stylize_b")
        chaos_b = st.slider("Chaos (--chaos)", 0, 100, 0, step=5, key="chaos_b")
        weird_b = st.slider("Weird (--weird)", 0, 3000, 0, step=50, key="weird_b")

    with col_b3:
        seed_b = st.text_input("Seed (--seed)", key="seed_b")
        stop_b = st.slider("Stop (% | --stop)", 10, 100, 100, step=5, key="stop_b")
        tile_b = st.checkbox("Tile (--tile)", value=False, key="tile_b")

    no_batch = st.text_input("Negative Prompt (--no)", key="no_b")
    iw_b = st.number_input("Image Weight (--iw)", min_value=0.0, max_value=2.0, value=1.0, step=0.1, key="iw_b")

    auto_generate = st.checkbox("Auto-Generate", value=True, key="auto_generate_b")

    def build_param_string():
        params = [f"--v {version_b}", f"--ar {aspect_b}"]
        if quality_b != "1":
            params.append(f"--q {quality_b}")
        if stylize_b:
            params.append(f"--stylize {stylize_b}")
        if chaos_b:
            params.append(f"--chaos {chaos_b}")
        if weird_b:
            params.append(f"--weird {weird_b}")
        if seed_b.strip():
            params.append(f"--seed {seed_b.strip()}")
        if stop_b != 100:
            params.append(f"--stop {stop_b}")
        if tile_b:
            params.append("--tile")
        if iw_b != 1.0:
            params.append(f"--iw {iw_b}")
        if no_batch.strip():
            params.append(f"--no {no_batch.strip()}")
        return " ".join(params)

    param_string = build_param_string()
    prompts = []

    def generate_prompts():
        combos = itertools.product(
            subjects.split(","),
            moods_batch or [""],
            lightings_batch or [""],
            styles_batch or [""],
            mediums_batch or [""],
            artists_batch or [""],
        )
        for combo in combos:
            s, m, l, stl, med, a = [x.strip() for x in combo]
            base = ", ".join(filter(None, [s, m, l, med, stl, f"by {a}"]))
            prompts.append(f"{base} {param_string}")

    if auto_generate:
        generate_prompts()
        st.text_area("Generated Prompts", "\n".join(prompts), height=300)
        st.download_button("📥 Download as TXT", "\n".join(prompts), file_name="batch_prompts.txt")
    else:
        if st.button("Generate"):
            generate_prompts()
            st.text_area("Generated Prompts", "\n".join(prompts), height=300)
            st.download_button("📥 Download as TXT", "\n".join(prompts), file_name="batch_prompts.txt")

# ============================================================================ #
#                                🛠️ Edit Lists                                 #
# ============================================================================ #
with tab3:
    st.header("Edit Lists")
    st.markdown(
        "Edit the lists below to customise your options.<br>"
        "<b>Note:</b> Changes are temporary and will not persist after reload.",
        unsafe_allow_html=True,
    )

    # Sort lists for nicer display
    st.subheader("Artists")
    st.text_area("artists.json", json.dumps(sorted(artists), indent=2), height=150)

    st.subheader("Styles")
    st.text_area("styles.json", json.dumps(sorted(styles), indent=2), height=150)

    st.subheader("Mediums")
    st.text_area("mediums.json", json.dumps(sorted(mediums), indent=2), height=150)

    st.subheader("Moods")
    st.text_area("moods.json", json.dumps(sorted(moods), indent=2), height=150)

    st.subheader("Lighting")
    st.text_area("lighting.json", json.dumps(sorted(lighting), indent=2), height=150)

    st.subheader("Colors")
    st.text_area("colors.json", json.dumps(sorted(colors, key=lambda c: c['name']), indent=2), height=150)

    st.markdown("✂️ Copy updated JSON and commit to your repository to make it permanent.", unsafe_allow_html=True)