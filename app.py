import streamlit as st
import json
from pathlib import Path
import itertools
__version__ = "1.1"

st.write("🔥 Hello from the top of app.py!")
st.set_page_config(page_title=f"Midjourney Prompter {__version__} (Editable)", layout="centered")
st.title(f"Midjourney Prompter v{__version__}")

# Load editable values
def load_json(name):
    try:
        return json.load(open(Path("data") / f"{name}.json"))
    except:
        return []

artists = load_json("artists")
styles = load_json("styles")
mediums = load_json("mediums")
moods = load_json("moods")
lighting = load_json("lighting")
colors = load_json("colors")    # << load our new color schemes

tab1, tab2, tab3 = st.tabs(["🎯 Single Prompt", "🌀 Batch Mode", "🛠️ Edit Lists"])

with tab1:
    st.header("Build a Single Prompt")
    subject = st.text_input("Subject")

    # Replace mood text_input with selectbox
    mood = st.selectbox("Mood", moods)

    lighting_sel = st.selectbox("Lighting", lighting)

    # ----------------------------------------------------------------
    st.subheader("Color Scheme")

    # put dropdown and preview checkbox on the same row
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_scheme = st.selectbox(
            "Choose a predefined scheme",
            [scheme["name"] for scheme in colors]
        )
    # after `selected_scheme = ...`
    preview_colors = []
    for scheme in colors:
        if scheme.get("name") == selected_scheme:
            preview_colors = scheme.get("colors", [])
            break
    # or
    # preview_colors = next(
    #     (s["colors"] for s in colors if s["name"]==selected_scheme),
    #     []
    # )
    with col2:
        show_preview = st.checkbox("Show Preview", value=False)

    custom_input = st.text_input(
        "Or enter custom hex codes (comma-separated)",
        help="e.g., red, green, blue = #FF0000, #00FF00, #0000FF"
    )

    # decide which list of colors to preview
    if custom_input.strip():
        color = custom_input
        preview_colors = [c.strip() for c in custom_input.split(",") if c.strip()]
    else:
        color = selected_scheme
        preview_colors = next(
            scheme["colors"] for scheme in colors
            if scheme["name"] == selected_scheme
        )

    if show_preview:
        st.markdown("**Preview:**")
        if selected_scheme == "Complementary":
            for i in range(0, len(preview_colors), 2):
                cols = st.columns(2)
                for col, hexcode in zip(cols, preview_colors[i:i+2]):
                    col.markdown(
                        f"<div style='background:{hexcode};width:40px;height:40px;"
                        "border:1px solid #ccc;border-radius:4px;'></div>",
                        unsafe_allow_html=True,
                    )
                st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
        else:
            cols = st.columns(max(1, len(preview_colors)))
            for col, hexcode in zip(cols, preview_colors):
                col.markdown(
                    f"<div style='background:{hexcode};width:40px;height:40px;"
                    "border:1px solid #ccc;border-radius:4px;'></div>",
                    unsafe_allow_html=True,
                )
    # ----------------------------------------------------------------

    # --- now your existing styles / mediums / artists multiselects etc. ---
    styles_sel = st.multiselect(
        "Styles",
        options=styles,
        default=[s for s in ["Cyberpunk", "Fantasy"] if s in styles]
    )
    mediums_sel = st.multiselect(
        "Mediums",
        options=mediums,
        default=[m for m in ["Digital Art", "3D render"] if m in mediums]
    )
    artists_sel = st.multiselect(
        "Artists",
        options=artists,
        default=[a for a in ["Moebius", "Basil Wolverton"] if a in artists]
    )
    version = st.selectbox("Model Version (--v)", ["6","5.2","5.1","5","4"])
    aspect  = st.selectbox("Aspect Ratio (--ar)", ["1:1","16:9","4:5","2:3","3:2","9:16"])

    # --- build prompt ---
    parts = [subject, mood, lighting_sel, color]
    parts.extend(mediums_sel)
    parts.extend(styles_sel)
    parts.extend(f"by {a}" for a in artists_sel)
    prompt = ", ".join(filter(None, parts))
    final  = f"{prompt} --v {version} --ar {aspect}"
    st.text_area("Final Prompt", final, height=100)
    # ----------------------------------------------------------------

