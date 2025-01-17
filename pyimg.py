import io
import shutil
import subprocess

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
    if isinstance(image, Image.Image):
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        show_im_buffer(buffer.read())
        return
    elif isinstance(image, str):
        show_im_path(image)
        return
    raise NotImplementedError("Image format not supported.")


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
