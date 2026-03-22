import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E TEMA
# ==========================================
st.set_page_config(
    page_title="Arkhos CRM - Elite Strategic",
    layout="wide",
    page_icon="⚖️"
)

# Estilização High-End Arkhos
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #121212; }
    h1, h2, h3, p, span, label { color: #e0e0e0 !important; }
    
    /* Remove as instruções automáticas 'Press Enter' */
    [data-testid="stInputInstructions"] { display: none !important; }

    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea {
        color: #ffffff !important; 
        background-color: #333333 !important; 
        border: 1px solid #444;
    }

    div.stButton > button {
        background-color: #d4af37 !important;
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        width: 100%;
        border-radius: 8px;
        border: 2px solid #ffffff !important;
        padding: 0.6rem;
        text-transform: uppercase;
    }
    
    div.stButton > button:hover {
        background-color: #ffffff !important;
        color: #d4af37 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CONTROLE DE ACESSO
# ==========================================
MINHA_CHAVE_MESTRA = "arkhos2026" 
is_admin = st.query_params.get("admin") == MINHA_CHAVE_MESTRA

# ==========================================
# 3. FUNÇÕES DE DADOS (JSON LOCAL)
# ==========================================
DB_FILE = "dados_leads.json"

def carregar_dados():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f: json.dump([], f)
    try:
        with open(DB_FILE, "r") as f:
            conteudo = f.read()
            return json.loads(conteudo) if conteudo else []
    except: return []

def salvar_todos_dados(dados):
    with open(DB_FILE, "w") as f: json.dump(dados, f, indent=4)

# ==========================================
# 4. BARRA LATERAL (CONFIGURAÇÃO CLEAN)
# ==========================================
st.sidebar.title("Arkhos Tech & Media")
st.sidebar.markdown("---")

if is_admin:
    st.sidebar.success("🔑 MODO ADMIN ATIVO")
    tela = st.sidebar.radio("Navegação:", ["Gerenciar CRM", "Visualizar Briefing"])
else:
    tela = "Formulário de Briefing"

LISTA_STATUS = ["Novo", "Em Contato", "Reunião Agendada", "Proposta Enviada", "Contrato Assinado"]

# ==========================================
# 5. TELA: FORMULÁRIO DE BRIEFING
# ==========================================
if tela in ["Formulário de Briefing", "Visualizar Briefing"]:
    st.header("📋 Diagnóstico Estratégico Arkhos")
    
    st.subheader("1. Perfil Profissional")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        nome_lead = st.text_input("Nome do Lead / Clínica / Escritório")
    with col_p2:
        nicho_sel = st.selectbox("Nicho de Atuação", ["Advocacia", "Medicina", "Outros"])
        
        nicho_final = nicho_sel
        if nicho_sel == "Outros":
            nicho_extra = st.text_input("Qual o seu nicho profissional?")
            nicho_final = f"Outros: {nicho_extra}" if nicho_extra else "Outros"

    with st.form("form_arkhos_web", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            contato = st.text_input("WhatsApp com DDD")
        with col2:
            site = st.text_input("Site ou Instagram (URL)")

        st.subheader("2. Raio-X do Negócio")
        col3, col4 = st.columns(2)
        with col3:
            faturamento = st.selectbox("Faturamento Médio Mensal", ["Até R$ 20k", "R$ 20k - R$ 100k", "Acima de R$ 100k"])
            investimento = st.selectbox("Investimento Atual em Marketing", ["Nenhum", "Até R$ 2k", "R$ 2k - R$ 10k", "Acima de R$ 10k"])
        with col4:
            equipe = st.radio("Possui equipe comercial ou secretária?", ["Sim", "Não"], horizontal=True)
            meta = st.text_input("Meta de Faturamento em 6 meses")

        st.subheader("3. Desafios e Diferenciais")
        diferencial = st.text_area("Seu principal diferencial competitivo")
        detalhes = st.text_area("Maior obstáculo para o crescimento")
        
        enviar = st.form_submit_button("ENVIAR ANÁLISE ESTRATÉGICA")

        if enviar:
            if nome_lead and contato and detalhes:
                id_unico = int(datetime.now().timestamp())
                novo_registro = {
                    "id": id_unico,
                    "data": datetime.now().strftime("%d/%m/%Y"),
                    "nome": nome_lead, 
                    "segmento": nicho_final,
                    "contato": contato,
                    "faturamento": faturamento, 
                    "investimento": investimento,
                    "status": "Novo", 
                    "meta": meta, 
                    "site": site,
                    "diferencial": diferencial, 
                    "detalhes": detalhes
                }
                dados_atuais = carregar_dados()
                dados_atuais.append(novo_registro)
                salvar_todos_dados(dados_atuais)
                st.success(f"✅ Diagnóstico enviado com sucesso!")
            else:
                st.warning("⚠️ Preencha Nome, Contato e Obstáculo.")

# ==========================================
# 6. TELA: GERENCIAR CRM
# ==========================================
elif tela == "Gerenciar CRM" and is_admin:
    st.header("📊 Inteligência de Leads & Gestão")
    dados = carregar_dados()
    if dados:
        df = pd.DataFrame(dados)
        st.data_editor(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum registro encontrado no banco local.")