with tab2:
    st.header("Batch Prompt Generator")
    st.markdown("Enter comma-separated values for batch combination:")

    col1, col2 = st.columns(2)
    with col1:
        subjects = st.text_input("Subjects", "robot, dragon, astronaut")

        # Replace moods text_input with multiselect or selectbox
        moods_batch = st.multiselect("Moods", moods, default=["Serene", "Dystopian", "Joyful"], key="moods_batch")

        styles_batch = st.multiselect("Styles", styles, default=["Cyberpunk", "Fantasy"], key="styles_batch")
    with col2:
        lightings_batch = st.multiselect("Lighting", lighting, default=["Cinematic lighting", "Golden hour"], key="lightings_batch")
        medium_defaults = [m for m in ["Digital Art", "3D render"] if m in mediums]
        mediums_batch = st.multiselect("Mediums", mediums, default=medium_defaults, key="mediums_batch")
        artists_batch = st.multiselect("Artists", artists, default=["Greg Rutkowski", "Beeple"], key="artists_batch")

    version_b = st.selectbox("Model Version (--v)", ["6", "5.2", "5.1", "5", "4"], key="ver2")
    aspect_b = st.selectbox("Aspect Ratio (--ar)", ["1:1", "16:9", "4:5", "2:3", "3:2", "9:16"], key="ar2")

    # Add Auto Generate checkbox
    auto_generate = st.checkbox("Auto Generate", value=True, key="auto_generate")

    # Initialize prompts list and generated flag
    prompts = []

    # If auto_generate is False, show the Generate button and generate prompts only on click
    if not auto_generate:
        if st.button("Generate", key="generate_button"):
            combos = list(itertools.product(
                subjects.split(","), moods_batch, lightings_batch,
                styles_batch, mediums_batch, artists_batch
            ))

            for combo in combos:
                s, m, l, stl, med, a = [x.strip() for x in combo]
                prompts.append(f"{s}, {m}, {l}, {med}, {stl}, by {a} --v {version_b} --ar {aspect_b}")

            st.text_area("Generated Prompts", "\n".join(prompts), height=300)
            st.download_button("📥 Download Prompts as TXT", data="\n".join(prompts), file_name="batch_prompts.txt")

    # If auto_generate is True, generate prompts automatically
    else:
        combos = list(itertools.product(
            subjects.split(","), moods_batch, lightings_batch,
            styles_batch, mediums_batch, artists_batch
        ))

        for combo in combos:
            s, m, l, stl, med, a = [x.strip() for x in combo]
            prompts.append(f"{s}, {m}, {l}, {med}, {stl}, by {a} --v {version_b} --ar {aspect_b}")

        st.text_area("Generated Prompts", "\n".join(prompts), height=300)
        st.download_button("📥 Download Prompts as TXT", data="\n".join(prompts), file_name="batch_prompts.txt")

with tab3:
    st.header("Edit Lists")
    st.markdown(
        "Edit the lists below to customize your options.<BR/><B>Note: Fields are not saved outside your session.</B>",
        unsafe_allow_html=True
    )

    # Sort the lists for display
    artists_sorted = sorted(artists)
    styles_sorted  = sorted(styles)
    mediums_sorted = sorted(mediums)
    moods_sorted   = sorted(moods)
    lighting_sorted = sorted(lighting)
    colors_sorted  = sorted(colors, key=lambda scheme: scheme["name"])

    st.subheader("Artists")
    st.text_area("artists.json", json.dumps(artists_sorted, indent=2), height=150)

    st.subheader("Styles")
    st.text_area("styles.json", json.dumps(styles_sorted, indent=2), height=150)

    st.subheader("Mediums")
    st.text_area("mediums.json", json.dumps(mediums_sorted, indent=2), height=150)

    st.subheader("Moods")
    st.text_area("moods.json", json.dumps(moods_sorted, indent=2), height=150)

    st.subheader("Lighting")
    st.text_area("lighting.json", json.dumps(lighting_sorted, indent=2), height=150)

    st.subheader("Colors")
    st.text_area("colors.json", json.dumps(colors_sorted, indent=2), height=150)

    st.markdown(
        "✂️ Copy this updated JSON and manually update the GitHub version to persist.",
        unsafe_allow_html=True
    )