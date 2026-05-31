import os
import base64
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
from streamlit_autorefresh import st_autorefresh
import time
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import math  # Essencial para o cálculo da rotação

# Inicializa o estado da câmera para a rotação automática
if "camera_angle" not in st.session_state:
    st.session_state.camera_angle = 0.0

# ==================================================
# 1. CONFIGURAÇÕES INICIAIS
# ==================================================
st.set_page_config(page_title="LaVinceri", layout="wide")

if "modo" not in st.session_state:
    st.session_state.modo = None

# ==================================================
# 2. CARREGAMENTO DE IMAGEM E CSS
# ==================================================
def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

caminho_completo = os.path.join(os.path.dirname(__file__), "assets", "fundo.jpg")
img = get_base64(caminho_completo)

if img:
    st.markdown(f"""
    <style>
    /* Estilização Geral */
    .stApp {{
        background-image: url("data:image/jpg;base64,{img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}
    .block-container {{ max-width: 900px; padding-top: 2rem; }}
    html, body, [class*="css"] {{ color: white; font-family: Arial; }}

    /* Sidebar Premium (Glassmorphism) */
    [data-testid="stSidebar"] {{
        background: rgba(10, 10, 10, 0.4) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }}

    /* Botões da Sidebar - Visual Limpo */
    [data-testid="stSidebar"] button {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        transition: 0.3s;
    }}

    /* --- INÍCIO DO NOVO CÓDIGO GLASSMORPHISM --- */
    
    /* Glassmorphism para o formulário de login */
    [data-testid="stForm"] {{
        background: rgba(10, 10, 10, 0.4) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 30px !important;
    }}

    /* Ajuste das caixas de input dentro do login */
    [data-testid="stForm"] input {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }}

    /* --- FIM DO NOVO CÓDIGO --- */

    /* Botões Principais (Página) */
    .stButton > button {{
        width: 100%; height: 75px; border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.08); background: rgba(15,15,15,0.72);
        color: white; font-size: 24px; font-weight: 600; transition: 0.3s;
        backdrop-filter: blur(10px);
    }}
    </style>
    """, unsafe_allow_html=True)

# ==================================================
# 3. FUNÇÕES LÓGICAS E DE GRÁFICO
# ==================================================
def custom_label(texto):
    st.markdown(f'<p style="color: white; font-size: 20px; font-weight: bold; margin-bottom: 5px;">{texto}</p>', unsafe_allow_html=True)

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

def criar_esfera(x_c, y_c, z_c, r):
    u = np.linspace(0, 2 * np.pi, 15) 
    v = np.linspace(0, np.pi, 15)
    x = r * np.outer(np.cos(u), np.sin(v)) + x_c
    y = r * np.outer(np.sin(u), np.sin(v)) + y_c
    z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + z_c
    return x, y, z

def render_gps_mercado():
    # Incrementa a rotação
    st.session_state.camera_angle += 0.02
    raio_camera = 1.6
    cam_x = raio_camera * math.sin(st.session_state.camera_angle)
    cam_y = raio_camera * math.cos(st.session_state.camera_angle)

    dados = get_market_data()
    ativos, variacoes = list(dados.keys()), list(dados.values())
    
    ativos_em_alta = sum(1 for v in variacoes if v >= 0)
    ativos_em_queda = sum(1 for v in variacoes if v < 0)
    
    if ativos_em_alta > 4: cor_centro = '#00ff66'
    elif ativos_em_queda > 4: cor_centro = '#ff3333'
    else: cor_centro = '#ffcc00'
    
    cores = ['#00ff66' if v >= 0 else '#ff3333' for v in variacoes]
    
    fig = go.Figure()
    
    np.random.seed(42)
    num_estrelas = 300
    fig.add_trace(go.Scatter3d(
        x=np.random.uniform(-35, 35, num_estrelas), y=np.random.uniform(-35, 35, num_estrelas), z=np.random.uniform(-20, 20, num_estrelas),
        mode='markers', marker=dict(size=np.random.uniform(1, 2.5, num_estrelas), color='white', opacity=0.4),
        hoverinfo='none', showlegend=False
    ))

    theta_ring = np.linspace(0, 2*np.pi, 150)
    raio_orbita = 15
    fig.add_trace(go.Scatter3d(
        x=raio_orbita * np.cos(theta_ring), y=raio_orbita * np.sin(theta_ring), z=np.zeros(150),
        mode='lines', line=dict(color='rgba(255, 255, 255, 0.3)', width=2, dash='dot'), hoverinfo='none', showlegend=False
    ))

    theta = np.linspace(0, 2*np.pi, len(ativos), endpoint=False)
    raio_planeta = 1.3
    for i in range(len(ativos)):
        x_p = raio_orbita * np.cos(theta[i])
        y_p = raio_orbita * np.sin(theta[i])
        z_p = 0
        x_esf, y_esf, z_esf = criar_esfera(x_p, y_p, z_p, raio_planeta)
        
        fig.add_trace(go.Surface(x=x_esf, y=y_esf, z=z_esf, colorscale=[[0, cores[i]], [1, cores[i]]], showscale=False, lighting=dict(ambient=0.3, diffuse=0.9, roughness=0.6, specular=0.4), lightposition=dict(x=0, y=0, z=0), hoverinfo='none'))
        fig.add_trace(go.Scatter3d(x=[x_p], y=[y_p], z=[z_p - (raio_planeta * 1.8)], mode='text', text=[f"<b>{ativos[i]}</b><br>{variacoes[i]}%"], textfont=dict(color='white', size=13), showlegend=False, hoverinfo='none'))

    raio_sol = 3.5
    x_sol, y_sol, z_sol = criar_esfera(0, 0, 0, raio_sol)
    fig.add_trace(go.Surface(x=x_sol, y=y_sol, z=z_sol, colorscale=[[0, cor_centro], [1, cor_centro]], showscale=False, lighting=dict(ambient=0.4, diffuse=0.6, roughness=0.5, specular=0.2), lightposition=dict(x=10, y=10, z=10), hoverinfo='none'))
    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[raio_sol + 2.0], mode='text', text=["<b>WIN1</b>"], textfont=dict(color='white', size=14), showlegend=False, hoverinfo='none'))

    camera = dict(up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0), eye=dict(x=cam_x, y=cam_y, z=0.9))
    
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
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key="gps_rotativo")

