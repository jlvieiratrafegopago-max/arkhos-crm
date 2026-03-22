import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E TEMA (ARKHOS PREMIUM)
# ==========================================
st.set_page_config(
    page_title="Arkhos CRM - Elite Strategic",
    layout="wide",
    page_icon="⚖️"
)

# Estilização High-End Arkhos (Mantendo seu CSS Original)
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #121212; }
    h1, h2, h3, p, span, label { color: #e0e0e0 !important; }
    
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
# 2. CONEXÃO COM SUPABASE
# ==========================================
def conectar_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

# ==========================================
# 3. CONTROLE DE ACESSO
# ==========================================
MINHA_CHAVE_MESTRA = "arkhos2026" 
is_admin = st.query_params.get("admin") == MINHA_CHAVE_MESTRA

# ==========================================
# 4. BARRA LATERAL (LOGO E NAVEGAÇÃO)
# ==========================================
# Usando o link do GitHub para a logo ser universal
logo_url = "https://raw.githubusercontent.com/jlvieiratrafegopago-max/arkhos-crm/main/logo_arkhos.png"
st.sidebar.image(logo_url, use_container_width=True)

st.sidebar.title("Arkhos Tech & Media")
st.sidebar.markdown("---")

if is_admin:
    st.sidebar.success("🔑 MODO ADMIN ATIVO")
    tela = st.sidebar.radio("Navegação:", ["Gerenciar CRM", "Formulário de Briefing"])
else:
    tela = "Formulário de Briefing"

# ==========================================
# 5. TELA: FORMULÁRIO DE BRIEFING (ENVIA PARA SUPABASE)
# ==========================================
if tela == "Formulário de Briefing":
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
            site = st.text_input("Site ou Instagram (URL)")
        with col2:
            faturamento = st.selectbox("Faturamento Médio Mensal", ["Até R$ 20k", "R$ 20k - R$ 100k", "Acima de R$ 100k"])
            investimento = st.selectbox("Investimento Atual em Marketing", ["Nenhum", "Até R$ 2k", "R$ 2k - R$ 10k", "Acima de R$ 10k"])

        st.subheader("2. Detalhes do Negócio")
        meta = st.text_input("Meta de Faturamento em 6 meses")
        diferencial = st.text_area("Seu principal diferencial competitivo")
        detalhes = st.text_area("Maior obstáculo para o crescimento (Detalhes)")
        
        enviar = st.form_submit_button("ENVIAR ANÁLISE ESTRATÉGICA")

        if enviar:
            if nome_lead and contato:
                supabase = conectar_supabase()
                if supabase:
                    novo_registro = {
                        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
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
                    # Comando para inserir no Banco de Dados
                    try:
                        supabase.table("leads_arkhos").insert(novo_registro).execute()
                        st.success(f"✅ Diagnóstico de '{nome_lead}' enviado com sucesso!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Erro ao salvar: {e}")
            else:
                st.warning("⚠️ Nome e Contato são obrigatórios.")

# ==========================================
# 6. TELA: GERENCIAR CRM (LÊ DO SUPABASE)
# ==========================================
elif tela == "Gerenciar CRM" and is_admin:
    st.header("📊 Inteligência de Leads & Gestão (Cloud)")
    
    supabase = conectar_supabase()
    if supabase:
        try:
            # Busca todos os dados da tabela
            resposta = supabase.table("leads_arkhos").select("*").order("data", desc=True).execute()
            dados = resposta.data
            
            if dados:
                df = pd.DataFrame(dados)
                # Remove colunas técnicas se houver (como 'id' do banco) para visualização limpa
                st.data_editor(df, use_container_width=True, hide_index=True)
                
                st.download_button(
                    label="Baixar Leads em CSV",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name="leads_arkhos_cloud.csv",
                    mime="text/csv"
                )
            else:
                st.info("Nenhum lead encontrado no banco de dados ainda.")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")

# ==========================================
# 7. RODAPÉ
# ==========================================
st.markdown("---")
st.caption("Arkhos Tech & Media © 2026 - Gestão de Dados Inteligente")
