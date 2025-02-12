import streamlit as st
import cv2
import numpy as np
import os
import time
from PIL import Image
import socket
UPLOAD_FOLDER = "uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists

def get_local_ip():
    """Get the local IP address of the PC to access from mobile."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def process_image(image):
    """Convert the image to a scanner-like format (grayscale & threshold)."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return processed

def get_latest_uploaded_image():
    """Check the upload folder for the latest image."""
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith((".jpg", ".jpeg", ".png"))]
    if files:
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(UPLOAD_FOLDER, x)))
        return os.path.join(UPLOAD_FOLDER, latest_file)
    return None

def main():
    # Display IP for mobile connection
    local_ip = get_local_ip()
    st.title("📱 Live Mobile Scanner on PC")
    st.write(f"📡 Upload from mobile: **http://{local_ip}:8501**")

    # File uploader for real-time mobile uploads
    uploaded_file = st.file_uploader("Upload an image from mobile", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ Image uploaded successfully! Refreshing on PC...")

    # Wait for a new image and update
    while True:
        latest_image_path = get_latest_uploaded_image()
        if latest_image_path:
            image = Image.open(latest_image_path).convert("RGB")
            image_np = np.array(image)

            # Process the image
            processed_image = process_image(image_np)

            # Show images
            st.write("### 🔍 Image Preview & Processed Output")
            col1, col2 = st.columns(2)

            with col1:
                st.image(image, caption="📷 Original Image", use_column_width=True)

            with col2:
                st.image(processed_image, caption="📝 Processed (Scanned) Image", use_column_width=True, channels="GRAY")

            # Download options
            processed_pil = Image.fromarray(processed_image)

            st.write("### 📥 Download Processed Image:")
            st.download_button("Download PNG", processed_pil.tobytes(), file_name="scanned_image.png", mime="image/png")

            break  # Stop checking once an image is found

        time.sleep(1)  # Check for new images every 1 second

if __name__ == "__main__":
    main()
