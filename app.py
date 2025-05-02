import streamlit as st

st.set_page_config(page_title="Midjourney Prompt Builder", layout="centered")
st.title("Midjourney Prompt Builder")
st.markdown("Build and customize prompts for Midjourney with ease.")

prompt = st.text_input("Describe your image prompt:", placeholder="A futuristic city at sunset")

col1, col2 = st.columns(2)
with col1:
    version = st.selectbox("Model Version (--v)", ["6", "5.2", "5.1", "5", "4"])
    aspect_ratio = st.selectbox("Aspect Ratio (--ar)", ["1:1", "16:9", "4:5", "2:3", "3:2", "9:16"])
    quality = st.selectbox("Quality (--q)", ["1", "0.5", "2"])
    stylization = st.slider("Stylization (--s)", 0, 1000, 250, step=50)
with col2:
    style = st.selectbox("Style (--style)", ["default", "raw", "4a", "4b", "4c"])
    chaos = st.slider("Chaos (--chaos)", 0, 100, 0, step=5)
    seed = st.text_input("Seed (--seed)", placeholder="Leave blank for random")

no_param = st.text_input("Exclude items (--no)", placeholder="e.g., text, people, watermarks")

final_prompt = prompt
if version: final_prompt += f" --v {version}"
if style and style != "default": final_prompt += f" --style {style}"
if aspect_ratio: final_prompt += f" --ar {aspect_ratio}"
if quality: final_prompt += f" --q {quality}"
if stylization is not None: final_prompt += f" --s {stylization}"
if chaos is not None: final_prompt += f" --chaos {chaos}"
if seed: final_prompt += f" --seed {seed}"
if no_param: final_prompt += f" --no {no_param}"

st.markdown("### Final Prompt")
st.code(final_prompt, language="bash")
st.info("Use your mouse or keyboard shortcut to copy the prompt.")
st.markdown("---")
st.markdown("Made with love for Midjourney creators.")
