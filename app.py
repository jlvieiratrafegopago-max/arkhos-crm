import streamlit as st
from supabase import create_client
from datetime import datetime

# --- 1. CONFIGURAÇÃO DA PÁGINA (Tema Escuro e Layout) ---
st.set_page_config(
    page_title="Arkhos Tech & Media - CRM", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- 2. CONTROLE DE ACESSO ---
query_params = st.query_params
acesso_admin = query_params.get("admin") == "arkhos2026"

# --- 3. FUNÇÃO DE SALVAMENTO NO SUPABASE ---
def salvar_lead_supabase(dados):
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        supabase = create_client(url, key)
        
        novo_lead = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "nome": dados.get('nome', ''),
            "segmento": dados.get('segmento', ''),
            "contato": dados.get('contato', ''),
            "faturamento": dados.get('faturamento', ''),
            "investimento": dados.get('investimento', ''),
            "status": "Novo",
            "meta": dados.get('meta', ''),
            "site": dados.get('site', ''),
            "diferencial": dados.get('diferencial', ''),
            "detalhes": dados.get('detalhes', '')
        }
        
        supabase.table("leads_arkhos").insert(novo_lead).execute()
        return True
    except Exception as e:
        st.error(f"Erro na conexão: {e}")
        return False

# --- 4. LOGO E IDENTIDADE VISUAL ---
# Centralizando a logo no topo
logo_url = "https://raw.githubusercontent.com/jlvieiratrafegopago-max/arkhos-crm/main/logo_arkhos.png"
col_logo_1, col_logo_2, col_logo_3 = st.columns()
with col_logo_2:
    st.image(logo_url, use_container_width=True)

# --- 5. LÓGICA DE EXIBIÇÃO ---

if acesso_admin:
    # --- VISÃO DO ADMINISTRADOR (O que você vê) ---
    st.markdown("<h1 style='text-align: center;'>🚀 Painel de Gestão Arkhos</h1>", unsafe_allow_html=True)
    st.sidebar.title("Menu Arkhos")
    st.sidebar.info("Acesso Administrativo Ativo")
    st.sidebar.write("Aqui você poderá ver os leads em breve.")
else:
    # --- VISÃO DO CLIENTE (O que o cliente vê) ---
    st.markdown("<h2 style='text-align: center;'>Formulário de Diagnóstico Estratégico</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Preencha os dados abaixo para iniciarmos sua análise.</p>", unsafe_allow_html=True)

# --- FORMULÁRIO (Igual para ambos, mas salvando na nuvem) ---
with st.form("form_leads", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Nome da Empresa/Cliente")
        segmento = st.text_input("Segmento de Atuação")
        contato = st.text_input("WhatsApp / E-mail")
        site = st.text_input("Site ou Instagram")
        
    with col2:
        faturamento = st.selectbox("Faturamento Mensal", ["R$ 0 - 5k", "R$ 5k - 20k", "R$ 20k - 50k", "Acima de 50k"])
        investimento = st.text_input("Pretensão de Investimento")
        meta = st.text_input("Qual seu principal objetivo?")
        diferencial = st.text_area("Seu diferencial competitivo")

    detalhes = st.text_area("Observações Adicionais")
    
    label_botao = "Enviar Diagnóstico para Arkhos" if not acesso_admin else "Cadastrar Lead no CRM"
    submit = st.form_submit_button(label_botao)

if submit:
    if nome and contato:
        dados_prospect = {
            "nome": nome, "segmento": segmento, "contato": contato,
            "faturamento": faturamento, "investimento": investimento,
            "meta": meta, "site": site, "diferencial": diferencial, "detalhes": detalhes
        }
        if salvar_lead_supabase(dados_prospect):
            st.success(f"✅ Sucesso! Os dados foram enviados para a equipe Arkhos.")
            st.balloons()
    else:
        st.warning("⚠️ Por favor, preencha o Nome e o Contato.")

# --- RODAPÉ ---
st.markdown("---")
st.caption("Arkhos Tech & Media © 2026")
