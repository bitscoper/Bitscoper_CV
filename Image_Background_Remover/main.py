# By Abdullah As-Sadeed

from PIL import Image
from pathlib import Path
from rembg import remove
import os
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from Common import *

if __name__ == "__main__":
    input_path = select_directory_or_file("File")

    input = Image.open(input_path)
    output = remove(input)

    output.show()

    output_path = select_directory_or_file("Directory")

    _, extension = os.path.splitext(input_path)
    output_path = os.path.join(output_path, "output" + extension)

    output = output.convert("RGB")
    output.save(output_path)

sys.exit(0)
