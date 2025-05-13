import qrcode
from PIL import Image

def generate_qr_with_logo(data, path, color="#000000", box_size=10, logo_path=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color=color, back_color="white").convert("RGB")

    if logo_path:
        logo = Image.open(logo_path)
        box = (img_qr.size[0] // 4, img_qr.size[1] // 4)
        logo = logo.resize(box, Image.ANTIALIAS)
        pos = ((img_qr.size[0] - logo.size[0]) // 2, (img_qr.size[1] - logo.size[1]) // 2)
        img_qr.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)

    img_qr.save(path)
