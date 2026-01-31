import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
import sys
import os

# Adiciona o diretório raiz ao path para conseguir importar os módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config_data
import config_app

# --- Fixtures (Dados de Exemplo) ---
@pytest.fixture
def sample_df():
    """Cria um DataFrame fictício para testes isolados."""
    data = {
        'ano': [2023, 2024, 2025, 2025],
        'senioridade': ['Junior', 'Senior', 'Senior', 'Lead'],
        'contrato': ['Integral', 'Integral', 'PJ', 'Integral'],
        'empresa': ['Empresa A', 'Empresa B', 'Empresa A', 'Empresa C'],
        'usd': [50000, 100000, 120000, 150000],
        'cargo': ['Data Analyst', 'Data Scientist', 'Data Scientist', 'Data Engineer'],
        'remoto': ['remoto', 'hibrido', 'remoto', 'presencial'],
        'residencia_iso3': ['BRA', 'USA', 'USA', 'GBR']
    }
    return pd.DataFrame(data)

# --- Testes do Model (config_data) ---

def test_filtrar_dados_sem_filtros(sample_df):
    """Deve retornar o DF original se nenhum filtro for passado."""
    filtros_vazios = {
        "anos": [],
        "senioridade": [],
        "contrato": [],
        "empresas": []
    }
    
    # Injetamos o sample_df no lugar do df real do módulo
    with patch('config_data.df', sample_df):
        resultado = config_data.filtrar_dados(filtros_vazios)
        assert len(resultado) == 4
        assert resultado.equals(sample_df)

def test_filtrar_dados_por_ano(sample_df):
    """Deve filtrar corretamente apenas pelo ano."""
    filtros = {
        "anos": [2025],
        "senioridade": [],
        "contrato": [],
        "empresas": []
    }
    
    with patch('config_data.df', sample_df):
        resultado = config_data.filtrar_dados(filtros)
        assert len(resultado) == 2
        assert all(resultado['ano'] == 2025)

def test_filtrar_dados_combinados(sample_df):
    """Deve filtrar por múltiplos critérios (Ano E Senioridade)."""
    filtros = {
        "anos": [2025],
        "senioridade": ['Senior'],
        "contrato": [],
        "empresas": []
    }
    
    with patch('config_data.df', sample_df):
        resultado = config_data.filtrar_dados(filtros)
        assert len(resultado) == 1
        assert resultado.iloc[0]['cargo'] == 'Data Scientist'

def test_filtrar_dados_sem_match(sample_df):
    """Deve retornar DataFrame vazio se nenhum dado corresponder aos filtros."""
    filtros = {
        "anos": [2020], # Ano que não existe no sample
        "senioridade": [],
        "contrato": [],
        "empresas": []
    }
    
    with patch('config_data.df', sample_df):
        resultado = config_data.filtrar_dados(filtros)
        assert resultado.empty

# --- Testes da View (config_app) ---

def test_validar_dados_com_dados(sample_df):
    """Deve retornar True se o DataFrame não estiver vazio."""
    # Mockamos st.warning e st.info para não poluir a saída do teste
    with patch('config_app.st'):
        assert config_app.validar_dados(sample_df) is True

def test_validar_dados_vazio():
    """Deve retornar False e chamar st.warning se o DataFrame estiver vazio."""
    df_vazio = pd.DataFrame()
    
    with patch('config_app.st') as mock_st:
        resultado = config_app.validar_dados(df_vazio)
        assert resultado is False
        mock_st.warning.assert_called_once()

def test_exibir_metricas_execucao(sample_df):
    """Verifica se a função de métricas roda sem erros (Smoke Test)."""
    with patch('config_app.st') as mock_st:
        # Configura as colunas mockadas
        mock_col = MagicMock()
        mock_st.columns.return_value = [mock_col, mock_col, mock_col, mock_col]
        
        config_app.exibir_metricas(sample_df)
        
        # Verifica se as métricas foram chamadas
        assert mock_col.metric.call_count == 4

def test_exibir_graficos_execucao(sample_df):
    """Verifica se a função de gráficos tenta renderizar os gráficos (Smoke Test)."""
    with patch('config_app.st') as mock_st:
        # Mock das colunas
        mock_col = MagicMock()
        # A função chama st.columns(2) duas vezes
        mock_st.columns.return_value = [mock_col, mock_col]
        
        config_app.exibir_graficos(sample_df)
        
        # Verifica se o plotly_chart foi chamado
        # Como temos 4 gráficos, esperamos chamadas no st.plotly_chart
        assert mock_st.plotly_chart.called or mock_col.plotly_chart.called

def test_exibir_tabela_execucao(sample_df):
    """Verifica se a tabela é renderizada."""
    with patch('config_app.st') as mock_st:
        config_app.exibir_tabela(sample_df)
        mock_st.dataframe.assert_called_once()
