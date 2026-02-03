from pypdf import PdfReader


def extract_text_from_file(uploaded_file) -> str:
    """
    Extracts text from uploaded PDF or TXT file.
    """

    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    else:
        raise ValueError("Unsupported file type")
