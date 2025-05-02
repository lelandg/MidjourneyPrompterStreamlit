import streamlit as st

st.set_page_config(page_title="Advanced Midjourney Prompt Builder", layout="centered")
st.title("Advanced Midjourney Prompt Builder")
st.markdown("Craft rich, detailed prompts for Midjourney using both creative and technical controls.")

# Section 1: Base Prompt
st.header("1. Base Prompt")
prompt = st.text_input("Main Description", placeholder="A futuristic city at sunset")

# Section 2: Descriptors
st.header("2. Descriptors")
subject = st.text_input("Subject", placeholder="robot, forest, mountain")
environment = st.text_input("Environment", placeholder="dense fog, underwater, outer space")
lighting = st.text_input("Lighting", placeholder="cinematic lighting, soft shadows, golden hour")
mood = st.text_input("Mood", placeholder="serene, intense, dystopian")

# Section 3: Artistic Style
st.header("3. Artistic Style")
art_style = st.selectbox("Art Style / Movement", ["None", "Cyberpunk", "Impressionism", "Surrealism", "Baroque", "Anime", "Vaporwave", "Minimalism"])
medium = st.selectbox("Medium", ["None", "Oil painting", "Digital art", "Pencil sketch", "Watercolor", "3D render", "Photo"])
artist_reference = st.text_input("Artist Reference", placeholder="Greg Rutkowski, Beeple")

# Section 4: Camera Settings
st.header("4. Camera Settings (for photo realism)")
camera_type = st.selectbox("Camera Type", ["None", "DSLR", "Mirrorless", "Smartphone", "Polaroid", "Film"])
lens = st.text_input("Lens", placeholder="85mm, wide-angle, fisheye")
aperture = st.text_input("Aperture", placeholder="f/1.4, f/5.6")

# Section 5: Midjourney Parameters
st.header("5. Midjourney Parameters")
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

no_param = st.text_input("Exclude Items (--no)", placeholder="e.g., text, people, watermarks")

# Section 6: Image Prompt
st.header("6. Optional Image Prompt")
image_url = st.text_input("Image URL", placeholder="https://example.com/image.jpg")
image_weight = st.slider("Image Weight (--iw)", 0.0, 2.0, 1.0, step=0.1)

# Build final prompt
components = [
    prompt, subject, environment, lighting, mood,
    art_style if art_style != "None" else "",
    medium if medium != "None" else "",
    artist_reference,
    camera_type if camera_type != "None" else "",
    lens, aperture
]
base_prompt = ", ".join(filter(None, components))

final_prompt = base_prompt
if image_url: final_prompt = f"{image_url} --iw {image_weight} " + final_prompt
if version: final_prompt += f" --v {version}"
if style and style != "default": final_prompt += f" --style {style}"
if aspect_ratio: final_prompt += f" --ar {aspect_ratio}"
if quality: final_prompt += f" --q {quality}"
if stylization is not None: final_prompt += f" --s {stylization}"
if chaos is not None: final_prompt += f" --chaos {chaos}"
if seed: final_prompt += f" --seed {seed}"
if no_param: final_prompt += f" --no {no_param}"

st.markdown("### Final Midjourney Prompt")
st.code(final_prompt, language="bash")
st.info("Copy this prompt to use in Midjourney via Discord.")
st.markdown("---")
st.markdown("Inspired by PrompterGuide.com and extended for modern Midjourney prompts.")
