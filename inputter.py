import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Camera Capture with Edge Detection")

# Sidebar for controls
enable = st.sidebar.checkbox("Enable Camera")

# Camera input
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    # Convert image to OpenCV format
    img = Image.open(picture)
    img_array = np.array(img)

    # Convert to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    # Apply Canny Edge Detection
    edges = cv2.Canny(gray, 100, 200)

    # Display original and edge-detected images
    st.image(img, caption="Original Image", use_column_width=True)
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
