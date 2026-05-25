import streamlit as st
from utils.api import upload_pdfs


def render_uploader():
    st.sidebar.header("Upload PDFs")

    uploaded_files = st.sidebar.file_uploader(
        "Upload multiple PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if st.sidebar.button("Upload to DB") and uploaded_files:
        response = upload_pdfs(uploaded_files)

        # response is dict → NOT status_code
        if response.get("status") == "success":
            st.sidebar.success("Uploaded successfully")
        else:
            st.sidebar.error(f"Error: {response}")