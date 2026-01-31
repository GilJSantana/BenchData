import pandas as pd

df = pd.read_csv('./data/dados-final.csv')


def anos():
    anos = sorted(df['ano'].unique())
    return anos


def senioridade():
    senioridade = sorted(df['senioridade'].unique())
    return senioridade


def empresas():
    empresas = sorted(df['empresa'].unique())
    return empresas


def contrato():
    contrato = sorted(df['contrato'].unique())
    return contrato


def filtrar_dados(filtros):
    # Começamos com uma cópia ou referência ao df original para não alterá-lo globalmente
    df_filtrado = df.copy()

    if filtros['anos']:
        df_filtrado = df_filtrado[df_filtrado['ano'].isin(filtros['anos'])]

    if filtros['senioridade']:
        df_filtrado = df_filtrado[df_filtrado['senioridade'].isin(filtros['senioridade'])]

    if filtros['contrato']:
        df_filtrado = df_filtrado[df_filtrado['contrato'].isin(filtros['contrato'])]

    if filtros['empresas']:
        df_filtrado = df_filtrado[df_filtrado['empresa'].isin(filtros['empresas'])]

    return df_filtrado
