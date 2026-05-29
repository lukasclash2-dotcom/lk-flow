import streamlit as st
import base64

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(
    page_title="LK FLOW",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# SESSION
# ==========================================
if "modo" not in st.session_state:
    st.session_state.modo = None

# ==========================================
# BASE64
# ==========================================
def get_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_base64("fundo.jpg")

# ==========================================
# CSS
# ==========================================
page_bg = f"""
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
    padding-top: 2rem;
    max-width: 900px;
}}

html, body, [class*="css"] {{
    color: white;
    font-family: Arial;
}}

.stNumberInput input {{
    background-color: rgba(20,20,20,0.65);
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.06);
}}

.stTextInput input {{
    background-color: rgba(20,20,20,0.65);
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.06);
}}

.stButton > button {{
    width: 100%;
    height: 75px;
    border-radius: 50px;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(10,10,10,0.92);
    color: white;
    font-size: 24px;
    font-weight: 600;
    transition: 0.3s;
    backdrop-filter: blur(10px);
    box-shadow: 0px 0px 25px rgba(0,0,0,0.45);
}}

.stButton > button:hover {{
    transform: scale(1.01);
    border: 1px solid rgba(0,255,255,0.4);
    box-shadow: 0px 0px 25px rgba(0,255,255,0.25);
}}

</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ==========================================
# HERO
# ==========================================
st.markdown(f'''
<div style="
    position: relative;
    border-radius: 25px;
    overflow: hidden;
    background: rgba(0,0,0,0.85);
    border: 1px solid rgba(0,255,255,0.08);
    box-shadow: 0px 0px 30px rgba(0,0,0,0.45);
">

    <img src="data:image/jpg;base64,{img}" style="
        width:100%;
        height:780px;
        object-fit:cover;
        opacity:0.28;
    ">

    <div style="
        position:absolute;
        top:0;
        left:0;
        width:100%;
        height:100%;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        text-align:center;
        padding:40px;
    ">

        <h4 style="
            color:#cfcfcf;
            letter-spacing:10px;
            font-weight:300;
            margin-bottom:20px;
        ">
            abertura
        </h4>

        <h1 style="
            font-size:130px;
            font-weight:900;
            color:white;
            letter-spacing:10px;
            margin-top:-20px;
        ">
            HOUND
        </h1>

        <p style="
            color:#9ca3af;
            margin-top:-10px;
            font-size:18px;
        ">
            Institutional opening flow
        </p>

    </div>

</div>
''', unsafe_allow_html=True)

# ==========================================
# ESCOLHA
# ==========================================
if st.session_state.modo is None:

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""

    <div style="
        background: rgba(15,15,15,0.72);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 30px;
        padding: 40px;
        margin-top: 30px;
        backdrop-filter: blur(18px);
        box-shadow: 0px 0px 35px rgba(0,0,0,0.45);
    ">

    <p style="
        color:#8b8b8b;
        letter-spacing:4px;
        font-size:13px;
    ">
    ENTRADA MANUAL
    </p>

    <h1 style="
        color:white;
        font-size:42px;
    ">
    Há notícia 3⭐ no Brasil às 09h hoje?
    </h1>

    <p style="
        color:#8b8b8b;
        font-size:18px;
    ">
    Isso define se o cálculo usa a fórmula macro
    (-VIX + FEF + CL) ou ADRs.
    </p>

    </div>

    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:

        if st.button("Não", use_container_width=True):

            st.session_state.modo = "SEM NOTÍCIA"
            st.rerun()

    with c2:

        if st.button("Sim", use_container_width=True):

            st.session_state.modo = "COM NOTÍCIA"
            st.rerun()

# ==========================================
# SEM NOTÍCIA
# ==========================================
elif st.session_state.modo == "SEM NOTÍCIA":

    st.markdown("""

    <div style="
        background: rgba(15,15,15,0.72);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 30px;
        padding: 40px;
        margin-top: 30px;
        backdrop-filter: blur(18px);
    ">

    <p style="
        color:#8b8b8b;
        letter-spacing:4px;
        font-size:13px;
    ">
    ENTRADA MANUAL
    </p>

    <h1 style="
        color:white;
        font-size:42px;
    ">
    Insira as variações do macro
    </h1>

    </div>

    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        vix = st.number_input("VIX", value=0.0)

    with c2:
        fef2 = st.number_input("FEF", value=0.0)

    with c3:
        cl1 = st.number_input("CL", value=0.0)

    st.markdown("<br>", unsafe_allow_html=True)

    gerar = st.button("Gerar leitura")

    if gerar:

        resultado = (-vix) + fef2 + cl1

        intensidade = min(abs(resultado) * 20, 100)

        if resultado >= 4.5:
            classificacao = "COMPRA FORTE"
        elif resultado >= 2.5:
            classificacao = "COMPRA MODERADA"
        elif resultado >= 1.5:
            classificacao = "COMPRA LEVE"
        elif resultado <= -4.5:
            classificacao = "VENDA FORTE"
        elif resultado <= -2.5:
            classificacao = "VENDA MODERADA"
        elif resultado <= -1.5:
            classificacao = "VENDA LEVE"
        else:
            classificacao = "LATERAL"

        if resultado > 0:
            vies = "VIÉS COMPRADOR"
            fluxo = "FLUXO COMPRADOR"
        elif resultado < 0:
            vies = "VIÉS VENDEDOR"
            fluxo = "FLUXO VENDEDOR"
        else:
            vies = "MERCADO LATERAL"
            fluxo = "FLUXO INDEFINIDO"

        st.markdown("---")

        st.markdown(f"""
        <div style="
            background: rgba(0,0,0,0.72);
            border-radius:25px;
            padding:40px;
            border:1px solid rgba(255,255,255,0.08);
            text-align:center;
        ">

            <h3 style="
                color:#9ca3af;
                letter-spacing:4px;
            ">
                RESULTADO
            </h3>

            <h1 style="
                color:white;
                font-size:95px;
            ">
                {round(resultado,2)}
            </h1>

            <h2 style="
                color:#00c8ff;
            ">
                {vies}
            </h2>

            <h3 style="color:white;">
                {classificacao}
            </h3>

            <h4 style="color:#9ca3af;">
                FORÇA: {round(intensidade)}%
            </h4>

            <h4 style="color:#9ca3af;">
                {fluxo}
            </h4>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("← Voltar"):

        st.session_state.modo = None
        st.rerun()

# ==========================================
# COM NOTÍCIA
# ==========================================
elif st.session_state.modo == "COM NOTÍCIA":

    st.markdown("""

    <div style="
        background: rgba(15,15,15,0.72);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 30px;
        padding: 40px;
        margin-top: 30px;
        backdrop-filter: blur(18px);
    ">

    <p style="
        color:#8b8b8b;
        letter-spacing:4px;
        font-size:13px;
    ">
    ENTRADA MANUAL
    </p>

    <h1 style="
        color:white;
        font-size:42px;
    ">
    Insira as variações das ADRs
    </h1>

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

    gerar = st.button("Gerar leitura")

    if gerar:

        resultado = (
            vale +
            pbr +
            itub +
            bdory +
            bbd +
            bolsy
        )

        intensidade = min(abs(resultado) * 20, 100)

        if resultado >= 4.5:
            classificacao = "COMPRA FORTE"
        elif resultado >= 2.5:
            classificacao = "COMPRA MODERADA"
        elif resultado >= 1.5:
            classificacao = "COMPRA LEVE"
        elif resultado <= -4.5:
            classificacao = "VENDA FORTE"
        elif resultado <= -2.5:
            classificacao = "VENDA MODERADA"
        elif resultado <= -1.5:
            classificacao = "VENDA LEVE"
        else:
            classificacao = "LATERAL"

        if resultado > 0:
            vies = "VIÉS COMPRADOR"
            fluxo = "FLUXO COMPRADOR"
        elif resultado < 0:
            vies = "VIÉS VENDEDOR"
            fluxo = "FLUXO VENDEDOR"
        else:
            vies = "MERCADO LATERAL"
            fluxo = "FLUXO INDEFINIDO"

        st.markdown("---")

        st.markdown(f"""
        <div style="
            background: rgba(0,0,0,0.72);
            border-radius:25px;
            padding:40px;
            border:1px solid rgba(255,255,255,0.08);
            text-align:center;
        ">

            <h3 style="
                color:#9ca3af;
                letter-spacing:4px;
            ">
                RESULTADO
            </h3>

            <h1 style="
                color:white;
                font-size:95px;
            ">
                {round(resultado,2)}
            </h1>

            <h2 style="
                color:#00c8ff;
            ">
                {vies}
            </h2>

            <h3 style="color:white;">
                {classificacao}
            </h3>

            <h4 style="color:#9ca3af;">
                FORÇA: {round(intensidade)}%
            </h4>

            <h4 style="color:#9ca3af;">
                {fluxo}
            </h4>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("← Voltar"):

        st.session_state.modo = None
        st.rerun()
