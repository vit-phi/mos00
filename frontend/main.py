import streamlit as st
import requests
from PIL import Image

# Define styles for transfer
STYLES = {
    "Candy": "candy",
    "Composition 6": "composition_vii",
    "Feathers": "feathers",
    "La Muse": "la_muse",
    "Mosaic": "mosaic",
    "Starry Night": "starry_night",
    "The Scream": "the_scream",
    "The Wave": "the_wave",
    "Udnie": "udnie",
}

# Page configuration
st.set_page_config(page_title="Style Transfer App", layout="wide", initial_sidebar_state="expanded")

# Apply custom theme
theme_css = """
<style>
    /* Main body style */
    body {
        background: linear-gradient(135deg, #ff6f61, #d16d85);
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
        color: #ffffff;
    }

    /* Title and headers */
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        color: white;
        text-align: center;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
    }

    h1 {
        font-size: 50px;
        font-weight: 600;
    }

    h2 {
        font-size: 32px;
        font-weight: 500;
    }

    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #1c1f26, #34495e);
        color: white;
        padding-top: 50px;
        font-size: 18px;
    }

    .sidebar .sidebar-header {
        background: #e74c3c;
        color: white;
        padding: 20px;
        font-size: 24px;
        text-align: center;
        font-weight: bold;
    }

    .sidebar .sidebar-nav {
        margin-top: 50px;
    }

    .sidebar .sidebar-nav a {
        display: block;
        padding: 15px;
        margin-bottom: 10px;
        color: white;
        text-decoration: none;
        background: #34495e;
        border-radius: 10px;
        font-size: 20px;
        text-align: center;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }

    .sidebar .sidebar-nav a:hover {
        background: #e74c3c;
        transform: scale(1.05);
    }

    /* File uploader styling */
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 25px;
        border: 3px dashed #e74c3c;
        margin-bottom: 30px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
        text-align: center;
    }

    .stFileUploader p {
        color: #f39c12;
        font-size: 18px;
    }

    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #e74c3c, #f39c12);
        color: white;
        padding: 18px 36px;
        border-radius: 50px;
        font-size: 20px;
        border: none;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s;
    }

    .stButton>button:hover {
        transform: scale(1.1);
        background: linear-gradient(45deg, #ff6347, #ffbb33);
    }

    /* Scrollable container for images */
    .scrollable-image-container {
        display: flex;
        overflow-x: auto;
        gap: 20px;
        padding: 15px;
        justify-content: center;
    }

    .scrollable-image-container img {
        width: 320px;
        height: auto;
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }

    /* Footer styling */
    footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1c1f26;
        color: white;
        text-align: center;
        padding: 20px;
        font-size: 16px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
    }

    footer a {
        color: #e74c3c;
        text-decoration: none;
        font-weight: bold;
    }

    footer a:hover {
        color: #f39c12;
    }
</style>
"""
st.markdown(theme_css, unsafe_allow_html=True)

# Function to show the home page
def show_home():
    st.title("🎨 แอปโอนถ่ายสไตล์ศิลปะ")
    st.write("แอปพลิเคชันนี้ช่วยให้คุณสามารถเปลี่ยนสไตล์ของรูปภาพด้วยการใช้เทคโนโลยี AI ได้อย่างง่ายดาย!")

    # File uploader
    st.subheader("1. อัปโหลดรูปภาพของคุณ")
    image = st.file_uploader("เลือกรูปภาพที่คุณต้องการแปลง", type=["jpg", "png", "jpeg"])

    # Sidebar for style selection
    st.sidebar.subheader("เลือกสไตล์")
    style = st.sidebar.selectbox("เลือกสไตล์ที่คุณชอบ", list(STYLES.keys()))

    # Button for style transfer
    st.subheader("2. เลือกสไตล์และแปลงรูปภาพ")
    if st.button("เริ่มแปลงรูปภาพ"):
        if image and style:
            with st.spinner('กำลังประมวลผล...'):
                files = {"file": image.getvalue()}
                try:
                    res = requests.post(f"http://backend:8080/{STYLES[style]}", files=files)
                    img_path = res.json()
                    output_image = Image.open(img_path.get("name"))
                    
                    # Display images in a scrollable container
                    st.markdown("<div class='scrollable-image-container'>", unsafe_allow_html=True)
                    st.image(output_image, caption=f"ภาพที่แปลงเป็นสไตล์: {style}", use_column_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {e}")
        else:
            st.warning("กรุณาอัปโหลดรูปภาพและเลือกสไตล์ก่อนค่ะ")

# Function to show the about page
def show_about():
    st.title("เกี่ยวกับเรา")
    st.write("นี่คือตัวอย่างแอปโอนถ่ายสไตล์ศิลปะที่สร้างโดย Vitsanu Phimanram")
    st.write("แอปนี้ใช้เทคโนโลยี AI เพื่อทำการแปลงสไตล์ของรูปภาพต่างๆ ตามที่เลือกไว้ เช่น สไตล์ของศิลปินชื่อดังหรือสไตล์ที่เป็นเอกลักษณ์ของศิลปะบางประเภท")

# Function to show the contact page
def show_contact():
    st.title("ติดต่อเรา")
    st.write("สามารถติดต่อเราได้ที่: contact@yourdomain.com")
    st.write("หรือเข้าเยี่ยมชมเว็บไซต์ที่: [www.yourwebsite.com](http://www.yourwebsite.com)")

# Sidebar navigation
st.sidebar.title("เมนู")
page = st.sidebar.radio("เลือกหน้า", ["หน้าแรก", "เกี่ยวกับ", "ติดต่อเรา"])

# Show the selected page
if page == "หน้าแรก":
    show_home()
elif page == "เกี่ยวกับ":
    show_about()
elif page == "ติดต่อเรา":
    show_contact()

# Fixed footer
st.markdown("""
<footer>
    พัฒนาโดย Vitsanu Phimanram © 2025 | <a href="https://github.com/vit-phi">github</a>
</footer>
""", unsafe_allow_html=True)
