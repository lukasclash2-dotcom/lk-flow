import time
import os
import base64
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
from streamlit_autorefresh import st_autorefresh

# --- DEFINA A FUNÇÃO AQUI NO TOPO ---
def custom_label(texto):
    st.markdown(f'<p style="color: white; font-size: 20px; font-weight: bold; margin-bottom: 5px;">{texto}</p>', unsafe_allow_html=True)

# O restante do seu código vem abaixo...

def get_market_data():
    tickers = {
        'VIX': '^VIX', 'FEF2': 'FEF=F', 'CL1': 'CL=F', 'DI1F29': 'DI1F29.SA',
        'VALE': 'VALE3.SA', 'PBR': 'PBR', 'ITUB': 'ITUB4.SA', 'BDORY': 'BDORY', 
        'BBD': 'BBD', 'BOLSY': 'BOLSY', 'BRENT': 'BZ=F', 'EWZ': 'EWZ'
    }
    data = yf.download(list(tickers.values()), period='2d')['Close']
    variacoes = {}
    for nome, ticker in tickers.items():
        atual = data[ticker].iloc[-1]
        anterior = data[ticker].iloc[-2]
        variacoes[nome] = round(((atual / anterior) - 1) * 100, 2)
    return variacoes

# NOVA FUNÇÃO: Constrói esferas 3D matemáticas verdadeiras
def criar_esfera(x_c, y_c, z_c, r):
    u = np.linspace(0, 2 * np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x = r * np.outer(np.cos(u), np.sin(v)) + x_c
    y = r * np.outer(np.sin(u), np.sin(v)) + y_c
    z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + z_c
    return x, y, z

def render_gps_mercado():
    dados = get_market_data()
    ativos, variacoes = list(dados.keys()), list(dados.values())
    
    # --- LÓGICA DE CORES DO CENTRO ---
    ativos_em_alta = sum(1 for v in variacoes if v >= 0)
    ativos_em_queda = sum(1 for v in variacoes if v < 0)
    
    # Regra de coloração central
    if ativos_em_alta > 4:
        cor_centro = '#00ff66' # Verde
    elif ativos_em_queda > 4:
        cor_centro = '#ff3333' # Vermelho
    else:
        cor_centro = '#ffcc00' # Laranja padrão
    
    # Cores dos planetas
    cores = ['#00ff66' if v >= 0 else '#ff3333' for v in variacoes]
    
    fig = go.Figure()
    
    # --- 1. CAMPO ESTELAR ---
    np.random.seed(42)
    num_estrelas = 300
    fig.add_trace(go.Scatter3d(
        x=np.random.uniform(-35, 35, num_estrelas),
        y=np.random.uniform(-35, 35, num_estrelas),
        z=np.random.uniform(-20, 20, num_estrelas),
        mode='markers',
        marker=dict(size=np.random.uniform(1, 2.5, num_estrelas), color='white', opacity=0.4),
        hoverinfo='none', showlegend=False
    ))

    # --- 2. ANEL DA ÓRBITA ---
    theta_ring = np.linspace(0, 2*np.pi, 150)
    raio_orbita = 15
    fig.add_trace(go.Scatter3d(
        x=raio_orbita * np.cos(theta_ring),
        y=raio_orbita * np.sin(theta_ring),
        z=np.zeros(150),
        mode='lines',
        line=dict(color='rgba(255, 255, 255, 0.3)', width=2, dash='dot'),
        hoverinfo='none', showlegend=False
    ))

    # --- 3. PLANETAS 3D ---
    theta = np.linspace(0, 2*np.pi, len(ativos), endpoint=False)
    raio_planeta = 1.3
    
    for i in range(len(ativos)):
        x_p = raio_orbita * np.cos(theta[i])
        y_p = raio_orbita * np.sin(theta[i])
        z_p = 0
        
        x_esf, y_esf, z_esf = criar_esfera(x_p, y_p, z_p, raio_planeta)
        
        # Superfície do planeta (Corrigido: parâmetros diretos sem atribuições extras)
        fig.add_trace(go.Surface(
            x=x_esf, y=y_esf, z=z_esf,
            colorscale=[[0, cores[i]], [1, cores[i]]],
            showscale=False,
            lighting=dict(ambient=0.3, diffuse=0.9, roughness=0.6, specular=0.4),
            lightposition=dict(x=0, y=0, z=0),
            hoverinfo='none'
        ))
        
        fig.add_trace(go.Scatter3d(
            x=[x_p], y=[y_p], z=[z_p - (raio_planeta * 1.8)],
            mode='text',
            text=[f"<b>{ativos[i]}</b><br>{variacoes[i]}%"],
            textfont=dict(color='white', size=13),
            showlegend=False, hoverinfo='none'
        ))

    # --- 4. SOL CENTRAL (WIN1 - ESFERA 3D COM VOLUME) ---
    raio_sol = 3.5
    x_sol, y_sol, z_sol = criar_esfera(0, 0, 0, raio_sol)
    
    fig.add_trace(go.Surface(
        x=x_sol, y=y_sol, z=z_sol,
        colorscale=[[0, cor_centro], [1, cor_centro]],
        showscale=False,
        lighting=dict(ambient=0.4, diffuse=0.6, roughness=0.5, specular=0.2),
        lightposition=dict(x=10, y=10, z=10), 
        hoverinfo='none'
    ))
    
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[raio_sol + 2.0],
        mode='text',
        text=["<b>WIN1</b>"],
        textfont=dict(color='white', size=14),
        showlegend=False, hoverinfo='none'
    ))

    # --- 5. CONFIGURAÇÃO DE CÂMERA E PROPORÇÃO ---
    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=0, y=-1.6, z=0.9) 
    )

    fig.update_layout(
        paper_bgcolor='rgba(5, 5, 5, 0.8)', 
        plot_bgcolor='rgba(0, 0, 0, 0)',
        scene_camera=camera,
        scene=dict(
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=1), 
            bgcolor='rgba(0,0,0,0)',
            xaxis=dict(visible=False, range=[-20, 20]),
            yaxis=dict(visible=False, range=[-20, 20]),
            zaxis=dict(visible=False, range=[-20, 20])
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=750 
    )    
    st.plotly_chart(
    fig, 
    use_container_width=True, 
    config={'displayModeBar': False}, 
    key=f"grafico_gps_{time.time()}" 
)

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

