import streamlit as st
import plotly.express as px
from config_data import anos, senioridade, empresas, contrato


def setup_page():
    """Configura a página e a barra lateral de filtros."""
    # Definição da página
    st.set_page_config(
        page_title='Dashboard de Salários na Área de Dados',
        page_icon='📊',
        layout="wide"
    )

    # Barra lateral
    st.sidebar.header('🔍 Filtros')

    # Filtro anos.
    anos_disponiveis = anos()
    anos_selecionados = st.sidebar.multiselect('Ano', anos_disponiveis, default=anos_disponiveis)

    # Filtro senioridade.
    senioridade_disponiveis = senioridade()
    senioridade_selecionada = st.sidebar.multiselect('Senioridade', senioridade_disponiveis,
                                                     default=senioridade_disponiveis)

    # Filtro contrato.
    contrato_disponiveis = contrato()
    contrato_selecionado = st.sidebar.multiselect('Contrato', contrato_disponiveis, default=contrato_disponiveis)

    # Filtro empresas.
    empresas_disponiveis = empresas()
    empresas_selecionadas = st.sidebar.multiselect('Empresa', empresas_disponiveis, default=empresas_disponiveis)

    return {
        "anos": anos_selecionados,
        "senioridade": senioridade_selecionada,
        "contrato": contrato_selecionado,
        "empresas": empresas_selecionadas
    }


def exibir_cabecalho():
    """Exibe o título e a descrição inicial do dashboard."""
    st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
    st.markdown(
        "Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")


def exibir_metricas(df):
    """Exibe as métricas principais (KPIs) baseadas no DataFrame filtrado."""
    st.subheader("Métricas gerais (Salário anual em USD)")

    if df.empty:
        return

    # Cálculos das métricas
    salario_medio = df['usd'].mean()
    salario_maximo = df['usd'].max()
    total_registros = len(df)
    # Pega o cargo mais comum (mode() retorna uma série, pegamos o primeiro item)
    cargo_mais_frequente = df['cargo'].mode()[0] if not df['cargo'].empty else "N/A"

    # Exibição em colunas
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Salário médio", f"${salario_medio:,.0f}")
    col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
    col3.metric("Total de registros", f"{total_registros:,}")
    col4.metric("Cargo mais frequente", cargo_mais_frequente)


def exibir_graficos(df):
    """Exibe os gráficos de análise visual."""
    st.divider()
    st.subheader("📊 Análises Visuais")

    # --- Primeira Linha de Gráficos ---
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        # Top 10 cargos por salário médio
        top_cargos = df.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)

    with col_graf2:
        # Distribuição de salários (Histograma)
        grafico_hist = px.histogram(
            df,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)

    # --- Segunda Linha de Gráficos ---
    col_graf3, col_graf4 = st.columns(2)

    with col_graf3:
        # Proporção dos tipos de trabalho (Pizza/Donut)
        remoto_contagem = df['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)

    with col_graf4:
        # Mapa de salários (Filtro específico para Data Scientist)
        df_ds = df[df['cargo'] == 'Data Scientist']

        if not df_ds.empty:
            media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
            grafico_paises = px.choropleth(
                media_ds_pais,
                locations='residencia_iso3',
                color='usd',
                color_continuous_scale='rdylgn',
                title='Salário médio de Cientista de Dados por país',
                labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'}
            )
            grafico_paises.update_layout(title_x=0.1)
            st.plotly_chart(grafico_paises, use_container_width=True)
        else:
            st.info("⚠️ Não há dados de 'Data Scientist' nos filtros atuais para gerar o mapa.")


def exibir_tabela(df):
    """Exibe a tabela de dados detalhados."""
    st.divider()
    st.subheader("📋 Dados Detalhados")
    st.write(f"Mostrando {len(df)} registros encontrados.")
    # use_container_width faz a tabela ocupar a largura total
    st.dataframe(df, use_container_width=True)


def validar_dados(df):
    """
    Valida se o DataFrame filtrado possui dados para exibição.
    Retorna True se válido, False caso contrário.
    """
    if df.empty:
        st.warning("⚠️ Nenhum dado encontrado com a combinação de filtros selecionada.")
        st.info("Tente ajustar os filtros na barra lateral para obter resultados.")
        return False

    return True
