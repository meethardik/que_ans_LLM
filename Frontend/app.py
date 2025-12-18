import sys
import streamlit as slt
from pathlib import Path
import os
import time

sys.path.append("Services")
from Services.ProcessDocument import ProcessDocument

upload_dir = Path("Uploads")

def setup_page() ->None:
    slt.set_page_config(
     page_title="Multiple File Uploader", page_icon="📤", layout="centered")
    slt.title("📤 Upload Your Multiple Files")

def ensure_upload_directory() ->None:
    upload_dir.mkdir(parents=True, exist_ok=True)
    
def file_uploader_ui():
    return slt.file_uploader(
        "Upload PDF file(s) only", type="pdf", accept_multiple_files=True)

def save_uploaded_files(uploaded_files) -> None:
    total = len(uploaded_files)
    progress = slt.progress(0)
    status = slt.empty()

    for i, f in enumerate(uploaded_files, start=1):
        status.write(f"Saving **{f.name}** ({i}/{total})...")
        (upload_dir / f.name).write_bytes(f.getbuffer())

        # Call the process function from ProcessDocument.py
        process_document = ProcessDocument()
        process_document.process()

        progress.progress(int(i / total * 100))
        time.sleep(0.05)  # optional: makes progress visible even for tiny files
        status.success(f"✅ Processing of {total} file(s) successfully!")
        del process_document

def main():
    setup_page()
    ensure_upload_directory()

    uploaded_files = file_uploader_ui()

    if uploaded_files:
        slt.success(f"{len(uploaded_files)} PDF(s) selected!")

        invalid = [
            f.name for f in uploaded_files if not f.name.lower().endswith(".pdf")
        ]
        if invalid:
            slt.error(f"These files are not PDFs: {', '.join(invalid)}")
        else:
            if slt.button("Click to Save Files"):
                save_uploaded_files(uploaded_files)

if __name__ == "__main__":
    main()

