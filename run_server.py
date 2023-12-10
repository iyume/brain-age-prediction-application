import base64
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import Dict
from uuid import uuid4

import matplotlib.pyplot as plt
import nibabel as nib
import numpy as np
import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from brain_age_prediction.evaluate import Evaluator

app = FastAPI()

origins = [
    "http://localhost:1420",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

evaluator = Evaluator(device="cuda", pth_file="ckpt/model_v1_epoch100.pth")


temp_inputs: Dict[str, np.ndarray] = {}


def load_nii_fp32(filename: str) -> np.ndarray:
    data = nib.load(filename).get_fdata()  # type: ignore
    data = np.array(data, dtype=np.float32)
    return data


@app.post("/get_thumbnail")
async def _(file: UploadFile):
    # create tmp file because nibabel not support file-like
    tmpfile = NamedTemporaryFile(delete=False, suffix=".nii")
    tmpfile.write(file.file.read())
    data = load_nii_fp32(tmpfile.name)
    tmpfile.close()
    del tmpfile

    fileuid = str(uuid4())
    temp_inputs[fileuid] = data.copy()

    img = np.rot90(data[:, :, data.shape[2] // 2])
    plt.imshow(img, cmap="gray", aspect="equal")
    plt.axis("off")
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0, transparent=True)

    return {
        "thumbnail": base64.b64encode(buf.getvalue()),
        "file_id": fileuid,
    }


class EvaluateReq(BaseModel):
    file_id: str


@app.post("/evaluate")
async def _(reqdata: EvaluateReq):
    if reqdata.file_id not in temp_inputs:
        return JSONResponse("upload first", status_code=400)
    inputs = temp_inputs[reqdata.file_id]
    out = evaluator.evaluate_ndarray(inputs)
    return {"result": out[0]}


@app.get("/ping")
async def _():
    return "pong"


if __name__ == "__main__":
    uvicorn.run(app)
