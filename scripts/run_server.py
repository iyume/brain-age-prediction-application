import base64
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import Dict

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:1420",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


files: Dict[str, bytes] = {}


def load_nii(filename: str) -> np.ndarray:
    data = nib.load(tmpfile.name).get_fdata()  # type: ignore
    data = np.array(data, dtype=np.float32)
    return data


@app.post("/get_thumbnail")
async def _(file: UploadFile):
    # create tmp file because nibabel not support file-like
    tmpfile = NamedTemporaryFile(delete=False, suffix=".nii")
    tmpfile.write(file.file.read())
    data = load_nii(tmpfile.name)
    tmpfile.close()
    del tmpfile
    img = np.rot90(data[:, :, data.shape[2] // 2])
    plt.imshow(img, cmap="gray", aspect="equal")
    plt.axis("off")
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0, transparent=True)
    return {"thumbnail": base64.b64encode(buf.getvalue())}


@app.post("/evaluate")
async def _(file: UploadFile):
    ...


if __name__ == "__main__":
    uvicorn.run(app)
