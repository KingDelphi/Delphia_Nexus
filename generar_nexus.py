import pandas as pd
import os
import json
import re

# --- CONFIGURACIÓN DE INFRAESTRUCTURA ---
ARCHIVO_LEDGER = "Truth_Ledger_Master.csv"
ARCHIVO_CAP_TABLE = "Delphia_Cap_Table.csv"
ARCHIVO_CUENTAS = "Delphia_Bank_Accounts.csv"
ARCHIVO_MERCADO = "Market_Orders.csv"
RAIZ_BOVEDAS = "Boveda_Activos"
CARPETA_CERTIFICADOS = "Certificados_Emitidos"

def inicializar_mercado():
    if not os.path.exists(ARCHIVO_MERCADO) or os.stat(ARCHIVO_MERCADO).st_size == 0:
        df = pd.DataFrame(columns=['Order_ID', 'Asset_ID', 'Vendedor', 'Acciones', 'Precio_DPX', 'Status'])
        df.to_csv(ARCHIVO_MERCADO, index=False)

def limpiar_precio_pro(valor):
    if pd.isna(valor): return 0.0
    s = str(valor).replace('$', '').replace(',', '').strip()
    try: return float(s)
    except: return 0.0

def ejecutar_nexus():
    inicializar_mercado()
    
    if not os.path.exists(ARCHIVO_LEDGER) or not os.path.exists(ARCHIVO_CAP_TABLE):
        print("[!] Error: No se encuentran los archivos del Ledger o Cap Table.")
        return

    df_ledger = pd.read_csv(ARCHIVO_LEDGER)
    df_cap = pd.read_csv(ARCHIVO_CAP_TABLE)
    
    if 'Yield_Anual_DPX' not in df_ledger.columns:
        df_ledger['Yield_Anual_DPX'] = 0.0
    
    if 'Valor_Root' not in df_ledger.columns:
        df_ledger['Valor_Root'] = "10³⁶"
        
    try:
        df_mercado = pd.read_csv(ARCHIVO_MERCADO)
    except:
        df_mercado = pd.DataFrame(columns=['Order_ID', 'Asset_ID', 'Vendedor', 'Acciones', 'Precio_DPX', 'Status'])
    
    # Mapeo de archivos reales para evitar errores de nombres largos
    mapa_cert_maestros = {}
    if os.path.exists(CARPETA_CERTIFICADOS):
        for f in os.listdir(CARPETA_CERTIFICADOS):
            if f.startswith("Certificado_DLPH-"):
                match = re.search(r"DLPH-([A-Z0-9]+)", f)
                if match: mapa_cert_maestros[match.group(1)] = f

    banco_dict = {}
    soberanos_banco = []
    if os.path.exists(ARCHIVO_CUENTAS):
        df_cuentas = pd.read_csv(ARCHIVO_CUENTAS)
        soberanos_banco = df_cuentas['Soberano'].dropna().unique().tolist()
        for _, row in df_cuentas.iterrows():
            banco_dict[row['Soberano']] = {
                'Saldo': float(row['Saldo_DPX']) if pd.notna(row['Saldo_DPX']) else 0.0,
                'Tipo': str(row['Tipo']).replace('_', ' ')
            }

    df_ledger['Precio_Num'] = df_ledger['Valor'].apply(limpiar_precio_pro)
    
    mapa_archivos = {}
    if os.path.exists(RAIZ_BOVEDAS):
        for raiz, _, archivos in os.walk(RAIZ_BOVEDAS):
            for f in archivos:
                mapa_archivos[f.lower()] = os.path.relpath(os.path.join(raiz, f)).replace("\\", "/")

    total_valor_reino = df_ledger['Precio_Num'].sum()
    total_yield_global = df_ledger['Yield_Anual_DPX'].sum() / 12
    
    soberanos_cap = df_cap['Soberano'].dropna().unique().tolist()
    soberanos_lista = sorted(list(set(soberanos_cap + soberanos_banco)))
    
    banco_json = json.dumps(banco_dict)
    mercado_json = df_mercado[df_mercado['Status'] == 'OPEN'].to_json(orient='records')
    maestros_json = json.dumps(mapa_cert_maestros)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>DELPHIA NEXUS v7.5 - CERTIFICATE RECOVERY</title>
        <style>
            :root {{ --gold: #c5a059; --dark: #0a0a0a; --accent: #00ff88; --card-bg: #121212; --danger: #ff4444; --blue: #00d4ff; --yield: #d4fb79; --root: #d400ff; }}
            body {{ background:#050505; color:white; font-family:'Segoe UI',sans-serif; margin:0; padding:20px; }}
            .header {{ text-align:center; padding-bottom:20px; margin-bottom:20px; border-bottom: 1px solid #222; }}
            .stats {{ display:flex; justify-content:center; gap:20px; margin:20px 0; flex-wrap: wrap; }}
            .stat-box {{ background:#111; padding:15px; border:1px solid #333; border-radius:8px; text-align:center; min-width:220px; }}
            .stat-val {{ font-size:24px; color:var(--gold); font-weight:bold; font-family:monospace; }}
            
            .wallet-panel {{ display:none; background:linear-gradient(145deg, #1a1a1a, #0a0a0a); border:1px solid var(--gold); border-radius:12px; padding:25px; margin-bottom:30px; text-align:center; box-shadow: 0 0 30px rgba(197,160,89,0.15); animation: fadeIn 0.5s ease; }}
            .wallet-name {{ color:var(--gold); margin-top:0; font-size:24px; letter-spacing:4px; text-transform:uppercase; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 20px; }}
            .wallet-grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:20px; margin-bottom:20px; justify-content: center; }}
            .wallet-item {{ background: rgba(255,255,255,0.02); padding: 15px; border-radius: 8px; border: 1px solid #222; }}
            .wallet-label {{ font-size:9px; color:#888; letter-spacing:1px; margin-bottom:8px; font-weight:bold; text-transform:uppercase; }}
            .wallet-value {{ font-size:18px; color:#fff; font-family:monospace; font-weight:bold; }}
            
            .market-section {{ background: rgba(0, 212, 255, 0.05); border: 1px solid var(--blue); border-radius: 12px; padding: 20px; margin-bottom: 30px; display:none; animation: fadeIn 0.5s ease; }}
            .market-title {{ color: var(--blue); text-transform: uppercase; letter-spacing: 4px; font-size: 14px; margin-bottom: 20px; font-weight: bold; border-bottom: 1px solid rgba(0,212,255,0.2); padding-bottom: 10px; }}
            .market-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }}
            .market-item {{ background: #000; border: 1px solid #222; padding: 12px; border-radius: 8px; display: flex; align-items: center; gap: 15px; }}
            .market-item img {{ width: 50px; height: 50px; object-fit: cover; border-radius: 4px; }}

            .controls {{ display:flex; justify-content:center; gap:15px; margin-bottom:40px; background:#111; padding:20px; border-radius:12px; border:1px solid #333; }}
            input, select {{ background:#000; color:white; border:1px solid #444; padding:12px; border-radius:6px; outline:none; }}
            
            .grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:25px; }}
            .card {{ background:var(--card-bg); border:1px solid #222; border-radius:12px; padding:15px; display:flex; flex-direction:column; position:relative; min-height: 550px; transition: 0.3s; }}
            .card:hover {{ border-color: #444; }}
            .card.selected {{ border-color: var(--accent); box-shadow: 0 0 15px rgba(0,255,136,0.2); }}
            
            .yield-badge {{ position:absolute; top:-10px; right:15px; background: #000; border: 1px solid var(--yield); color: var(--yield); padding: 2px 10px; border-radius: 4px; font-size: 10px; font-weight: bold; z-index: 11; }}
            .sale-tag {{ position:absolute; top:-10px; left:15px; background:var(--blue); color:black; padding:2px 10px; border-radius:4px; font-size:10px; font-weight:bold; z-index:11; }}
            .colateral-check {{ position:absolute; top:20px; right:15px; transform:scale(1.5); z-index:10; cursor:pointer; accent-color: var(--accent); display:none; }}

            .media-container {{ width:100%; height:220px; background:#000; border-radius:8px; overflow:hidden; display:flex; align-items:center; justify-content:center; margin-bottom:12px; border:1px solid #222; position:relative; }}
            .media-container img {{ width:100%; height:100%; object-fit:cover; }}
            .media-container audio {{ width:90%; filter: invert(100%) hue-rotate(180deg); }}
            .media-container iframe {{ width:100%; height:100%; border:none; }}
            
            .card-title {{ font-size:16px; font-weight:bold; color:#fff; margin-bottom: 2px; min-height:40px; display:flex; align-items:center; line-height:1.2; }}
            .price {{ color:var(--accent); font-size:18px; font-weight:bold; font-family:monospace; display:inline-block; margin-right: 10px; }}
            .root-val {{ color: var(--root); font-size: 11px; font-family: monospace; letter-spacing: 1px; display:inline-block; text-shadow: 0 0 8px rgba(212,0,255,0.4); }}
            
            .cap-table {{ background:rgba(0,0,0,0.4); padding:10px; border-radius:6px; border-left:3px solid var(--gold); margin:10px 0; font-size:11px; flex-grow: 1; }}
            .cap-row {{ display:flex; justify-content:space-between; margin-bottom:3px; }}
            .btn-action {{ background:transparent; border:1px solid var(--gold); color:var(--gold); padding:10px; text-align:center; border-radius:4px; text-decoration:none; font-size:11px; font-weight:bold; margin-top: 5px; cursor:pointer; transition:0.2s; }}
            .btn-cert {{ display: block; width: 100%; box-sizing: border-box; }}
            .btn-action:hover {{ background:var(--gold); color:black; }}
            .sell-panel {{ background:rgba(0, 212, 255, 0.1); border:1px solid var(--blue); padding:10px; border-radius:6px; margin-top:10px; display:none; }}
            
            @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1 style="letter-spacing:15px; color:var(--gold); margin-bottom:5px;">D E L P H I A</h1>
            <div style="font-size:11px; color:#666; letter-spacing:4px; margin-bottom:20px;">SISTEMA BURSÁTIL Y LEDGER INMUTABLE</div>
            <div class="stats">
                <div class="stat-box"><div>VALOR TOTAL REINO</div><div class="stat-val">${total_valor_reino:,.2f}</div></div>
                <div class="stat-box"><div>YIELD GLOBAL MENSUAL</div><div class="stat-val" style="color:var(--yield);">{total_yield_global:,.2f} DPX</div></div>
                <div class="stat-box" style="border:1px solid var(--accent);"><div id="wealthLabel">RIQUEZA FILTRADA</div><div class="stat-val" id="wealthVal">$0.00</div></div>
            </div>
        </div>

        <div id="walletPanel" class="wallet-panel">
            <h2 id="walletName" class="wallet-name">-</h2>
            <div class="wallet-grid">
                <div class="wallet-item">
                    <div class="wallet-label">SALDO BANCARIO</div>
                    <div id="walletSaldo" class="wallet-value text-accent">0.00 DPX</div>
                </div>
                <div class="wallet-item">
                    <div class="wallet-label">VALOR EN ACTIVOS</div>
                    <div id="walletWealth" class="wallet-value text-gold">$0.00</div>
                </div>
                <div class="wallet-item" style="border: 1px solid var(--accent); background: rgba(0, 255, 136, 0.05);" id="itemPoder">
                    <div class="wallet-label" id="walletPoderLabel" style="color:var(--accent);">NET WORTH (PODER)</div>
                    <div id="walletPoder" class="wallet-value" style="color:var(--accent); font-size:22px;">$0.00</div>
                </div>
                <div class="wallet-item" id="itemYield">
                    <div class="wallet-label">RENTA PASIVA PROPIA</div>
                    <div id="walletYield" class="wallet-value" style="color:var(--yield);">0.00 DPX / mes</div>
                </div>
                <div class="wallet-item" id="itemLTV">
                    <div class="wallet-label">CAPACIDAD CREDITICIA</div>
                    <div id="walletLTV" class="wallet-value">0.00 DPX</div>
                </div>
            </div>
            
            <div id="creditConsole" style="border-top: 1px dashed #444; padding-top: 15px;">
                <div class="wallet-label" style="color:var(--gold); margin-bottom:10px;">🏦 GESTIÓN DE COLATERAL</div>
                <div class="wallet-value" style="font-size:14px; margin-bottom:15px;">SELECCIONADO: <span id="creditTotal" style="color:var(--accent)">0.00</span> DPX</div>
                <button id="btnRequestCredit" class="btn-action" style="padding:10px 30px; margin: 0 auto; display: block;" disabled onclick="generarOrden()">SOLICITAR CRÉDITO</button>
            </div>
        </div>

        <div id="marketSection" class="market-section">
            <div class="market-title">🏛️ DELPHIA ASSET EXCHANGE</div>
            <div id="marketGrid" class="market-grid"></div>
        </div>

        <div class="controls">
            <input type="text" id="search" placeholder="🔍 Buscar activo..." oninput="update()">
            <select id="sortOrder" onchange="update()">
                <option value="name_asc">🔤 Nombre</option>
                <option value="price_desc">💰 Mayor Valor</option>
                <option value="price_asc">📉 Menor Valor</option>
            </select>
            <select id="sobFilter" onchange="update()">
                <option value="ALL">🏛️ Ver Todo el Reino</option>
                {"".join([f'<option value="{s}">{s}</option>' for s in soberanos_lista])}
            </select>
        </div>

        <div class="grid" id="mainGrid">
    """

    for _, row in df_ledger.iterrows():
        a_id = str(row['Asset_ID']).replace("DLPH-", "")
        nombre = str(row['Nombre'])
        v_num = row['Precio_Num']
        t_shares = int(row['Total_Shares'])
        v_root = str(row.get('Valor_Root', '10³⁶'))
        
        y_per_share = (float(row.get('Yield_Anual_DPX', 0)) / 12) / t_shares if t_shares > 0 else 0
        es_colateral = "COLATERAL" in str(row.get('Status', '')).upper()
        
        full_id = f"DLPH-{a_id}"
        owners_data = df_cap[df_cap['Asset_ID'] == full_id]
        if owners_data.empty: owners_data = df_cap[df_cap['Asset_ID'] == a_id]

        cap_rows_html = ""
        owners_dict = {}
        for _, o in owners_data.iterrows():
            owners_dict[o['Soberano']] = int(o['Acciones'])
            cap_rows_html += f'<div class="cap-row"><span>{o["Soberano"]}</span><span>{o["Acciones"]} sh</span></div>'

        # Preview Multimedia
        n_clean = os.path.splitext(nombre.lower())[0]
        media_html = '<div style="color:#444; font-size:11px;">[ Sin Preview ]</div>'
        encontrado = False
        for ext in [".jpeg", ".jpg", ".png", ".webp", ".mp3", ".wav", ".pdf"]:
            file_to_check = (n_clean + ext).lower()
            if file_to_check in mapa_archivos:
                path = mapa_archivos[file_to_check]
                if ext in [".jpeg", ".jpg", ".png", ".webp"]:
                    media_html = f'<img src="{path}" loading="lazy">'
                elif ext in [".mp3", ".wav"]:
                    media_html = f'<audio controls><source src="{path}" type="audio/mpeg"></audio>'
                elif ext == ".pdf":
                    media_html = f'<iframe src="{path}#toolbar=0"></iframe>'
                encontrado = True
                break
        
        if not encontrado and nombre.lower() in mapa_archivos:
            path = mapa_archivos[nombre.lower()]
            if path.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                media_html = f'<img src="{path}" loading="lazy">'
            elif path.lower().endswith(('.mp3', '.wav')):
                media_html = f'<audio controls><source src="{path}" type="audio/mpeg"></audio>'
            elif path.lower().endswith('.pdf'):
                media_html = f'<iframe src="{path}#toolbar=0"></iframe>'

        yield_badge = f'<div class="yield-badge">💎 {y_per_share:.2f} DPX/sh</div>' if y_per_share > 0 else ''

        html_content += f"""
            <div class="card" id="card-{a_id}" data-name="{nombre.lower()}" data-price="{v_num}" data-shares="{t_shares}" data-yield="{y_per_share}" data-cap='{json.dumps(owners_dict)}' data-id="{a_id}" data-rawname="{nombre}">
                <div id="tag-{a_id}" class="sale-tag" style="display:none;">🏷️ EN VENTA</div>
                {yield_badge}
                <input type="checkbox" class="colateral-check" id="check-{a_id}" onchange="toggleSelect('{a_id}')" data-val="{v_num * 0.5}" {"disabled" if es_colateral else ""}>
                
                <div class="media-container">{media_html}</div>
                <div class="card-info" style="margin-bottom: 10px;">
                    <span style="font-size:9px; color:var(--gold); text-transform:uppercase;">{row['Categoria']}</span>
                    <div class="card-title">{nombre} {"🔒" if es_colateral else ""}</div>
                    <div>
                        <span class="price">${v_num:,.2f}</span>
                        <span class="root-val">⚛️ ROOT: {v_root} Φ</span>
                    </div>
                </div>
                <div class="cap-table">{cap_rows_html}</div>
                
                <button id="btn-{a_id}" class="btn-action btn-cert" onclick="desplegarCertificado('{a_id}')">CARGANDO...</button>
                
                <div id="sell-ui-{a_id}" class="sell-panel">
                    <input type="number" id="price-in-{a_id}" placeholder="Precio DPX" style="width:60%; padding:5px; background:black; border:1px solid var(--blue); color:white;">
                    <button class="btn-action" style="padding:5px 10px; border-color:var(--blue); color:var(--blue);" onclick="crearVenta('{a_id}')">VENDER</button>
                </div>
            </div>
        """

    html_content += f"""
        </div>
        <script>
            const bancoData = {banco_json};
            const mercadoData = {mercado_json};
            const mapaMaestros = {maestros_json};
            let selectedAssets = [];

            // FUNCIÓN PARA ABRIR HTML EN NUEVO TAB (BASADO EN TU IMAGEN DE ARCHIVOS)
            function desplegarCertificado(id) {{
                const sob = document.getElementById('sobFilter').value;
                const folder = "Certificados_Emitidos/";
                let path = "";

                if(sob === "ALL") {{
                    // Patrón Maestro: Certificado_DLPH-[ID]_[Nombre].html
                    const file = mapaMaestros[id];
                    if(file) path = folder + file;
                    else alert("Certificado Maestro no encontrado para DLPH-" + id);
                }} else {{
                    // Patrón Título: Titulo_[Soberano]_DLPH-[ID].html
                    path = folder + "Titulo_" + sob + "_DLPH-" + id + ".html";
                }}
                
                if(path) window.open(path, '_blank');
            }}

            function toggleSelect(id) {{
                const check = document.getElementById('check-' + id);
                const card = document.getElementById('card-' + id);
                if(check.checked) {{ selectedAssets.push(id); card.classList.add('selected'); }}
                else {{ selectedAssets = selectedAssets.filter(i => i !== id); card.classList.remove('selected'); }}
                let t = 0; selectedAssets.forEach(i => t += parseFloat(document.getElementById('check-'+i).dataset.val));
                document.getElementById('creditTotal').innerText = t.toLocaleString();
                document.getElementById('btnRequestCredit').disabled = selectedAssets.length === 0;
            }}

            function crearVenta(id) {{
                const p = document.getElementById('price-in-'+id).value;
                const sob = document.getElementById('sobFilter').value;
                if(!p) return alert("Ingresa un precio.");
                alert("EJECUTA EN TERMINAL:\\n\\npython3 -c \\"import motor_p2p; motor_p2p.crear_orden('DLPH-${{id}}', '${{sob}}', ${{p}})\\"");
            }}

            function comprarActivo(orderId) {{
                const sob = document.getElementById('sobFilter').value;
                if(sob === 'ALL') return alert("Selecciona un Soberano para comprar.");
                alert("EJECUTA EN TERMINAL:\\n\\npython3 -c \\"import motor_p2p; motor_p2p.ejecutar_compra('${{orderId}}', '${{sob}}')\\"");
            }}

            function generarOrden() {{
                const sob = document.getElementById('sobFilter').value;
                const idsString = selectedAssets.map(id => `'DLPH-${{id}}'`).join(", ");
                alert("EJECUTA EN TERMINAL:\\n\\npython3 -c \\"import procesar_credito; procesar_credito.otorgar_credito('${{sob}}', [${{idsString}}])\\"");
            }}

            function update() {{
                const term = document.getElementById('search').value.toLowerCase();
                const sob = document.getElementById('sobFilter').value;
                const sort = document.getElementById('sortOrder').value;
                const cards = Array.from(document.getElementsByClassName('card'));
                
                // Aplicar Sorting
                cards.sort((a, b) => {{
                    if(sort === 'name_asc') return a.dataset.rawname.localeCompare(b.dataset.rawname);
                    if(sort === 'price_desc') return b.dataset.price - a.dataset.price;
                    if(sort === 'price_asc') return a.dataset.price - b.dataset.price;
                }});
                const grid = document.getElementById('mainGrid');
                cards.forEach(c => grid.appendChild(c));

                let count = 0, wealthTotal = 0, yieldUser = 0;
                
                // Actualizar Market
                const marketGrid = document.getElementById('marketGrid');
                marketGrid.innerHTML = "";
                const orders = mercadoData.filter(o => o.Vendedor !== sob);
                orders.forEach(o => {{
                    const c = cards.find(card => "DLPH-"+card.dataset.id === o.Asset_ID || card.dataset.id === o.Asset_ID);
                    if(c) {{
                        marketGrid.innerHTML += `
                            <div class="market-item">
                                <div style="flex-grow:1">
                                    <div style="font-size:12px; font-weight:bold;">${{c.dataset.rawname}}</div>
                                    <div style="font-size:10px; color:var(--blue);">${{o.Precio_DPX}} DPX</div>
                                </div>
                                <button class="btn-action" style="border-color:var(--blue); color:var(--blue);" onclick="comprarActivo('${{o.Order_ID}}')">COMPRAR</button>
                            </div>`;
                    }}
                }});
                document.getElementById('marketSection').style.display = orders.length ? 'block' : 'none';

                cards.forEach(c => {{
                    const cap = JSON.parse(c.dataset.cap);
                    const isVisible = c.dataset.name.includes(term) && (sob === 'ALL' || cap.hasOwnProperty(sob));
                    c.style.display = isVisible ? 'flex' : 'none';
                    
                    if(isVisible) {{
                        count++;
                        const price = parseFloat(c.dataset.price);
                        if(sob === 'ALL') {{
                            wealthTotal += price;
                            document.getElementById('btn-' + c.dataset.id).innerText = "📄 CERTIFICADO MAESTRO";
                        }} else {{
                            const uSh = cap[sob];
                            wealthTotal += (uSh / parseInt(c.dataset.shares)) * price;
                            yieldUser += (uSh * parseFloat(c.dataset.yield));
                            document.getElementById('btn-' + c.dataset.id).innerText = "📜 TÍTULO DE PROPIEDAD";
                        }}
                    }}
                    
                    const esDueno = sob !== 'ALL' && cap.hasOwnProperty(sob);
                    const order = mercadoData.find(o => o.Asset_ID === "DLPH-"+c.dataset.id || o.Asset_ID === c.dataset.id);
                    document.getElementById('sell-ui-'+c.dataset.id).style.display = (esDueno && !order) ? 'block' : 'none';
                    document.getElementById('check-'+c.dataset.id).style.display = (esDueno && !order) ? 'block' : 'none';
                    document.getElementById('tag-'+c.dataset.id).style.display = order ? 'block' : 'none';
                }});

                document.getElementById('wealthVal').innerText = '$' + wealthTotal.toLocaleString();
                const wp = document.getElementById('walletPanel');
                
                if(sob === 'ALL') {{
                    wp.style.display = 'none';
                }} else {{
                    wp.style.display = 'block';
                    const bank = bancoData[sob] || {{Saldo:0}};
                    document.getElementById('walletName').innerText = sob;
                    document.getElementById('walletSaldo').innerText = bank.Saldo.toLocaleString() + " DPX";
                    document.getElementById('walletWealth').innerText = "$" + wealthTotal.toLocaleString();
                    document.getElementById('walletPoder').innerText = "$" + (bank.Saldo + wealthTotal).toLocaleString();
                    
                    if(sob === 'Boveda_Arquitecto') {{
                        document.getElementById('itemYield').style.display = 'none';
                        document.getElementById('itemLTV').style.display = 'none';
                        document.getElementById('creditConsole').style.display = 'none';
                        document.getElementById('walletPoderLabel').innerText = 'LIQUIDEZ RESPALDO (M0)';
                    }} else {{
                        document.getElementById('itemYield').style.display = 'block';
                        document.getElementById('itemLTV').style.display = 'block';
                        document.getElementById('creditConsole').style.display = 'block';
                        document.getElementById('walletPoderLabel').innerText = 'NET WORTH (PODER)';
                        document.getElementById('walletYield').innerText = yieldUser.toLocaleString(undefined, {{minimumFractionDigits: 2}}) + " DPX / mes";
                        document.getElementById('walletLTV').innerText = (wealthTotal * 0.5).toLocaleString() + " DPX";
                    }}
                }}
            }}
            update();
        </script>
    </body></html>
    """
    with open("NEXUS_DASHBOARD.html", "w", encoding="utf-8") as f: f.write(html_content)
    print("[✔] NEXUS v7.5: Despliegue de certificados HTML activado y UI preservada.")

if __name__ == "__main__": ejecutar_nexus()