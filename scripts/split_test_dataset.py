import os
import random
from pathlib import Path

ixi_path = Path("datasets/IXI-norm")
ixi_test_path = Path("datasets/IXI-test")

ixi_test_path.mkdir(exist_ok=False)
files = list(ixi_path.iterdir())

for _ in range(100):
    file = random.choice(files)
    if file.suffix != ".npy":
        raise ValueError(f"{file} is not .npy file. transform it first")
    os.system(f"mv {file} {ixi_test_path/file.name}")
    files.remove(file)
