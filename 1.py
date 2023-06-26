import streamlit as st
from io import BytesIO
from streamlit_cropper import st_cropper
from streamlit.components.v1 import html
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw


# <================================== For the main header ================================================================>

header_html = """
    <div style="background-color: #242424; padding: 20px; text-align: center;">
        <h1 style="font-size: 48px; font-weight: bold;">
            <span style="background: linear-gradient(to right, #00e5ff, #ff00e1); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                ImageWizard
            </span>
        </h1>
    </div>
"""

html(header_html)

def apply_filters(image, brightness, contrast, sharpness, saturation, color_temperature, exposure, shadows, blur_radius, highlight):

    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.0 + brightness)
    
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)
    
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpness)
    
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(saturation)
    
    if color_temperature != 0:
        matrix = (1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, color_temperature, 0.0, 0.0)
        image = image.convert("RGB", matrix)
    
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.0 + exposure)
    
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(shadows)
    
    if blur_radius > 0:
        image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(highlight)    
    return image
    
st.sidebar.markdown("<p style='color:green;font-weight:bold;'>This app has been developed by Arya Chakraborty</p>", unsafe_allow_html=True)

uploaded_file = st.sidebar.file_uploader("Upload an image of your choice", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    brightness = st.sidebar.slider("Brightness", -1.0, 1.0, 0.0, step=0.01)
    contrast = st.sidebar.slider("Contrast", 0.0, 2.0, 1.0, step=0.01)
    sharpness = st.sidebar.slider("Sharpness", -2.0, 2.0, 0.0, step=0.01)
    saturation = st.sidebar.slider("Saturation", 0.0, 2.0, 1.0, step=0.01)
    color_temperature = st.sidebar.slider("Col>or Temperature", -100.0, 100.0, 0.0, step=0.00001)
    exposure = st.sidebar.slider("Exposure", -1.0, 1.0, 0.0, step=0.01)
    shadows = st.sidebar.slider("Shadows", 0.0, 2.0, 1.0, step=0.01)
    blur_radius = st.sidebar.slider("Blur Radius", 0, 20, 0)
    highlight = st.sidebar.slider("Highlight", 0.0, 2.0, 1.0, step=0.01)
    
    # Apply filters to the image
    filtered_image = apply_filters(image, brightness, contrast, sharpness, saturation, color_temperature, exposure, shadows, blur_radius, highlight)
    if filtered_image.mode != "RGB":
        filtered_image = filtered_image.convert("RGB")
    byte_stream = BytesIO()
    filtered_image.save(byte_stream, format="JPEG")
    byte_stream.seek(0)
    col1, col2 = st.columns(2)
    with col1:
            st.image(image, caption="Original Image", use_column_width=True)

    if st.sidebar.button("Show Processed Image"):    
        with col2:
            st.image(filtered_image, caption="Processed Image", use_column_width=True)

    st.sidebar.download_button(
    label="Download The Editted Photo",
    data=byte_stream,
    file_name="filtered_image.jpg",
    )
    st.sidebar.success("Click the button above to download the processed image.")