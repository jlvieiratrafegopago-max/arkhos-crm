import streamlit as st
from supabase import create_client
from datetime import datetime

# --- 1. CONFIGURAÇÃO DA PÁGINA (DESIGN) ---
st.set_page_config(page_title="Arkhos CRM - Gestão Profissional", layout="centered")

# --- 2. LOGO DA ARKHOS (Ajuste o link se necessário) ---
# Coloque aqui o link direto da sua imagem/logo
logo_url = "https://raw.githubusercontent.com/jlvieiratrafegopago-max/arkhos-crm/main/logo_arkhos.png" 
st.image(logo_url, width=200)

# --- 3. CONTROLE DE ACESSO (O SEGREDO DO LINK) ---
query_params = st.query_params
acesso_admin = query_params.get("admin") == "arkhos2026"

# --- 4. FUNÇÃO PARA SALVAR NO SUPABASE ---
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
        st.error(f"Erro no banco: {e}")
        return False

# --- 5. LÓGICA DE EXIBIÇÃO ---
if acesso_admin:
    st.title("🚀 Arkhos Tech & Media")
    st.subheader("Painel de Captação de Leads")

    with st.form("form_leads", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome da Empresa/Cliente")
            segmento = st.text_input("Segmento de Atuação")
            contato = st.text_input("WhatsApp / E-mail")
        with col2:
            faturamento = st.selectbox("Faturamento Atual", ["R$ 0 - 5k", "R$ 5k - 20k", "R$ 20k - 50k", "Acima de 50k"])
            investimento = st.text_input("Pretensão de Investimento")
            meta = st.text_input("Principal Objetivo")
        
        site = st.text_input("Site / Redes Sociais")
        diferencial = st.text_area("Diferencial do Negócio")
        detalhes = st.text_area("Observações Adicionais")
        
        submit = st.form_submit_button("Cadastrar Lead na Nuvem")

    if submit:
        if nome and contato:
            dados_prospect = {
                "nome": nome, "segmento": segmento, "contato": contato,
                "faturamento": faturamento, "investimento": investimento,
                "meta": meta, "site": site, "diferencial": diferencial, "detalhes": detalhes
            }
            if salvar_lead_supabase(dados_prospect):
                st.success(f"✅ Lead '{nome}' enviado para o Banco de Dados!")
                st.balloons()
        else:
            st.warning("⚠️ Preencha pelo menos Nome e Contato.")

else:
    # Tela para quem não tem o link secreto
    st.error("🔒 Acesso restrito.")
    st.info("Este é um sistema interno da Arkhos Tech & Media. Por favor, utilize o link de acesso oficial.")

st.markdown("---")
st.caption("Arkhos Tech & Media © 2026")
