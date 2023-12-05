# extract dataset from IXI-T1.tar
import os
from pathlib import Path

ixi_path = Path("datasets/IXI")

if ixi_path.exists() and next(iter(ixi_path.iterdir()), False):
    raise RuntimeError("dir already exist")

os.system(f"mkdir -p {ixi_path} && tar xf IXI-T1.tar -C {ixi_path}")


for file in ixi_path.iterdir():
    if file.suffix != ".gz":
        raise RuntimeError("invalid dataset")
    os.system(f"gzip -d {file}")
    os.system(f"rm -rf {file}")
