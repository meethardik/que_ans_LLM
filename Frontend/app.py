import sys
import streamlit as slt
from pathlib import Path
from typing import List
import time

sys.path.append("Services")
from Services.ProcessDocument import ProcessDocument
from Services.ProcessSearchResults import ProcessSearchResults

upload_dir = Path("Uploads")

def setup_page() ->None:
    slt.set_page_config(
     page_title="Multiple File Uploader", page_icon="📤", layout="wide")
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

def text_input_with_button() -> str:
    # Text box + button on the side
    c1, c2 = slt.columns([4, 1])
    with c1:
        user_text = slt.text_input("Enter a value", placeholder="Type something (e.g., What skills are needed...)")
    with c2:
        clicked = slt.button("Submit", use_container_width=True)
    if clicked:
        slt.session_state["last_submitted"] = user_text
        process_query = ProcessSearchResults(query=user_text, top_k=3)
        
        slt.text_area("output_text", value=str(process_query.process_query_results()))

    return slt.session_state.get("last_submitted", "")

def auto_expanding_text_area() -> str:
    
    if "output_text" not in slt.session_state:
        slt.session_state["output_text"] = ""

    text = slt.session_state["output_text"]
    # Rough dynamic height: 22px per line, min 120px, max 600px
    line_count = max(6, min(30, text.count("\n") + 1))
    dynamic_height = line_count * 22

    slt.session_state["output_text"] = slt.text_area(
        "Output (auto-expands as content grows)",
        value=text,
        height=dynamic_height
    )
    return slt.session_state["output_text"]

def main():
    setup_page()
    ensure_upload_directory()

    uploaded_files = file_uploader_ui()

    # Save uploaded files button + progress
    if uploaded_files:
        if slt.button("Save uploaded files", type="primary"):
            save_uploaded_files(uploaded_files)
    else:
        slt.caption("Upload files to enable saving.")

    col_a, col_b = slt.columns([1, 1], vertical_alignment="top")

    with col_a:
        slt.subheader("Text box + button (side-by-side)")
        submitted_value = text_input_with_button()

        # Demo action: append submitted text into output area
        if submitted_value:
            slt.info(f"Last submitted: **{submitted_value}**")
            if slt.button("Append submitted text to Output"):
                slt.session_state["output_text"] = (slt.session_state.get("output_text", "") + submitted_value + "\n")

        

    with col_b:
        slt.subheader("Plain text area (auto-expanding)")
        auto_expanding_text_area()

        # Demo helper buttons
        c1, c2, c3 = slt.columns(3)
        with c1:
            if slt.button("Add sample log"):
                slt.session_state["output_text"] = slt.session_state.get("output_text", "") + "Sample log line...\n"
        with c2:
            if slt.button("Clear output"):
                slt.session_state["output_text"] = ""
        with c3:
            if slt.button("Load file names"):
                if uploaded_files:
                    names = "\n".join([f.name for f in uploaded_files])
                    slt.session_state["output_text"] = slt.session_state.get("output_text", "") + f"Uploaded files:\n{names}\n"
                else:
                    slt.session_state["output_text"] = slt.session_state.get("output_text", "") + "No files uploaded.\n"

    # if uploaded_files:
    #     slt.success(f"{len(uploaded_files)} PDF(s) selected!")

    #     invalid = [
    #         f.name for f in uploaded_files if not f.name.lower().endswith(".pdf")
    #     ]
    #     if invalid:
    #         slt.error(f"These files are not PDFs: {', '.join(invalid)}")
    #     else:
    #         if slt.button("Click to Save Files"):
    #             save_uploaded_files(uploaded_files)

if __name__ == "__main__":
    main()

