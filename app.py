import streamlit as st
import json
from pathlib import Path
import itertools

st.set_page_config(page_title="Midjourney Prompter v3.4+ (Editable)", layout="centered")
st.title("Midjourney Prompter v3.4+")

# Load editable values
def load_json(name):
    try:
        return json.load(open(Path("data") / f"{name}.json"))
    except:
        return []

artists = load_json("artists")
styles = load_json("styles")
mediums = load_json("mediums")

tab1, tab2, tab3 = st.tabs(["🎯 Single Prompt", "🌀 Batch Mode", "🛠️ Edit Lists"])

with tab1:
    st.header("Build a Single Prompt")
    subject = st.text_input("Subject")
    mood = st.text_input("Mood")
    lighting = st.text_input("Lighting")
    color = st.text_input("Color Scheme")
    artist = st.selectbox("Artist", ["None"] + artists)
    style = st.selectbox("Style", ["None"] + styles)
    medium = st.selectbox("Medium", ["None"] + mediums)
    version = st.selectbox("Model Version (--v)", ["6", "5.2", "5.1", "5", "4"])
    aspect = st.selectbox("Aspect Ratio (--ar)", ["1:1", "16:9", "4:5", "2:3", "3:2", "9:16"])

    parts = [subject, mood, lighting, color]
    if medium != "None": parts.append(medium)
    if style != "None": parts.append(style)
    if artist != "None": parts.append(f"by {artist}")
    prompt = ", ".join(filter(None, parts))
    final = f"{prompt} --v {version} --ar {aspect}"
    st.text_area("Final Prompt", final, height=100)

with tab2:
    st.header("Batch Prompt Generator")
    st.markdown("Enter comma-separated values for batch combination:")

    col1, col2 = st.columns(2)
    with col1:
        subjects = st.text_input("Subjects", "robot, dragon, astronaut")
        moods = st.text_input("Moods", "serene, dystopian, joyful")
        styles_batch = st.multiselect("Styles", styles, default=["Cyberpunk", "Fantasy"])
    with col2:
        lightings = st.text_input("Lighting", "cinematic lighting, golden hour")
        mediums_batch = st.multiselect("Mediums", mediums, default=["Digital art", "3D render"])
        artists_batch = st.multiselect("Artists", artists, default=["Greg Rutkowski", "Beeple"])

    version_b = st.selectbox("Model Version (--v)", ["6", "5.2", "5.1", "5", "4"], key="ver2")
    aspect_b = st.selectbox("Aspect Ratio (--ar)", ["1:1", "16:9", "4:5", "2:3", "3:2", "9:16"], key="ar2")

    combos = list(itertools.product(
        subjects.split(","), moods.split(","), lightings.split(","),
        styles_batch, mediums_batch, artists_batch
    ))

    prompts = []
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