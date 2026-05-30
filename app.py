import streamlit as st
import base64
import os

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="LaVinceri",
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

caminho_completo = os.path.join(os.path.dirname(__file__), "fundo.jpg")
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

/* === ESTILO PREMIUM PARA OS INPUTS === */
.stNumberInput > div > div > input {{
    background: rgba(15,15,15,0.8);
    color: white;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.1);
    text-align: center; /* Centraliza os números */
    font-size: 18px;
    transition: 0.3s;
}}

/* Efeito de brilho ao clicar no campo */
.stNumberInput > div > div > input:focus {{
    border: 1px solid rgba(0,255,255,0.5);
    box-shadow: 0px 0px 15px rgba(0,255,255,0.2);
}}

/* Esconde os botões de + e - para um visual mais limpo */
    [data-testid="stNumberInputStepUp"],
    [data-testid="stNumberInputStepDown"] {{
        display: none;
    }}

    /* === AJUSTES PARA CELULAR (RESPONSIVIDADE) === */
    @media (max-width: 600px) {{
        .block-container {{ 
            padding-left: 10px !important; 
            padding-right: 10px !important; 
        }}
        /* Alvo ampliado: pega tanto o de 40px quanto o de 50px */
        div[style*="padding: 40px"], div[style*="padding: 50px"] {{ 
            padding: 15px !important; 
            border-radius: 15px !important;
        }}
        /* Reduz tamanho de h1 e h2 para não quebrar a linha */
        h1 {{ font-size: 30px !important; line-height: 1.2 !important; }}
        h2 {{ font-size: 20px !important; }}
    }}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HERO (CORRIGIDO: Sem quebras de linha nas tags)
# ==================================================

# ==================================================
# HERO (CORRIGIDO DEFINITIVO: Sem espaços em branco)
# ==================================================

html_hero = f"""<div style="position: relative; border-radius: 30px; overflow: hidden; background: rgba(0,0,0,0.85); border: 1px solid rgba(255,255,255,0.08);"><img src="data:image/jpg;base64,{img}" style="width:100%; height:650px; object-fit:cover; opacity:0.28;"><div style="position:absolute; top:0; left:0; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;"><h4 style="color:#bdbdbd; letter-spacing:10px; font-weight:300; margin-bottom:15px;">ABERTURA RASTREADA</h4><h1 style="font-size:120px; font-weight:900; color:white; letter-spacing:10px; margin-top:-10px;">LaVinceri</h1><p style="color:#9ca3af; font-size:18px; margin-top:-10px;">LaVinceri Abertura Institutional</p></div></div>"""

st.markdown(html_hero, unsafe_allow_html=True)
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

    c1, c2 = st.columns(2)

    with c1:
        # Adicionamos o use_container_width=True
        if st.button("Não", use_container_width=True):
            st.session_state.modo = "macro"
            st.rerun()

    with c2:
        # Adicionamos o use_container_width=True
        if st.button("Sim", use_container_width=True):
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

    c1, c2, c3 = st.columns(3)

    with c1:
        vix = st.number_input("VIX", value=None, placeholder="0.0")

    with c2:
        fef = st.number_input("FEF", value=None, placeholder="0.0")

    with c3:
        cl = st.number_input("CL", value=None, placeholder="0.0")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Gerar leitura", use_container_width=True):
        
        # Como deixamos vazio, precisamos garantir que espaços em branco sejam lidos como 0
        v_vix = vix if vix is not None else 0.0
        v_fef = fef if fef is not None else 0.0
        v_cl = cl if cl is not None else 0.0

        resultado = (-v_vix) + v_fef + v_cl

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
            <h1 style="color:white; font-size:90px;">{round(resultado,2)}%</h1>
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

    c1, c2 = st.columns(2)

    with c1:
        vale = st.number_input("VALE", value=None, placeholder="0.0")
        itub = st.number_input("ITUB", value=None, placeholder="0.0")
        bbd = st.number_input("BBD", value=None, placeholder="0.0")

    with c2:
        pbr = st.number_input("PBR", value=None, placeholder="0.0")
        bdory = st.number_input("BDORY", value=None, placeholder="0.0")
        bolsy = st.number_input("BOLSY", value=None, placeholder="0.0")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Gerar leitura", use_container_width=True):

        # Transforma os campos vazios em 0 para não dar erro no cálculo
        v_vale = vale if vale is not None else 0.0
        v_itub = itub if itub is not None else 0.0
        v_bbd = bbd if bbd is not None else 0.0
        v_pbr = pbr if pbr is not None else 0.0
        v_bdory = bdory if bdory is not None else 0.0
        v_bolsy = bolsy if bolsy is not None else 0.0

        resultado = v_vale + v_pbr + v_itub + v_bdory + v_bbd + v_bolsy

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

# --- Lógica de Confluência ---
        dicionario_adrs = {
            "VALE": v_vale, "ITUB": v_itub, "BBD": v_bbd,
            "PBR": v_pbr, "BDORY": v_bdory, "BOLSY": v_bolsy
        }
        
        positivos = [nome for nome, valor in dicionario_adrs.items() if valor > 0]
        negativos = [nome for nome, valor in dicionario_adrs.items() if valor < 0]
        
        html_confluencia = ""
        if len(positivos) >= 4:
            texto = f"CONFLUÊNCIA: {', '.join(positivos)} na mesma direção (Alta)"
            html_confluencia = f'<h4 style="color:#ffd700; margin-top:25px; font-weight:600; letter-spacing: 1px;">⭐ {texto}</h4>'
        elif len(negativos) >= 4:
            texto = f"CONFLUÊNCIA: {', '.join(negativos)} na mesma direção (Baixa)"
            html_confluencia = f'<h4 style="color:#ffd700; margin-top:25px; font-weight:600; letter-spacing: 1px;">⭐ {texto}</h4>'

        st.markdown("<br>", unsafe_allow_html=True)

        # SUBSTITUA O ST.MARKDOWN ABAIXO POR ESTA LINHA ÚNICA (SEM QUEBRAS):
        st.markdown(f"""<div style="background: rgba(10,10,10,0.82); border-radius: 30px; padding: 50px; text-align:center; border:1px solid rgba(255,255,255,0.08);"><h3 style="color:#9ca3af; letter-spacing:5px;">RESULTADO</h3><h1 style="color:white; font-size:90px;">{round(resultado,2)}%</h1><h2 style="color:#00d5ff;">{vies}</h2><h3 style="color:white;">{classificacao}</h3><h4 style="color:#9ca3af;">FORÇA: {round(forca)}%</h4><h4 style="color:#9ca3af;">{fluxo}</h4>{html_confluencia}</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    if st.button("← Voltar"):
        st.session_state.modo = None
        st.rerun()
