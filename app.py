import streamlit as st
import json
from pathlib import Path
import itertools
__version__ = "1.1"

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

tab1, tab2, tab3 = st.tabs(["🎯 Single Prompt", "🌀 Batch Mode", "🛠️ Edit Lists (Not Saved)"])

with tab1:
    st.header("Build a Single Prompt")
    subject = st.text_input("Subject")
    
    # Replace mood text_input with selectbox
    mood = st.selectbox("Mood", moods)
    
    lighting_sel = st.selectbox("Lighting", lighting)
    color   = st.text_input("Color Scheme")

    # --- now multi-selects with defaults ---
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

    # --- build prompt parts ---
    parts = [subject, mood, lighting_sel, color]
    parts.extend(mediums_sel)
    parts.extend(styles_sel)
    # prepend "by " to each selected artist
    parts.extend(f"by {a}" for a in artists_sel)

    prompt = ", ".join(filter(None, parts))
    final  = f"{prompt} --v {version} --ar {aspect}"
    st.text_area("Final Prompt", final, height=100)

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
    st.subheader("Artists")
    st.text_area("artists.json", json.dumps(artists, indent=2), height=150)
    st.subheader("Styles")
    st.text_area("styles.json", json.dumps(styles, indent=2), height=150)
    st.subheader("Mediums")
    st.text_area("mediums.json", json.dumps(mediums, indent=2), height=150)
    st.markdown("✂️ Copy this updated JSON and manually update the GitHub version to persist.")