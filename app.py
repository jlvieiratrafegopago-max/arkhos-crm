import streamlit as st
from supabase import create_client
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Arkhos CRM - Dashboard", layout="wide")

# --- FUNÇÃO PARA CONECTAR E SALVAR NO SUPABASE ---
def salvar_lead_supabase(dados):
    # O Streamlit busca as chaves automaticamente nos Secrets que você configurou
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        supabase = create_client(url, key)
        
        # Prepara o dicionário exatamente como as colunas da nossa tabela SQL
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
        
        # Envia para a tabela 'leads_arkhos' no Supabase
        supabase.table("leads_arkhos").insert(novo_lead).execute()
        return True
    except Exception as e:
        st.error(f"Erro ao conectar com o banco de dados: {e}")
        return False

# --- INTERFACE DO USUÁRIO ---
st.title("🚀 Arkhos Tech & Media - CRM de Leads")
st.subheader("Cadastro de Novo Lead (Prospect)")

with st.form("form_leads", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Nome da Empresa/Cliente")
        segmento = st.text_input("Segmento de Atuação")
        contato = st.text_input("WhatsApp / E-mail")
        site = st.text_input("Site / Redes Sociais")
        
    with col2:
        faturamento = st.selectbox("Faturamento Mensal Atual", ["R$ 0 - 5k", "R$ 5k - 20k", "R$ 20k - 50k", "Acima de 50k"])
        investimento = st.text_input("Quanto pretende investir em tráfego?")
        meta = st.text_input("Qual o principal objetivo/meta?")
        diferencial = st.text_area("Qual o diferencial do negócio?")

    detalhes = st.text_area("Observações adicionais")
    
    submit = st.form_submit_button("Cadastrar Lead na Nuvem")

if submit:
    if nome and contato:
        # Criamos o dicionário com os dados do formulário
        dados_prospect = {
            "nome": nome,
            "segmento": segmento,
            "contato": contato,
            "faturamento": faturamento,
            "investimento": investimento,
            "meta": meta,
            "site": site,
            "diferencial": diferencial,
            "detalhes": detalhes
        }
        
        # Chamamos a função de salvar
        sucesso = salvar_lead_supabase(dados_prospect)
        
        if sucesso:
            st.success(f"✅ Lead '{nome}' salvo com sucesso no banco de dados da Arkhos!")
            st.balloons()
    else:
        st.warning("⚠️ Por favor, preencha pelo menos o Nome e o Contato.")

# --- RODAPÉ ---
st.markdown("---")
st.caption("Arkhos Tech & Media © 2026 - Sistema de Gestão de Leads Profissional")
