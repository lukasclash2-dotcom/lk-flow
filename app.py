import streamlit as st
import base64
import os

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="LK FLOW",
    layout="wide"
)

# ==================================================
# SESSION
# ==================================================

if "modo" not in st.session_state:
    st.session_state.modo = None

# ==================================================
# IMAGEM
# ==================================================

def get_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

caminho_completo = os.path.join(os.path.dirname(__file__), "assets", "fundo.jpg")
img = get_base64(caminho_completo)

# ==================================================
# CSS
# ==================================================

st.markdown(f"""
<style>

.stApp {{
    background-image: url("data:image/jpg;base64,{img}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

.block-container {{
    max-width: 900px;
    padding-top: 2rem;
}}

html, body, [class*="css"] {{
    color: white;
    font-family: Arial;
}}

.stButton > button {{
    width: 100%;
    height: 75px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(15,15,15,0.72);
    color: white;
    font-size: 24px;
    font-weight: 600;
    transition: 0.3s;
    backdrop-filter: blur(10px);
}}

.stButton > button:hover {{
    border: 1px solid rgba(0,255,255,0.35);
    box-shadow: 0px 0px 20px rgba(0,255,255,0.15);
}}

.stNumberInput input {{
    background: rgba(20,20,20,0.7);
    color: white;
    border-radius: 15px;
}}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HERO (CORRIGIDO: Sem quebras de linha nas tags)
# ==================================================

st.markdown(f"""
<div style="position: relative; border-radius: 30px; overflow: hidden; background: rgba(0,0,0,0.85); border: 1px solid rgba(255,255,255,0.08);">

    <img src="data:image/jpg;base64,{img}" style="width:100%; height:650px; object-fit:cover; opacity:0.28;">

    <div style="position:absolute; top:0; left:0; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">

        <h4 style="color:#bdbdbd; letter-spacing:10px; font-weight:300; margin-bottom:15px;">abertura</h4>

        <h1 style="font-size:120px; font-weight:900; color:white; letter-spacing:10px; margin-top:-10px;">LK FLOW</h1>

        <p style="color:#9ca3af; font-size:18px; margin-top:-10px;">Institutional opening flow</p>

    </div>

</div>
""", unsafe_allow_html=True)

# ==================================================
# MENU
# ==================================================

if st.session_state.modo is None:

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background: rgba(15,15,15,0.72); border-radius: 30px; padding: 40px; border: 1px solid rgba(255,255,255,0.08); backdrop-filter: blur(15px);">

    <p style="color:#8b8b8b; letter-spacing:4px; font-size:13px;">ENTRADA MANUAL</p>

    <h1 style="color:white; font-size:48px;">Há notícia 3⭐ no Brasil às 09h hoje?</h1>

    <p style="color:#8b8b8b; font-size:18px;">Isso define se o cálculo usa: (-VIX + FEF + CL) ou ADRs.</p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Não"):
            st.session_state.modo = "macro"
            st.rerun()

    with c2:
        if st.button("Sim"):
            st.session_state.modo = "adr"
            st.rerun()

# ==================================================
# MACRO
# ==================================================

elif st.session_state.modo == "macro":

    st.markdown("""
    <div style="background: rgba(15,15,15,0.72); border-radius: 30px; padding: 40px; border: 1px solid rgba(255,255,255,0.08);">
        <h1 style="color:white; font-size:42px;">Insira as variações do macro</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        vix = st.number_input("VIX", value=0.0)

    with c2:
        fef = st.number_input("FEF", value=0.0)

    with c3:
        cl = st.number_input("CL", value=0.0)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Gerar leitura"):

        resultado = (-vix) + fef + cl

        forca = min(abs(resultado) * 20, 100)

        if resultado >= 4.5:
            classificacao = "COMPRA FORTE"
            fluxo = "FLUXO COMPRADOR"
            vies = "VIÉS COMPRADOR"
        elif resultado >= 2.5:
            classificacao = "COMPRA MODERADA"
            fluxo = "FLUXO COMPRADOR"
            vies = "VIÉS COMPRADOR"
        elif resultado >= 1.5:
            classificacao = "COMPRA LEVE"
            fluxo = "FLUXO COMPRADOR"
            vies = "VIÉS COMPRADOR"
        elif resultado <= -4.5:
            classificacao = "VENDA FORTE"
            fluxo = "FLUXO VENDEDOR"
            vies = "VIÉS VENDEDOR"
        elif resultado <= -2.5:
            classificacao = "VENDA MODERADA"
            fluxo = "FLUXO VENDEDOR"
            vies = "VIÉS VENDEDOR"
        elif resultado <= -1.5:
            classificacao = "VENDA LEVE"
            fluxo = "FLUXO VENDEDOR"
            vies = "VIÉS VENDEDOR"
        else:
            classificacao = "LATERAL"
            fluxo = "FLUXO INDEFINIDO"
            vies = "MERCADO LATERAL"

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: rgba(10,10,10,0.82); border-radius: 30px; padding: 50px; text-align:center; border:1px solid rgba(255,255,255,0.08);">
            <h3 style="color:#9ca3af; letter-spacing:5px;">RESULTADO</h3>
            <h1 style="color:white; font-size:90px;">{round(resultado,2)}</h1>
            <h2 style="color:#00d5ff;">{vies}</h2>
            <h3 style="color:white;">{classificacao}</h3>
            <h4 style="color:#9ca3af;">FORÇA: {round(forca)}%</h4>
            <h4 style="color:#9ca3af;">{fluxo}</h4>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("← Voltar"):
        st.session_state.modo = None
        st.rerun()

# ==================================================
# ADR
# ==================================================

elif st.session_state.modo == "adr":

    st.markdown("""
    <div style="background: rgba(15,15,15,0.72); border-radius: 30px; padding: 40px; border: 1px solid rgba(255,255,255,0.08);">
        <h1 style="color:white; font-size:42px;">Insira as variações das ADRs</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        vale = st.number_input("VALE", value=0.0)
        itub = st.number_input("ITUB", value=0.0)
        bbd = st.number_input("BBD", value=0.0)

    with c2:
        pbr = st.number_input("PBR", value=0.0)
        bdory = st.number_input("BDORY", value=0.0)
        bolsy = st.number_input("BOLSY", value=0.0)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Gerar leitura"):

        resultado = vale + pbr + itub + bdory + bbd + bolsy

        forca = min(abs(resultado) * 20, 100)

        if resultado >= 4.5:
            classificacao = "COMPRA FORTE"
            fluxo = "FLUXO COMPRADOR"
            vies = "VIÉS COMPRADOR"
        elif resultado >= 2.5:
            classificacao = "COMPRA MODERADA"
            fluxo = "FLUXO COMPRADOR"
            vies = "VIÉS COMPRADOR"
        elif resultado >= 1.5:
            classificacao = "COMPRA LEVE"
            fluxo = "FLUXO COMPRADOR"
            vies = "VIÉS COMPRADOR"
        elif resultado <= -4.5:
            classificacao = "VENDA FORTE"
            fluxo = "FLUXO VENDEDOR"
            vies = "VIÉS VENDEDOR"
        elif resultado <= -2.5:
            classificacao = "VENDA MODERADA"
            fluxo = "FLUXO VENDEDOR"
            vies = "VIÉS VENDEDOR"
        elif resultado <= -1.5:
            classificacao = "VENDA LEVE"
            fluxo = "FLUXO VENDEDOR"
            vies = "VIÉS VENDEDOR"
        else:
            classificacao = "LATERAL"
            fluxo = "FLUXO INDEFINIDO"
            vies = "MERCADO LATERAL"

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: rgba(10,10,10,0.82); border-radius: 30px; padding: 50px; text-align:center; border:1px solid rgba(255,255,255,0.08);">
            <h3 style="color:#9ca3af; letter-spacing:5px;">RESULTADO</h3>
            <h1 style="color:white; font-size:90px;">{round(resultado,2)}</h1>
            <h2 style="color:#00d5ff;">{vies}</h2>
            <h3 style="color:white;">{classificacao}</h3>
            <h4 style="color:#9ca3af;">FORÇA: {round(forca)}%</h4>
            <h4 style="color:#9ca3af;">{fluxo}</h4>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("← Voltar"):
        st.session_state.modo = None
        st.rerun()