</style>
""", unsafe_allow_html=True)

# ==================================================
# HERO (CORRIGIDO: Sem quebras de linha nas tags)
# ==================================================

# ==================================================
# HERO (CORRIGIDO DEFINITIVO: Sem espaços em branco)
# ==================================================

html_hero = f"""<div style="position: relative; border-radius: 30px; overflow: hidden; background: rgba(0,0,0,0.85); border: 1px solid rgba(255,255,255,0.08);"><img src="data:image/jpg;base64,{img}" style="width:100%; height:650px; object-fit:cover; opacity:0.28;"><div style="position:absolute; top:0; left:0; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;"><h4 style="color:#bdbdbd; letter-spacing:10px; font-weight:300; margin-bottom:15px;">abertura</h4><h1 style="font-size:120px; font-weight:900; color:white; letter-spacing:10px; margin-top:-10px;">LaVinceri</h1><p style="color:#9ca3af; font-size:18px; margin-top:-10px;">LaVinceri Abertura Institutional</p></div></div>"""

st.markdown(html_hero, unsafe_allow_html=True)
# ==================================================
# MENU
# ==================================================

st.sidebar.title("Navegação")

# Botão do GPS
if st.sidebar.button("🧭 GPS Mercado", use_container_width=True):
    st.session_state.modo = "gps"
    st.rerun()

# Botão para voltar à página inicial da notícia
if st.sidebar.button("🏠 Início", use_container_width=True):
    st.session_state.modo = None
    st.rerun()

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

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    # Função interna rápida para o seu rótulo estilizado
    def custom_label(texto):
        st.markdown(f'<p style="color: white; font-size: 20px; font-weight: bold; margin-bottom: 5px;">{texto}</p>', unsafe_allow_html=True)

    with c1:
        custom_label("VIX")
        vix = st.number_input("VIX", value=None, placeholder="0.0", label_visibility="collapsed")

    with c2:
        custom_label("FEF")
        fef = st.number_input("FEF", value=None, placeholder="0.0", label_visibility="collapsed")

    with c3:
        custom_label("CL")
        cl = st.number_input("CL", value=None, placeholder="0.0", label_visibility="collapsed")

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

    if st.button("← Voltar", key="voltar_macro"):
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
        custom_label("VALE")
        vale = st.number_input("VALE", value=None, placeholder="0.0", label_visibility="collapsed")
        custom_label("ITUB")
        itub = st.number_input("ITUB", value=None, placeholder="0.0", label_visibility="collapsed")
        custom_label("BBD")
        bbd = st.number_input("BBD", value=None, placeholder="0.0", label_visibility="collapsed")

    with c2:
        custom_label("PBR")
        pbr = st.number_input("PBR", value=None, placeholder="0.0", label_visibility="collapsed")
        custom_label("BDORY")
        bdory = st.number_input("BDORY", value=None, placeholder="0.0", label_visibility="collapsed")
        custom_label("BOLSY")
        bolsy = st.number_input("BOLSY", value=None, placeholder="0.0", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Gerar leitura", key="gerar_leitura_adr", use_container_width=True):
        # Transforma os campos vazios em 0
        v_vale = vale if vale is not None else 0.0
        v_itub = itub if itub is not None else 0.0
        v_bbd = bbd if bbd is not None else 0.0
        v_pbr = pbr if pbr is not None else 0.0
        v_bdory = bdory if bdory is not None else 0.0
        v_bolsy = bolsy if bolsy is not None else 0.0

        resultado = v_vale + v_pbr + v_itub + v_bdory + v_bbd + v_bolsy
        forca = min(abs(resultado) * 20, 100)

        # Lógica de Classificação
        if resultado >= 4.5:
            classificacao, fluxo, vies = "COMPRA FORTE", "FLUXO COMPRADOR", "VIÉS COMPRADOR"
        elif resultado >= 2.5:
            classificacao, fluxo, vies = "COMPRA MODERADA", "FLUXO COMPRADOR", "VIÉS COMPRADOR"
        elif resultado >= 1.5:
            classificacao, fluxo, vies = "COMPRA LEVE", "FLUXO COMPRADOR", "VIÉS COMPRADOR"
        elif resultado <= -4.5:
            classificacao, fluxo, vies = "VENDA FORTE", "FLUXO VENDEDOR", "VIÉS VENDEDOR"
        elif resultado <= -2.5:
            classificacao, fluxo, vies = "VENDA MODERADA", "FLUXO VENDEDOR", "VIÉS VENDEDOR"
        elif resultado <= -1.5:
            classificacao, fluxo, vies = "VENDA LEVE", "FLUXO VENDEDOR", "VIÉS VENDEDOR"
        else:
            classificacao, fluxo, vies = "LATERAL", "FLUXO INDEFINIDO", "MERCADO LATERAL"

        # Lógica de Confluência
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

        # Exibição Final
        st.markdown(f"""
        <div style="background: rgba(10,10,10,0.82); border-radius: 30px; padding: 50px; text-align:center; border:1px solid rgba(255,255,255,0.08);">
            <h3 style="color:#9ca3af; letter-spacing:5px;">RESULTADO</h3>
            <h1 style="color:white; font-size:90px;">{round(resultado,2)}%</h1>
            <h2 style="color:#00d5ff;">{vies}</h2>
            <h3 style="color:white;">{classificacao}</h3>
            <h4 style="color:#9ca3af;">FORÇA: {round(forca)}%</h4>
            <h4 style="color:#9ca3af;">{fluxo}</h4>
            {html_confluencia}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Voltar", key="voltar_adr"):
        st.session_state.modo = None
        st.rerun()

elif st.session_state.modo == "gps":
    st.header("GPS Mercado")
    
    # Ele fica aqui no nível principal do "elif"
    st_autorefresh(interval=120000, key="gps_refresh_unique")
    
    # Chama o desenho do gráfico que colocamos lá no topo
    render_gps_mercado()
