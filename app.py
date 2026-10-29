import streamlit as st
import pandas as pd
from datetime import date
import os

# Configuração da página para ficar bonita e larga
st.set_page_config(page_title="Controlo de Corretivas - Aeronáutica", layout="wide")

# Título do sistema
st.title("✈️ Sistema de Controlo de Corretivas - Aeronáutica / SIL")

# Ficheiro onde os dados serão guardados (funciona como um mini banco de dados)
DATA_FILE = "dados_corretivas.csv"

# Função para carregar os dados
def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Se não existir, cria a estrutura vazia
        df = pd.DataFrame(columns=[
            "Equipamento", "Peças Orçadas", "Status Proposta", "Data Envio", 
            "Parecer SIL", "Status Compra", "Execução", "Faturamento", "Observações"
        ])
        df.to_csv(DATA_FILE, index=False)
        return df

# Função para guardar os dados
def guardar_dados(df):
    df.to_csv(DATA_FILE, index=False)

df = carregar_dados()

# --- FORMULÁRIO DE REGISTO ---
st.markdown("### 📝 Registar Nova Corretiva")
with st.form("novo_registo", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        equipamento = st.text_input("Equipamento (Ex: Ar Condicionado 12k BTU)")
        status_proposta = st.selectbox("Status da Proposta", ["Pendente", "Enviada"])
        execucao = st.selectbox("Execução do Serviço", ["Pendente", "Agendado", "Em Andamento", "Concluído"])
        
    with col2:
        pecas = st.text_input("Peças Orçadas (Ex: Compressor, Gás)")
        data_envio = st.date_input("Data de Envio", value=None)
        faturamento = st.selectbox("Faturamento (NF)", ["Pendente", "Emitida", "Paga"])
        
    with col3:
        parecer = st.selectbox("Parecer da SIL", ["Aguardando", "Aprovado", "Reprovado"])
        status_compra = st.selectbox("Status Compra (Peças)", ["Pendente", "Em cotação", "Comprado", "Entregue"])
        observacoes = st.text_input("Observações para o fiscal")

    submitted = st.form_submit_button("Adicionar Registo")
    
    if submitted and equipamento and pecas:
        # Formatar a data se existir
        data_str = data_envio.strftime("%d/%m/%Y") if data_envio else "-"
        
        # Criar novo registo
        novo_dado = pd.DataFrame([{
            "Equipamento": equipamento,
            "Peças Orçadas": pecas,
            "Status Proposta": status_proposta,
            "Data Envio": data_str,
            "Parecer SIL": parecer,
            "Status Compra": status_compra,
            "Execução": execucao,
            "Faturamento": faturamento,
            "Observações": observacoes
        }])
        
        # Juntar ao que já existe e guardar
        df = pd.concat([df, novo_dado], ignore_index=True)
        guardar_dados(df)
        st.success("Corretiva registada com sucesso!")
        st.rerun()

# --- TABELA DE ACOMPANHAMENTO ---
st.markdown("---")
st.markdown("### 📊 Acompanhamento de Corretivas")

if not df.empty:
    # Usamos o st.data_editor para permitir que você mude os status diretamente na tabela!
    df_editado = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic", # Permite apagar linhas
        column_config={
            "Status Proposta": st.column_config.SelectboxColumn(options=["Pendente", "Enviada"]),
            "Parecer SIL": st.column_config.SelectboxColumn(options=["Aguardando", "Aprovado", "Reprovado"]),
            "Status Compra": st.column_config.SelectboxColumn(options=["Pendente", "Em cotação", "Comprado", "Entregue"]),
            "Execução": st.column_config.SelectboxColumn(options=["Pendente", "Agendado", "Em Andamento", "Concluído"]),
            "Faturamento": st.column_config.SelectboxColumn(options=["Pendente", "Emitida", "Paga"]),
        }
    )
    
    # Se houver mudanças na tabela (edição de status ou exclusão), guardamos automaticamente
    if not df.equals(df_editado):
        guardar_dados(df_editado)
        st.rerun()
else:
    st.info("Nenhuma corretiva registada ainda.")
