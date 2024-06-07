"""
Read audio files present in the working directory and converts the filenames to be BPO compliant.

All .wav and .mp3 files in the working directory will be copied to a new subdirectory named
'BPO_filenames' and there filenames will be changed to be BPO pipeline compliant.
"""
from typing import Tuple
from pathlib import Path
import re


def reformat_filename(file: Path) -> str | None:
    """Reformats standard birdnetpi filename to BPO filename."""
    match = re.search(
        r'(\d{4}-\d{2}-\d{2})_(\w+)-\d+-\d{4}-\d{2}-\d{2}-birdnet-(\d{2}_\d{2}_\d{2})', file.stem
        )
    if match:
        date_part = match.group(1).replace('-', '')
        species_part = match.group(2)
        time_part = match.group(3).replace('_', '')
        new_filename = f'{date_part}-{time_part}-{species_part}{file.suffix}'
        return new_filename
    return None


def main():
    """Find files and copies them with new filename to subdirectory."""
    source_dir = Path.cwd()
    dest_dir = source_dir / 'BPO_filenames'
    dest_dir.mkdir(exist_ok=True)  # Create the destination directory if it doesn't exist

    extensions: Tuple[str] = ('*.mp3', '*.wav')
    files: list[Path] = []

    # Find files with the specified extensions
    for ext in extensions:
        files.extend(source_dir.glob(ext))

    # Print the type of each file path
    for file in files:
        new_filename = reformat_filename(file)
        if new_filename is None:
            print(f'WARNING: file "{file}" was not recognized and is ignored.')
        else:
            new_file_path = dest_dir / new_filename
            new_file_path.write_bytes(file.read_bytes())
            print(f"Copied and renamed: {file} -> {new_file_path}")


if __name__ == '__main__':
    main()
