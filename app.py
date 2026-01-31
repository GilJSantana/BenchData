import config_app
import config_data

# 1. Configura a página e obtém os filtros
filtros = config_app.setup_page()

# 2. Exibe o cabeçalho (Título e Descrição)
config_app.exibir_cabecalho()

# 3. Obtém os dados filtrados
df_filtrado = config_data.filtrar_dados(filtros)

# 4. Valida os dados e exibe o conteúdo
if config_app.validar_dados(df_filtrado):
    # Exibe as métricas (KPIs)
    config_app.exibir_metricas(df_filtrado)

    # Exibe os gráficos
    config_app.exibir_graficos(df_filtrado)

    # Exibe a tabela de dados
    config_app.exibir_tabela(df_filtrado)
