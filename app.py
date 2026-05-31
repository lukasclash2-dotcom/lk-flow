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
    st_autorefresh(interval=60000, key="gps_refresh_unique")
    
    # A função apenas desenha o gráfico
    render_gps_mercado()
    
    # Atualiza automaticamente a cada 120 segundos
    st_autorefresh(interval=60000, key="datarefresh")
    
    # Chama o desenho do gráfico que colocamos lá no topo
    render_gps_mercado()
