import streamlit as st
from supabase import create_client
from datetime import datetime

# --- 1. CONFIGURAÇÃO DA PÁGINA (Tema e Layout) ---
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
        st.error(f"Erro na conexão com o banco de dados: {e}")
        return False

# --- 4. LOGO E IDENTIDADE VISUAL ---
# Centralizando a logo no topo com 3 colunas (Corrigido aqui!)
col_logo_1, col_logo_2, col_logo_3 = st.columns()
with col_logo_2:
    # Link da sua logo no GitHub
    logo_url = "https://raw.githubusercontent.com/jlvieiratrafegopago-max/arkhos-crm/main/logo_arkhos.png"
    st.image(logo_url, use_container_width=True)

# --- 5. LÓGICA DE EXIBIÇÃO ---

if acesso_admin:
    # --- VISÃO DO ADMINISTRADOR (Você acessando com ?admin=arkhos2026) ---
    st.markdown("<h1 style='text-align: center; color: #FFD700;'>🚀 Painel de Gestão Arkhos</h1>", unsafe_allow_html=True)
    st.sidebar.title("Menu Administrativo")
    st.sidebar.success("Conectado como Arkhos Admin")
    st.sidebar.markdown("---")
    st.sidebar.write("Os leads cadastrados estão sendo enviados para o seu banco no Supabase.")
else:
    # --- VISÃO DO CLIENTE (O que o cliente vê no link normal) ---
    st.markdown("<h2 style='text-align: center;'>Formulário de Diagnóstico Estratégico</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cccccc;'>Responda brevemente para iniciarmos sua análise personalizada.</p>", unsafe_allow_html=True)

# --- 6. FORMULÁRIO DE CAPTAÇÃO ---
with st.form("form_leads", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Nome da Empresa/Cliente")
        segmento = st.text_input("Segmento de Atuação")
        contato = st.text_input("WhatsApp / E-mail")
        site = st.text_input("Site ou Perfil Social")
        
    with col2:
        faturamento = st.selectbox("Faturamento Mensal Atual", ["R$ 0 - 5k", "R$ 5k - 20k", "R$ 20k - 50k", "Acima de 50k"])
        investimento = st.text_input("Quanto pretende investir?")
        meta = st.text_input("Principal Objetivo / Meta")
        diferencial = st.text_area("Seu Diferencial no Mercado")

    detalhes = st.text_area("Informações Adicionais (Opcional)")
    
    # Texto do botão muda conforme o acesso
    texto_botao = "Enviar para Consultoria Arkhos" if not acesso_admin else "Cadastrar Lead no Banco de Dados"
    submit = st.form_submit_button(texto_botao)

if submit:
    if nome and contato:
        dados_prospect = {
            "nome": nome, "segmento": segmento, "contato": contato,
            "faturamento": faturamento, "investimento": investimento,
            "meta": meta, "site": site, "diferencial": diferencial, "detalhes": detalhes
        }
        # Chamada para o Supabase
        if salvar_lead_supabase(dados_prospect):
            st.success(f"✅ Recebemos seus dados, {nome}! Nossa equipe entrará em contato em breve.")
            st.balloons()
    else:
        st.warning("⚠️ Atenção: Nome e Contato são obrigatórios para prosseguirmos.")

# --- RODAPÉ ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888888;'>Arkhos Tech & Media © 2026 | Inteligência em Tráfego e Dados</p>", unsafe_allow_html=True)
