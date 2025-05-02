# MidjourneyPrompterStreamlit

MidjourneyPrompterStreamlit is an interactive guide for crafting prompts and running them through a Streamlit interface. Whether you're new to prompt engineering or looking for a streamlined workflow, this tool helps you build, preview, and manage prompts with ease.

---

## Table of Contents

1. [Features](#features)  
2. [Installation](#installation)  
3. [Install on Streamlit](#install-on-streamlit)  
4. [Basic Usage](#basic-usage)  
5. [Configuration](#configuration)  
6. [Deploy on Streamlit](#deploy-on-streamlit)  
7. [Contributing](#contributing)  
8. [License](#license)  

---

## Features

- Interactive prompt builder with live preview  
- Predefined templates for common use cases  
- Copy-to-clipboard for generated prompts  
- Export prompts as text or CSV  
- Easy configuration via YAML or JSON  

---

## Installation

1. Clone the repository  
   ```bash
   git clone https://github.com/yourusername/MidjourneyPrompterStreamlit.git
   cd MidjourneyPrompterStreamlit
   ```
2. Create and activate a virtual environment (optional but recommended)  
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

---

## Install on Streamlit

Streamlit apps can be hosted online through the Streamlit Community Cloud. To install and set up this app:

1. Fork or clone the repository to your GitHub account.  
2. Log in to https://streamlit.io/cloud with your GitHub account.  
3. Create a new application:  
   - Click **New app** in the dashboard.  
   - Point the app to your repository and the branch where your code resides.  
   - Specify the main script path (e.g., `app.py`).  
4. Ensure the `requirements.txt` file exists in the repository's root and lists all necessary dependencies. Generate one if missing:  
   ```bash
   pip freeze > requirements.txt
   ```  
5. Set environment variables if required by the app. This can be done in the "Advanced settings" section during deployment.  
6. Click **Deploy** to launch your app.  

Your app will be live and available to anyone with the URL provided.

---

## Basic Usage

After installation, launch the Streamlit app locally: