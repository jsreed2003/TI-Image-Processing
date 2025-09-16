# === FastAPI + IQA Backend Starter ===
# Run with:     source .venv/bin/activate
#               pip install uvicorn

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from io import BytesIO
from PIL import Image
import numpy as np
import skimage.metrics as metrics
import tempfile
import os

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Utilities ===
def image_to_array(upload: UploadFile) -> np.ndarray:
    image = Image.open(BytesIO(upload.file.read())).convert("RGB")
    return np.array(image)

# === API Endpoints ===
@app.post("/iq-metrics/")
def compute_metrics(
    distorted: UploadFile = File(...),
    reference: Optional[UploadFile] = File(None)
):
    distorted_arr = image_to_array(distorted)

    if reference:
        reference_arr = image_to_array(reference)

        ssim = metrics.structural_similarity(distorted_arr, reference_arr, channel_axis=-1)
        psnr = metrics.peak_signal_noise_ratio(reference_arr, distorted_arr)
        return {"ssim": ssim, "psnr": psnr, "mode": "full-reference"}

    # No-reference mode (just dummy output for now)
    # Replace with real BRISQUE/NIQE later
    sharpness = np.var(distorted_arr)
    return {"sharpness": sharpness, "mode": "no-reference"}

@app.post("/compress/")
def compress_image(
    image: UploadFile = File(...),
    quality: int = Form(75)
):
    img = Image.open(BytesIO(image.file.read())).convert("RGB")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        img.save(tmp.name, format="JPEG", quality=quality)
        size = os.path.getsize(tmp.name)
        with open(tmp.name, "rb") as f:
            content = f.read()
        os.unlink(tmp.name)

    return {"compressed_size": size, "bytes": content.hex()[:100]}  # hex preview only
