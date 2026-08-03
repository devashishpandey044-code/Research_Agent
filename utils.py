from pathlib import Path

UPLOAD_FOLDER = Path(__file__).resolve().parent / "uploads"


def save_uploaded_files(uploaded_files):

    UPLOAD_FOLDER.mkdir(exist_ok=True)

    for file in uploaded_files:

        save_path = UPLOAD_FOLDER / file.name

        with open(save_path, "wb") as f:
            f.write(file.getbuffer())