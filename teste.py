from supabase_py import create_client
import pandas as pd 
import streamlit as st 
import plotly.express as px

API_URL = 'https://lkoavinwvnwfmvpkvvyk.supabase.co'
API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxrb2F2aW53dm53Zm12cGt2dnlrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDgyNzYzMzQsImV4cCI6MjAyMzg1MjMzNH0.CVJSIFMoElDjkSWPdgbx6W9vxiBqcfNyblCSu9t85bY'
supabase = create_client(API_URL, API_KEY)

# Obter os dados do Supabase
response = supabase.table('Principal').select('*').execute()
data = response.data

if data:
    df = pd.DataFrame(data)
    
    # Formatar coluna 'created_at'
    df['created_at'] = pd.to_datetime(df['created_at'])

    # Extrair data e hora
    df['date'] = df['created_at'].dt.date
    df['time'] = df['created_at'].dt.time
    df['DateTime'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Configurar a página do Streamlit
    st.set_page_config(page_title="Medidor Residencial", layout='wide', initial_sidebar_state='collapsed')

    # Últimos valores
    last_value_analog_1 = df['analog_value_1'].iloc[-1]
    last_value_analog_2 = df['analog_value_2'].iloc[-1]

    # Mostrar últimos valores em uma linha acima dos gráficos
    st.write("Últimos valores:")
    st.write(f"Potenciômetro 1: {last_value_analog_1}")
    st.write(f"Potenciômetro 2: {last_value_analog_2}")

    # Dividir a página em duas colunas para os gráficos
    col1, col2 = st.columns(2)

    # Gráfico para analog_value_1
    with col1:
        st.markdown('### Potenciômetro 1')
        fig_analog_value_1 = px.line(df, x="DateTime", y="analog_value_1", title='', markers=True)
        st.plotly_chart(fig_analog_value_1, use_container_width=True)

    # Gráfico para analog_value_2
    with col2:
        st.markdown('### Potenciômetro 2')
        fig_analog_value_2 = px.line(df, x="DateTime", y="analog_value_2", title='', markers=True)
        st.plotly_chart(fig_analog_value_2, use_container_width=True)

else:
    st.error("Erro ao obter dados do Supabase")
