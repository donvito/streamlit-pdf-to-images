import streamlit as st
import fitz  # PyMuPDF
import os
import zipfile
import io

def pdf_to_images(pdf_file, zoom_x=2.0, zoom_y=2.0, image_format="png"):
    images = []
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        matrix = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=matrix)
        img_bytes = pix.tobytes(image_format)
        images.append((f"page_{page_num + 1}.{image_format}", img_bytes))
    return images

def create_zip(images_dict):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        root_folder = "pdf_to_images_output"  # Root folder name
        for pdf_filename, images in images_dict.items():
            folder_name = os.path.splitext(pdf_filename)[0]  # Get the filename without extension
            for filename, img_bytes in images:
                zip_file.writestr(os.path.join(root_folder, folder_name, filename), img_bytes)  # Create folder in zip
    return zip_buffer.getvalue()

st.title("PDF to Images Converter")

uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    image_format = st.radio("Select image format", ["png", "jpeg"])  # User selects image format using radio buttons
    zoom_x = 2.0
    zoom_y = 2.0

    if st.button("Convert to Images"):
        images_dict = {}
        for uploaded_file in uploaded_files:
            with st.spinner(f"Converting {uploaded_file.name} to images..."):
                images = pdf_to_images(uploaded_file, zoom_x, zoom_y, image_format)  # Pass selected format
                images_dict[uploaded_file.name] = images  # Store images by PDF filename

        zip_file = create_zip(images_dict)  # Pass the dictionary of images

        st.success(f"Converted {sum(len(images) for images in images_dict.values())} pages to images!")
        st.download_button(
            label="Download ZIP file",
            data=zip_file,
            file_name="pdf_to_images_output.zip",  # Updated ZIP file name
            mime="application/zip"
        )

st.markdown("---")
st.text("Created by DonvitoCodes")
st.markdown("[Visit my website](https://donvitocodes.com) | [Buy me a coffee](https://buymeacoffee.com/donvitocodes)") 
