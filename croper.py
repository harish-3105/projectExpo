import streamlit as st
import cv2
import numpy as np
from PIL import Image
from streamlit_cropper import st_cropper  # Ensure installed via `pip install streamlit-cropper`

st.title("Camera Capture with Cropping & Edge Detection")

# Sidebar for camera toggle
enable = st.sidebar.checkbox("Enable Camera")

# Camera input
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    # Convert image to PIL format
    img = Image.open(picture).convert("RGB")  # Ensure compatibility with st_cropper

    # Image Cropping
    st.subheader("Crop the Image")
    cropped_img = st_cropper(img, box_color="red", aspect_ratio=None)

    if cropped_img:
        # Convert to OpenCV format
        img_array = np.array(cropped_img)

        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # Edge Detection with Adjustable Thresholds
        st.sidebar.subheader("Edge Detection Settings")
        low_threshold = st.sidebar.slider("Low Threshold", 0, 255, 100)
        high_threshold = st.sidebar.slider("High Threshold", 0, 255, 200)

        edges = cv2.Canny(gray, low_threshold, high_threshold)

        # Display results
        st.image(cropped_img, caption="Cropped Image", use_column_width=True)
        st.image(edges, caption="Edge Detected Image", use_column_width=True, clamp=True)

        # Convert edge-detected image to PIL format for download
        edge_pil = Image.fromarray(edges)

        # Provide download button for the processed image
        st.download_button(
            "Download Edge Image",
            data=edge_pil.tobytes(),
            file_name="edge_detected.jpg",
            mime="image/jpeg"
        )
