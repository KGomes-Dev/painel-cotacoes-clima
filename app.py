import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Configuração da página para ocupar a largura toda
st.set_page_config(page_title="Painel Integrado: Cotações e Clima", layout="wide")


st.title("📊🌧️ Painel Integrado: Cotações e Clima")
st.write("Acompanhe as cotações financeiras e a previsão do tempo lado a lado em tempo real.")

st.divider()

# -------------------------------------------------------------
# DIVISÃO DO ECRÃ EM DUAS COLUNAS PRINCIPAIS (LADO A LADO)
# -------------------------------------------------------------
col_esquerda, col_direita = st.columns(2)

# ==========================================
# COLUNA DA ESQUERDA: API DE COTAÇÕES
# ==========================================
with col_esquerda:
    st.header("💱 Cotações de Moedas")
    
    if st.button("Atualizar Cotações via API"):
        try:
            # Cabeçalhos para simular um navegador e evitar bloqueios da API na nuvem
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL'
            requisicao = requests.get(url, headers=headers, timeout=10)
            
            if requisicao.status_code == 200:
                requisicao_dic = requisicao.json()
                
                # Extração segura com tratamento de chaves (substitui hífens caso a API retorne sem eles)
                cotacao_dolar = float(requisicao_dic.get('USDBRL', {}).get('bid', 0))
                cotacao_euro = float(requisicao_dic.get('EURBRL', {}).get('bid', 0))
                cotacao_btc = float(requisicao_dic.get('BTCBRL', {}).get('bid', 0)) * 1000

                if cotacao_dolar > 0:
                    # Gravar no Excel
                    tabela = pd.read_excel('Cotações.xlsx')
                    tabela.loc[0, 'Cotação'] = cotacao_dolar
                    tabela.loc[1, 'Cotação'] = cotacao_euro
                    tabela.loc[2, 'Cotação'] = cotacao_btc
                    tabela.loc[0, 'Data Útilima Atualização'] = datetime.now()
                    
                    tabela.to_excel('Cotações.xlsx', index=False)
                    st.success("Cotações atualizadas com sucesso!")
                    st.rerun() # Atualiza a página automaticamente para mostrar os novos valores
                else:
                    st.error("A API respondeu, mas os valores vieram vazios.")
            else:
                st.error(f"Erro na API. Código de status: {requisicao.status_code}")
                
        except Exception as e:
            st.error(f"Erro ao conectar com a API: {e}")

    try:
        tabela_atual = pd.read_excel('Cotações.xlsx')
        
        # Métricas divididas em 3 colunas pequenas internas
        m1, m2, m3 = st.columns(3)
        with m1:
            val_dolar = tabela_atual.loc[tabela_atual['Moeda'] == 'Dólar', 'Cotação'].values[0]
            st.metric(label="USD", value=f"R$ {val_dolar:.2f}")
        with m2:
            val_euro = tabela_atual.loc[tabela_atual['Moeda'] == 'Euro', 'Cotação'].values[0]
            st.metric(label="EUR", value=f"R$ {val_euro:.2f}")
        with m3:
            val_btc = tabela_atual.loc[tabela_atual['Moeda'] == 'Bitcoin', 'Cotação'].values[0]
            st.metric(label="BTC", value=f"R$ {val_btc:,.2f}")

        st.subheader("Tabela de Dados")
        st.dataframe(tabela_atual, use_container_width=True)
        
        st.subheader("Gráfico Comparativo")
        grafico_dados = tabela_atual.set_index('Moeda')['Cotação']
        st.bar_chart(grafico_dados)

    except Exception as e:
        st.info("Certifique-se de que o ficheiro Excel existe no caminho indicado.")

# ==========================================
# COLUNA DA DIREITA: API DE CLIMA
# ==========================================
with col_direita:
    st.header("🌧️ Previsão do Tempo")
    
    # Entradas de coordenadas lado a lado na coluna da direita
    lat_col, lon_col = st.columns(2)
    with lat_col:
        lat = st.number_input("Latitude", value=-22.7356, format="%.4f")
    with lon_col:
        lon = st.number_input("Longitude", value=-43.3061, format="%.4f")

    if st.button("Obter Clima da Região"):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true"
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            dados = response.json()
            clima_atual = dados["current_weather"]
            
            # Exibe os resultados do clima em cartões de métrica
            c_meteo1, c_meteo2 = st.columns(2)
            with c_meteo1:
                st.metric(label="Temperatura Atual", value=f"{clima_atual['temperature']} °C")
            with c_meteo2:
                st.metric(label="Velocidade Vento", value=f"{clima_atual['windspeed']} km/h")
                
            st.success("Dados meteorológicos carregados com sucesso!")
        else:
            st.error("Erro ao conectar com a API Open-Meteo.")
