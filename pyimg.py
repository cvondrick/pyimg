import io
import shutil
import subprocess

import numpy as np
import torch
from PIL import Image


def show_im_buffer(image_buffer):
    kitten_path = shutil.which("kitten")
    if kitten_path is None:
        raise FileNotFoundError("kitten not found in PATH.")
    process = subprocess.Popen(
        [kitten_path, "icat", "--align", "left", "--scale-up"],
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    process.communicate(input=image_buffer)


def show_im_path(image_path):
    subprocess.run(["kitten", "icat", image_path])


def show_im(image):
    # PIL Image
    if isinstance(image, Image.Image):
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        show_im_buffer(buf.read())
        return

    # File path
    if isinstance(image, str):
        show_im_path(image)
        return

    # NumPy array
    if isinstance(image, np.ndarray):
        arr = image
        # if floats in [0,1], scale to [0,255]
        if np.issubdtype(arr.dtype, np.floating):
            arr = (arr * 255).clip(0, 255).astype(np.uint8)
        im = Image.fromarray(arr)
        return show_im(im)

    # Torch tensor
    if isinstance(image, torch.Tensor):
        t = image.detach().cpu()
        arr = t.numpy()
        # handle (C, H, W) → (H, W, C)
        if arr.ndim == 3 and arr.shape[0] in (1, 3):
            arr = np.transpose(arr, (1, 2, 0))
        # same float scaling
        if np.issubdtype(arr.dtype, np.floating):
            arr = (arr * 255).clip(0, 255).astype(np.uint8)
        im = Image.fromarray(arr)
        return show_im(im)

    raise NotImplementedError(f"Unsupported image type: {type(image)}")


def show_plot(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    show_im_buffer(buffer.read())


if __name__ == "__main__":
    image = Image.new("RGB", (200, 200), (255, 0, 0))
    show_im(image)

    import matplotlib.pyplot as plt

    plt.plot([1, 2, 3], [4, 1, 3])
    show_plot(plt.gcf())
