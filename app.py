import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 1. Configuração da Página
st.set_page_config(page_title="Otimizador de Fretes Marítimos", layout="wide")

# --- INCLUSÃO DA IMAGEM ---
try:
    st.image("baixados.png", width=250)
except:
    pass # Ignora se a imagem não existir

st.title("🚢 Otimizador de Fretes - Maritimo")
st.markdown("Análise inteligente de custos e tempos logísticos.")

# 2. Upload do Arquivo CSV
file = st.sidebar.file_uploader("Suba a sua planilha CSV", type=["csv"])

if file:
    try:
        # Leitura e Limpeza
        df = pd.read_csv(file, sep=None, engine='python', encoding='latin-1')
        df.columns = df.columns.str.strip()

        # 3. Verificação de Colunas
        cols_req = ['Porto Origem', 'Porto de Destino', 'Armador', 'Frete', 'Transittime', 'Fretime']
        cols_missing = [c for c in cols_req if c not in df.columns]

        if not cols_missing:
            # --- ADIÇÃO: FILTRO DE ORIGEM ---
            opcoes_origem = sorted(df['Porto Origem'].dropna().unique().astype(str))
            origem_sel = st.sidebar.selectbox("Selecione o Porto de Origem", opcoes_origem)

            # --- FILTRO DE DESTINO (Filtrado pela Origem selecionada) ---
            df_filtrado_origem = df[df['Porto Origem'].astype(str) == origem_sel]
            opcoes_dest = sorted(df_filtrado_origem['Porto de Destino'].dropna().unique().astype(str))
            dest_sel = st.sidebar.selectbox("Selecione o Porto de Destino", opcoes_dest)

            # Filtragem Final
            df_f = df_filtrado_origem[df_filtrado_origem['Porto de Destino'].astype(str) == dest_sel].copy()

            if not df_f.empty:
                # 5. Tratamento Numérico
                for col in ['Frete', 'Transittime', 'Fretime']:
                    df_f[col] = pd.to_numeric(df_f[col], errors='coerce')
                
                df_f = df_f.dropna(subset=['Frete', 'Transittime', 'Fretime'])

                if len(df_f) > 1:
                    scaler = MinMaxScaler()
                    df_f['n_P'] = 1 - scaler.fit_transform(df_f[['Frete']])
                    df_f['n_TT'] = 1 - scaler.fit_transform(df_f[['Transittime']])
                    df_f['n_FT'] = scaler.fit_transform(df_f[['Fretime']])
                    
                    # Cálculo Score 0-100
                    df_f['Score'] = ((df_f['n_P']*0.5) + (df_f['n_TT']*0.4) + (df_f['n_FT']*0.1)) * 100
                else:
                    df_f['Score'] = 100.0

                # 6. Top 3 e Formatação
                top_3 = df_f.sort_values(by='Score', ascending=False).head(3).reset_index(drop=True)

                def colorir(row):
                    if row.name == 0:
                        return ['background-color: #d4edda; color: #155724; font-weight: bold'] * len(row)
                    return [''] * len(row)

                def fmt_brl(v):
                    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

                # Gerar Tabela Estilizada
                col_final = ['Porto Origem', 'Armador', 'Frete', 'Transittime', 'Fretime', 'Score']
                estilo = top_3[col_final].style.apply(colorir, axis=1).format({
                    'Frete': fmt_brl,
                    'Transittime': "{:.0f}",
                    'Fretime': "{:.0f}",
                    'Score': "{:.2f}"
                })

                st.subheader(f"📍 Melhores opções de {origem_sel} para {dest_sel}")
                st.table(estilo)
                
                res_armador = top_3.iloc[0]['Armador']
                st.success(f"✅ Melhor opção técnica: **{res_armador}**")
            else:
                st.warning("Nenhuma cotação encontrada para esta rota.")
        else:
            st.error(f"Faltam colunas: {cols_missing}")

    except Exception as e:
        st.error(f"Erro no processamento: {e}")
else:

    st.info("👋 Por favor, suba o arquivo CSV na barra lateral.")
