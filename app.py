import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
from PIL import Image
from voice import speak_product
import gdown
import time
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Product Scanner",
    page_icon="logo.png",
    layout="centered"
)

# Hide Streamlit internal status details
st.set_option("client.showErrorDetails", False)

# ---------------- CONSTANTS ----------------
IMG_SIZE = 128
MODEL_PATH = "product_model.keras"
CSV_PATH = "product.csv"  # Unified this path
LOGO_PATH = "logo.png"
FILE_ID = '1cr3Xg8J8M40Gy-pfW_bq_9onL9QbxI4F'

# ---------------- LOADING SCREEN (SPINNING LOGO) ----------------
if "loaded" not in st.session_state:
    st.session_state.loaded = True
    loader = st.empty()
    with loader.container():
        st.markdown(
            """
            <style>
            .loader-container{
                display:flex;
                justify-content:center;
                align-items:center;
                height:80vh;
                flex-direction:column;
            }
            .spin-logo{
                width:180px;
                animation: spin 2.5s linear infinite;
            }
            @keyframes spin{
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            </style>
            <div class="loader-container">
                <img src="scanner_logo.jpg" class="spin-logo">
                <h3>Initializing Product Scanner...</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
    time.sleep(2) # Reduced slightly for better UX
    loader.empty()

# ---------------- SESSION STATE ----------------
if "last_spoken" not in st.session_state:
    st.session_state.last_spoken = None

# ---------------- CLASS NAMES ----------------
class_names = [
    'Amul_Milk','Chakra_Gold','Colgate_Paste','Colgate_Tooth_Brush',
    'Dettol','Dove_Soap','Fortune_Oil','Harpic','Himalaya_Shamapoo',
    'Lizol','Lux_Soap','Maggi_Noodles','Milky_Bikis',
    'Nestle_Milk_Powder','Parachute_Oil','Plastic_Bottle',
    'Pril_Liquid','Tata_Salt','Yardley_Powder'
]

# ---------------- DATA LOADING FUNCTIONS ----------------
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.info("⬇️ Downloading AI model… Please wait")
        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)

    return tf.keras.models.load_model(MODEL_PATH)





@st.cache_data(show_spinner=False)
def load_data():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    else:
        st.error(f"CSV file not found at {CSV_PATH}. Please check your file names.")
        return pd.DataFrame()

# Load instances
model = load_model()
data = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "🛍️ Product Scanner","📘 How to Use","📦 Supported Products","❓ FAQ","📞 Contact","ℹ️ About"]
)

# ---------------- PAGES ----------------
if page == "🏠 Home":
    st.markdown("<h1 style='text-align:center;'>Smart Product Scanner</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=260)
    st.markdown("<p style='text-align:center; font-size:18px; color:#9ca3af;'>AI-powered Identification System</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("👉 Use the sidebar to start scanning products")

elif page == "🛍️ Product Scanner":
    st.title("🛍️ Product Scanner")
    
    if model is None:
        st.error("Model not loaded. Check connection to Google Drive.")
    else:
        uploaded_file = st.file_uploader("📷 Upload product image", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, width=400)

            # -------- PREPROCESS --------
            img = image.resize((IMG_SIZE, IMG_SIZE))
            img_array = np.expand_dims(np.array(img) / 255.0, axis=0)

            # -------- PREDICT --------
            prediction = model.predict(img_array)
            predicted_class = class_names[np.argmax(prediction)]

            st.markdown("---")
            st.write("**Category:**", predicted_class)

            # -------- CSV LOOKUP --------
            # Ensure your CSV column is actually named "class_name"
            result = data[data["class_name"] == predicted_class]

            if result.empty:
                st.warning("⚠️ Product details not found in CSV for this category.")
            else:
                product = result.sample(1).iloc[0]

                st.success("✅ Product Details")
                st.write("🧾 **Product Name:**", product["product_name"])
                st.write("🏷️ **Brand:**", product["brand"])
                st.write("⚖️ **Weight:**", product["weight"])
                st.write("💰 **Price:** ₹", product["price"])
                st.write("📅 **Expiry Date:**", product["expiry"])
            
                

                # -------- VOICE (ONCE) --------
                key = f"{product['product_name']}_{product['expiry']}"
                
                if "last_spoken" not in st.session_state:
                   st.session_state.last_spoken = None

                if st.session_state.last_spoken != key:
                       
                       time.sleep(0.3) 
                       speak_product(product)
                       st.session_state.last_spoken = key

elif page == "📘 How to Use":
    st.title("📘 How to Use")
    st.markdown("""
    Follow these simple steps to use the **Smart Product Scanner**.
    This app helps you identify products and get details instantly.
    """)
    st.markdown("""
    ### 🔍 Step-by-Step Guide

    **Step 1:** Go to **Product Scanner** from the sidebar.  
                
    **Step 2:** Upload a clear image of the product (front view).
                  
    **Step 3:** Wait a few seconds while the AI analyzes the image. 
                 
    **Step 4:** View product details such as **name, brand, weight, price, and expiry date**.  
                
    **Step 5:** 🔊 The app will automatically read out the product details using voice.
    """)
    st.markdown("""
    ### 📷 Image Guidelines

    ✔ Use clear and well-lit images  
    ✔ Product label should be visible  
    ✔ Avoid blurred or dark images  
    ✔ JPG / PNG formats are supported
    """)



elif page == "📦 Supported Products":
    st.title("📦 Supported Products")
    for item in class_names:
        st.write("•", item.replace("_", " "))

elif page == "❓ FAQ":
    st.title("❓ FAQ")
    
    st.markdown("""
    **Q: What does this app do?** 
                 
    Identifies products from images and shows details.

    **Q: What image formats are supported?**  
                
    JPG, JPEG, and PNG.

    **Q: Why is my product not detected?**  
                
    Image may be unclear or product not supported.

    **Q: Does voice work?**  
                
    Yes, voice works automatically on local PC.
    """)


elif page == "📞 Contact":
    st.title("📞 Contact")
    st.markdown("""
    📧 **Email:** smartproductscanner@gmail.com  
    📍 **Location:** India  

    For queries, feedback, or support, please contact us.
    """)

elif page == "ℹ️ About":
    st.title("ℹ️ About")
    st.markdown("""
    **Smart Product Scanner** is an AI-powered application that helps users
    identify products from images and view important details such as
    brand, weight, price, and expiry date.

    The app also provides automatic voice assistance to improve accessibility.
    """)


# (All other ELIF pages remain as you wrote them)
# ... [Rest of your FAQ, Contact, About code] ...

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("© Smart Product Scanner | Deep Learning + Streamlit")