# ==================================================
# 4. SISTEMA DE AUTENTICAÇÃO E REGISTRO CUSTOMIZADO
# ==================================================
try:
    with open('config.yaml', 'r') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Erro: Arquivo 'config.yaml' não encontrado.")
    st.stop()

# Inicializa o Autenticador
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None

if st.session_state["authentication_status"] is not True:
    aba_login, aba_registro = st.tabs(["🔒 Entrar", "📝 Criar Conta"])
    with aba_login:
        authenticator.login()
        if st.session_state["authentication_status"] is False:
            st.error('Usuário ou senha incorretos')
        elif st.session_state["authentication_status"] is None:
            st.warning('Por favor, insira suas credenciais para acessar o painel')

    with aba_registro:
        st.markdown("<h3 style='color: white; margin-bottom: 20px;'>Registrar novo usuário</h3>", unsafe_allow_html=True)
        with st.form("form_registro_customizado"):
            c1, c2 = st.columns(2)
            with c1:
                nome_novo = st.text_input("Nome")
                email_novo = st.text_input("E-mail")
                senha_nova = st.text_input("Senha", type="password")
            with c2:
                sobrenome_novo = st.text_input("Sobrenome")
                username_novo = st.text_input("Usuário (Login)")
                senha_confirma = st.text_input("Confirmar Senha", type="password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit_registro = st.form_submit_button("Criar Conta", use_container_width=True)

            if submit_registro:
                if not nome_novo or not sobrenome_novo or not email_novo or not username_novo or not senha_nova:
                    st.error("⚠️ Por favor, preencha todos os campos.")
                elif senha_nova != senha_confirma:
                    st.error("⚠️ As senhas não coincidem.")
                else:
                    if 'usernames' not in config['credentials'] or config['credentials']['usernames'] is None:
                        config['credentials']['usernames'] = {}
                    if username_novo in config['credentials']['usernames']:
                        st.error("⚠️ Este nome de usuário já existe. Escolha outro.")
                    else:
                        try:
                            senha_criptografada = stauth.Hasher.hash(senha_nova)
                            config['credentials']['usernames'][username_novo] = {
                                'email': email_novo,
                                'name': f"{nome_novo} {sobrenome_novo}",
                                'password': senha_criptografada
                            }
                            with open('config.yaml', 'w') as file:
                                yaml.dump(config, file, default_flow_style=False)
                            st.success("✅ Conta criada com sucesso! Você já pode usar a aba 'Entrar'.")
                        except Exception as e:
                            st.error(f"Erro ao salvar a conta: {e}")

# ==================================================
# 5. CONTROLE DE ACESSO E NAVEGAÇÃO
# ==================================================
if st.session_state["authentication_status"] is True:
    with st.sidebar:
        st.markdown(f"### 👋 Olá, {st.session_state['name']}")
        st.divider()
        if st.button("🏠 Painel Principal"):
            st.session_state.modo = None
            st.rerun()
        if st.button("🧭 GPS Mercado"):
            st.session_state.modo = "gps"
            st.rerun()
        st.divider()
        authenticator.logout('Sair da conta', 'sidebar')

    if st.session_state.modo == "gps":
        st.header("🧭 GPS Mercado")
        if st.button("← Voltar para o início"):
            st.session_state.modo = None
            st.rerun()
        st_autorefresh(interval=120000, key="gps_refresh")
        render_gps_mercado()
    
    if st.session_state.modo is None:
        if img:
            html_hero = f"""<div style="position: relative; border-radius: 30px; overflow: hidden; background: rgba(0,0,0,0.85); border: 1px solid rgba(255,255,255,0.08);"><img src="data:image/jpg;base64,{img}" style="width:100%; height:650px; object-fit:cover; opacity:0.28;"><div style="position:absolute; top:0; left:0; width:100%; height:100%; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;"><h4 style="color:#bdbdbd; letter-spacing:10px; font-weight:300; margin-bottom:15px;">abertura</h4><h1 style="font-size:120px; font-weight:900; color:white; letter-spacing:10px; margin-top:-10px;">LaVinceri</h1><p style="color:#9ca3af; font-size:18px; margin-top:-10px;">LaVinceri Abertura Institutional</p></div></div>"""
            st.markdown(html_hero, unsafe_allow_html=True)
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
            if st.button("Não", use_container_width=True):
                st.session_state.modo = "macro"
                st.rerun()
        with c2:
            if st.button("Sim", use_container_width=True):
                st.session_state.modo = "adr"
                st.rerun()

    elif st.session_state.modo == "macro":
        st.markdown("""
        <div style="background: rgba(15,15,15,0.72); border-radius: 30px; padding: 40px; border: 1px solid rgba(255,255,255,0.08);">
            <h1 style="color:white; font-size:42px;">Insira as variações do macro</h1>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
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
            v_vix = vix if vix is not None else 0.0
            v_fef = fef if fef is not None else 0.0
            v_cl = cl if cl is not None else 0.0
            resultado = (-v_vix) + v_fef + v_cl
            forca = min(abs(resultado) * 20, 100)
            if resultado >= 4.5: classificacao, fluxo, vies = "COMPRA FORTE", "FLUXO COMPRADOR", "VIÉS COMPRADOR"
            elif resultado >= 2.5: classificacao, fluxo, vies = "COMPRA MODERADA", "FLUXO COMPRADOR", "VIÉS COMPRADOR"
            elif resultado >= 1.5: classificacao, fluxo, vies = "COMPRA LEVE", "FLUXO COMPRADOR", "VIÉS COMPRADOR"
            elif resultado <= -4.5: classificacao, fluxo, vies = "VENDA FORTE", "FLUXO VENDEDOR", "VIÉS VENDEDOR"
            elif resultado <= -2.5: classificacao, fluxo, vies = "VENDA MODERADA", "FLUXO VENDEDOR", "VIÉS VENDEDOR"
            elif resultado <= -1.5: classificacao, fluxo, vies = "VENDA LEVE", "FLUXO VENDEDOR", "VIÉS VENDEDOR"
            else: classificacao, fluxo, vies = "LATERAL", "FLUXO INDEFINIDO", "MERCADO LATERAL"
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

    elif st.session_state.modo == "adr":
        st.markdown("""
        <div style="background: rgba(15,15,15,0.72); border-radius: 30px; padding: 40px; border: 1px solid rgba(255,255,255,0.08);">
            <h1 style="color:white; font-size:42px;">Insira as variações das ADRs</h1>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            custom_label("VALE"); vale = st.number_input("VALE", value=None, placeholder="0.0", label_visibility="collapsed")
            custom_label("ITUB"); itub = st.number_input("ITUB", value=None, placeholder="0.0", label_visibility="collapsed")
            custom_label("BBD"); bbd = st.number_input("BBD", value=None, placeholder="0.0", label_visibility="collapsed")
        with c2:
            custom_label("PBR"); pbr = st.number_input("PBR", value=None, placeholder="0.0", label_visibility="collapsed")
            custom_label("BDORY"); bdory = st.number_input("BDORY", value=None, placeholder="0.0", label_visibility="collapsed")
            custom_label("BOLSY"); bolsy = st.number_input("BOLSY", value=None, placeholder="0.0", label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Gerar leitura", key="gerar_leitura_adr", use_container_width=True):
            v_vale, v_itub, v_bbd = vale or 0.0, itub or 0.0, bbd or 0.0
            v_pbr, v_bdory, v_bolsy = pbr or 0.0, bdory or 0.0, bolsy or 0.0
            resultado = v_vale + v_pbr + v_itub + v_bdory + v_bbd + v_bolsy
            forca = min(abs(resultado) * 20, 100)
            if resultado >= 4.5: classificacao, fluxo, vies = "COMPRA FORTE", "FLUXO COMPRADOR", "VIÉS COMPRADOR"
            elif resultado >= 2.5: classificacao, fluxo, vies = "COMPRA MODERADA", "FLUXO COMPRADOR", "VIÉS COMPRADOR"
            elif resultado >= 1.5: classificacao, fluxo, vies = "COMPRA LEVE", "FLUXO COMPRADOR", "VIÉS COMPRADOR"
            elif resultado <= -4.5: classificacao, fluxo, vies = "VENDA FORTE", "FLUXO VENDEDOR", "VIÉS VENDEDOR"
            elif resultado <= -2.5: classificacao, fluxo, vies = "VENDA MODERADA", "FLUXO VENDEDOR", "VIÉS VENDEDOR"
            elif resultado <= -1.5: classificacao, fluxo, vies = "VENDA LEVE", "FLUXO VENDEDOR", "VIÉS VENDEDOR"
            else: classificacao, fluxo, vies = "LATERAL", "FLUXO INDEFINIDO", "MERCADO LATERAL"
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
        if st.button("← Voltar", key="voltar_adr"):
            st.session_state.modo = None
            st.rerun()
