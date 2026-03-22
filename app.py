import streamlit as st
from supabase import create_client
from datetime import datetime

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Arkhos CRM - Gestão de Leads", layout="wide", initial_sidebar_state="expanded")

# --- 2. CONTROLE DE ACESSO ---
query_params = st.query_params
acesso_admin = query_params.get("admin") == "arkhos2026"

# --- 3. FUNÇÃO DE CONEXÃO COM SUPABASE ---
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
        st.error(f"Erro na conexão com o banco: {e}")
        return False

# --- 4. VERIFICAÇÃO DE ACESSO ---
if acesso_admin:
    # --- BARRA LATERAL (SIDEBAR) REATIVADA ---
    with st.sidebar:
        # Coloque o link correto da sua logo aqui
        logo_url = "https://raw.githubusercontent.com/jlvieiratrafegopago-max/arkhos-crm/main/logo_arkhos.png"
        st.image(logo_url, use_container_width=True)
        st.markdown("---")
        st.title("Menu Arkhos")
        menu = st.radio("Navegação", ["Novo Lead", "Dashboard (Em breve)", "Configurações"])
        st.info("Logado como Administrador")

    # --- CONTEÚDO PRINCIPAL ---
    if menu == "Novo Lead":
        st.title("🚀 Arkhos Tech & Media")
        st.subheader("Captura Profissional de Leads")
        
        with st.form("form_leads", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome da Empresa/Cliente")
                segmento = st.text_input("Segmento de Atuação")
                contato = st.text_input("WhatsApp / E-mail")
                site = st.text_input("Site / Redes Sociais")
                
            with col2:
                faturamento = st.selectbox("Faturamento Atual", ["R$ 0 - 5k", "R$ 5k - 20k", "R$ 20k - 50k", "Acima de 50k"])
                investimento = st.text_input("Investimento em Tráfego")
                meta = st.text_input("Principal Meta")
                diferencial = st.text_area("Diferencial Competitivo")

            detalhes = st.text_area("Notas Adicionais")
            
            submit = st.form_submit_button("Finalizar e Salvar no Banco")

        if submit:
            if nome and contato:
                dados_prospect = {
                    "nome": nome, "segmento": segmento, "contato": contato,
                    "faturamento": faturamento, "investimento": investimento,
                    "meta": meta, "site": site, "diferencial": diferencial, "detalhes": detalhes
                }
                if salvar_lead_supabase(dados_prospect):
                    st.success(f"✅ Lead '{nome}' registrado com sucesso!")
                    st.balloons()
            else:
                st.warning("⚠️ Nome e Contato são obrigatórios.")

    # --- RODAPÉ ---
    st.markdown("---")
    st.caption("Arkhos Tech & Media © 2026 - Ibirité, MG")

else:
    # TELA DE BLOQUEIO
    st.warning("🔒 Acesso Restrito à Arkhos Tech & Media.")
    st.info("Por favor, acesse através do link de administrador configurado.")
