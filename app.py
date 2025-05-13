# app.py
import streamlit as st
from qr_utils import generate_qr_with_logo
import uuid
import os
from PIL import Image

st.set_page_config(page_title="Gerador de QR Code Lema v1.0", layout="centered")
st.title("🔗 Gerador de QR Code Lema v1.0")

# Entrada do conteúdo
content = st.text_input("Digite o conteúdo do QR Code (URL, texto, etc):")

# Customização de cor e tamanho
color = st.color_picker("Escolha a cor do QR:", "#000000")
box_size = st.slider("Tamanho do QR:", 5, 20, 10)

# Upload de logo
logo_file = st.file_uploader("(Opcional) Envie o logotipo para o centro do QR", type=["png", "jpg", "jpeg"])

if st.button("Gerar QR Code") and content:
    qr_id = str(uuid.uuid4())[:8]
    qr_path = f"qrcodes/{qr_id}.png"
    qr_svg_path = f"qrcodes/{qr_id}.svg"
    os.makedirs("qrcodes", exist_ok=True)
    if logo_file:
        logo_path = f"logo/{qr_id}_logo.png"
        os.makedirs("logo", exist_ok=True)
        with open(logo_path, "wb") as f:
            f.write(logo_file.getbuffer())
    else:
        logo_path = None

    generate_qr_with_logo(content, qr_path, color=color, box_size=box_size, logo_path=logo_path)

    st.success("QR Code gerado com sucesso!")
    st.image(qr_path, caption="Seu QR Code")
    with open(qr_path, "rb") as file:
        st.download_button("📥 Baixar PNG", file.read(), file_name=f"qr_{qr_id}.png")

    # Geração adicional como SVG sem logo
    import qrcode
    import qrcode.image.svg
    factory = qrcode.image.svg.SvgImage
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=box_size, border=4)
    qr.add_data(content)
    qr.make(fit=True)
    img_svg = qr.make_image(image_factory=factory)
    img_svg.save(qr_svg_path)
    with open(qr_svg_path, "rb") as file_svg:
        st.download_button("📥 Baixar SVG", file_svg.read(), file_name=f"qr_{qr_id}.svg")
