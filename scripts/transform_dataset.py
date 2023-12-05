"""Cache the IXI dataset because transform cause too many time.

See: IXIDataset.transform
"""

import operator
import pickle
from pathlib import Path

import nibabel as nib
import numpy as np
import scipy.ndimage as nd

ixi_path = Path("datasets/IXI")
new_ixi_path = Path("datasets/IXI-norm")

if not ixi_path.exists():
    raise

if new_ixi_path.exists():
    raise

new_ixi_path.mkdir(parents=True)

new_shape = (256, 256, 128)

for file in ixi_path.iterdir():
    data: np.memmap = nib.load(file).get_fdata()  # type: ignore
    img = np.array(data, dtype=np.float32)
    real_resize_factor = tuple(map(operator.truediv, new_shape, img.shape))
    img = nd.zoom(img, real_resize_factor, order=3)
    new_file = new_ixi_path / (file.name + ".npy")
    # pickle.dump(img, open(new_file, "wb"))
    np.save(open(new_file, "wb"), img)
    print(f"saved to {new_file} {img.dtype}")
