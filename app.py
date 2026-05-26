import streamlit as st
import base64

# ==========================================
# CONFIG
# ==========================================
st.set_page_config(
    page_title="Lukas Andrade Institucional",
    page_icon="📈",
    layout="centered"
)

# ==========================================
# FUNDO
# ==========================================
def get_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_base64("fundo.jpg")

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
    background: rgba(10,10,10,0.82);
    padding: 2rem;
    border-radius: 20px;
    backdrop-filter: blur(8px);
}}

html, body, [class*="css"] {{
    color: white;
    font-family: Arial;
}}

.stNumberInput input {{
    background-color: rgba(20,20,20,0.9);
    color: white;
}}

.stSelectbox div {{
    background-color: rgba(20,20,20,0.9);
    color: white;
}}

.stButton > button {{
    width: 100%;
    height: 65px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(90deg,#00c853,#00e676);
    color: white;
    font-size: 22px;
    font-weight: bold;
}}

</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ==========================================
# TÍTULO
# ==========================================
st.markdown("""
# 📈 Lukas Andrade Institucional
### Institutional Reading
""")

st.markdown("---")

# ==========================================
# MODO
# ==========================================
modo = st.selectbox(
    "MODO",
    ["SEM NOTÍCIA", "COM NOTÍCIA"]
)

# ==========================================
# INPUTS
# ==========================================
if modo == "SEM NOTÍCIA":

    c1, c2, c3 = st.columns(3)

    with c1:
        vix = st.number_input(
            "VIX",
            value=0.0,
            step=0.01
        )

    with c2:
        fef2 = st.number_input(
            "FEF2",
            value=0.0,
            step=0.01
        )

    with c3:
        cl1 = st.number_input(
            "CL1",
            value=0.0,
            step=0.01
        )

else:

    c1, c2, c3 = st.columns(3)

    with c1:
        vale = st.number_input("VALE", value=0.0)
        bdory = st.number_input("BDORY", value=0.0)

    with c2:
        pbr = st.number_input("PBR", value=0.0)
        bbd = st.number_input("BBD", value=0.0)

    with c3:
        itub = st.number_input("ITUB", value=0.0)
        bolsy = st.number_input("BOLSY", value=0.0)

# ==========================================
# BOTÃO
# ==========================================
st.markdown("---")

executar = st.button("🚀 EXECUTAR")

# ==========================================
# FUNÇÕES
# ==========================================
def classificar(resultado):

    if resultado >= 4.5:
        return "COMPRA FORTE"

    elif resultado >= 2.5:
        return "COMPRA MODERADA"

    elif resultado >= 1.5:
        return "COMPRA LEVE"

    elif resultado <= -4.5:
        return "VENDA FORTE"

    elif resultado <= -2.5:
        return "VENDA MODERADA"

    elif resultado <= -1.5:
        return "VENDA LEVE"

    return "LATERAL"


def vies(resultado):

    if resultado > 0:
        return "VIÉS COMPRADOR"

    elif resultado < 0:
        return "VIÉS VENDEDOR"

    return "MERCADO LATERAL"


def fluxo(classificacao):

    if "COMPRA" in classificacao:
        return "FLUXO COMPRADOR"

    elif "VENDA" in classificacao:
        return "FLUXO VENDEDOR"

    return "FLUXO INDEFINIDO"

# ==========================================
# EXECUÇÃO
# ==========================================
if executar:

    # ==========================================
    # SEM NOTÍCIA
    # ==========================================
    if modo == "SEM NOTÍCIA":

        # VIX INVERTIDO
        vix_invertido = vix * -1

        resultado = (
            vix_invertido +
            fef2 +
            cl1
        )

    # ==========================================
    # COM NOTÍCIA
    # ==========================================
    else:

        resultado = (
            vale +
            pbr +
            itub +
            bdory +
            bbd +
            bolsy
        )

    classificacao = classificar(resultado)

    leitura_vies = vies(resultado)

    leitura_fluxo = fluxo(classificacao)

    intensidade = min(abs(resultado) * 20, 100)

    # ==========================================
    # DESTAQUE
    # ==========================================
    st.markdown("---")

    m1, m2 = st.columns(2)

    with m1:

        st.markdown(f"""
        <div style="
            background: rgba(0,0,0,0.55);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            border: 2px solid #00e676;
            box-shadow: 0px 0px 25px rgba(0,255,100,0.35);
        ">
            <h3 style="color:white;">RESULTADO</h3>
            <h1 style="
                color:#00e676;
                font-size:60px;
                margin-top:-10px;
            ">
                {round(resultado,2)}
            </h1>
        </div>
        """, unsafe_allow_html=True)

    with m2:

        st.markdown(f"""
        <div style="
            background: rgba(0,0,0,0.55);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            border: 2px solid #00e676;
            box-shadow: 0px 0px 25px rgba(0,255,100,0.35);
        ">
            <h3 style="color:white;">FORÇA</h3>
            <h1 style="
                color:#00e676;
                font-size:60px;
                margin-top:-10px;
            ">
                {round(intensidade)}%
            </h1>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # LEITURA
    # ==========================================
    st.markdown("---")

    if intensidade >= 80:

        st.success("🟢 FORÇA EXTREMA")

    elif intensidade >= 60:

        st.warning("🟡 FORÇA FORTE")

    else:

        st.error("⚪ FORÇA FRACA")

    st.markdown(f"""
# {leitura_vies}

## {classificacao}

### {leitura_fluxo}
""")
