from smarttester import PATH_saved_files


def save_text_in_saved_files_dir(file_name: str, save_dir: str, text: str, ext: str = "txt") -> None:
    """Saves text in saved_files directory."""
    file_path = PATH_saved_files / save_dir / f"{file_name}.{ext}"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
