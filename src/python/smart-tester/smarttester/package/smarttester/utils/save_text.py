from smarttester import PATH_saved_files


def save_text_in_saved_files_dir(file_name: str, save_dir: str, text: str, ext: str = "txt") -> None:
    """Saves text in saved_files directory."""
    file_path = PATH_saved_files / save_dir / f"{file_name}.{ext}"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)


def load_file_from_saved_files_dir(saved_dir: str, file_name: str, ext: str = "txt") -> str:
    """Saves text in saved_files directory."""
    file_path = PATH_saved_files / saved_dir / f"{file_name}.{ext}"

    if not file_path.exists():
        raise FileNotFoundError(f"Cannot load files from {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        return content

