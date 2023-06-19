import pandas as pd
import numpy as np
import datetime
import os
import json

'''
Esse arquivo contém todas as operações que são utilizadas para gerar o response do servidor para página web. Toda manipulação de dados
É contida nesse arquivo.
As bibliotecas pandas e numpy (utilizadas para manipulação de dados) não são nativas do Python. No arquivo README no diretório "SOLUÇÃO"
Existe um arquivo chamado "requirements.txt" que contém todas as bibliotecas utilizadas nesse projeto e um breve tutorial de como instalar em
Um arquivo README.md
'''
######################################################################## WEBPAGE ########################################################################
path= os.path.join(os.path.dirname(__file__), '..', 'webpage', 'index.html')
with open(path, 'r', encoding='utf-8') as file:
    WEBPAGE_YETI = file.read()
    file.close()
    
##################################################################### DATA HANDLER #####################################################################
# Globals
def get_df() -> pd.DataFrame:
    """Opens the table and returns it as a pandas dataframe."""
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, '..', '..', 'data', 'database.csv')
    df = pd.read_csv(csv_path, sep=';')
    df = data_treatment(df)
    # print(df)
    # print(df.info())
    return df

def data_treatment(df:pd.DataFrame) -> pd.DataFrame:
    '''Returns a dataframe with the data treated.'''
    df.fillna(0, inplace=True)
    df.DATA = pd.to_datetime(df.DATA, format='%Y/%m/%d')
    df.SYSTEM_DATE = pd.to_datetime(df.SYSTEM_DATE, format='%Y/%m/%d %H:%M:%S.%f')
    df.TIPO = df.TIPO.astype('int8')
    df.CATEGORIA = df.CATEGORIA.astype('int16')
    df.DESCRICAO = df.DESCRICAO.astype('str')
    df.VALOR = df.VALOR.astype('float32')
    return df

def treat_visualization() -> pd.DataFrame: 
    """Returns a dataframe with the data treated for visualization."""
    df = get_df()
    TIPO = {0: 'ENTRADA',
            1: 'SAIDA'}
    CATEGORIA_SAIDA = {
        0: 'CASA',
        1: 'TRANSPORTE',
        2: 'ALIMENTACAO',
        3: 'SAUDE',
        4: 'LAZER',
        20: 'OUTROS'
        }
    CATEGORIA_ENTRADA = {
        0: 'SALARIO',
        1: 'BONIFICACAO',
        2: 'AUXILIO',
        3: 'COMISSAO',
        4: '13º SALARIO',
        20: 'OUTROS'
        }
    
    df.loc[df['TIPO'] == 0, 'CATEGORIA'] = df['CATEGORIA'].map(CATEGORIA_SAIDA)
    df.loc[df['TIPO'] == 1, 'CATEGORIA'] = df['CATEGORIA'].map(CATEGORIA_ENTRADA)
    df['TIPO'] = df['TIPO'].map(TIPO)
    

def att_database(df:pd.DataFrame) -> bool:
    """ Att the database with the new dataframe """
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, '..', '..', 'data', 'database.csv')
    df.to_csv(csv_path, sep=';', index=False)
    return True
        
################################################################# Gerenciador de Contas ##################################################################
def add_data(data: str) -> bool:
    """Adds a new row to the table and returns True if successful."""
    df = get_df()
    data_dict = json.loads(data)
    data_dict['SYSTEM_DATE'] = datetime.datetime.now()
    df = df.append(data_dict, ignore_index=True)
    try:
        att_database(df)
        return True
    except Exception:
        return False
    

def rm_last_data() -> bool:
    '''Removes the last row of the table and returns True if successful.'''
    # Essa função precisa ser aprimorada. Preciso fazer tratamentos de erro
    df = get_df()
    df = df.iloc[:-1]
    att_database(df)
    return True

def merge_data(index1:int, index2:int) -> bool:
    '''Merges two rows of the table and returns True if successful.'''
    # Essa função precisa ser aprimorada. Preciso fazer tratamentos de erro
    df = get_df()
    data1= df.loc[index1]
    df.drop(df.index[index1], inplace=True)
    data2= df.loc[index2]
    df.drop(df.index[index2], inplace=True)
    data = df.loc[index1] + df.loc[index2]
    data['SYSTEM_DATE'] = datetime.datetime.now()
    data.DESCRICAO = 'MERGED - ['+ data1.DESCRICAO + '] + [' + data2.DESCRICAO +']'
    df.append(data, ignore_index=True)
    att_database(df)
    return True


############################################################### Gerenciador de Transações ###############################################################

def get_total() -> float:
    """Returns the sum of column VALUES in the table."""
    df = get_df()
    #df = treat_visualization()
    plus = df[df['TIPO'] == 0]
    plus = plus['VALOR'].sum()
    minus = df[df['TIPO'] == 1]
    minus = minus['VALOR'].sum()
    return (plus - minus)

##################################################################### Painel Geral ######################################################################
def get_data_this_month() -> float:
    '''Returns a dataframe with the data from this month.'''
    now = datetime.datetime.now().month
    year= datetime.datetime.now().year
    df = get_df()
    df= df[df['DATA'].dt.year == year]
    df.drop('DESCRICAO', axis=1, inplace=True) # Retirando a coluna DESCRIÇÃO, pois ela é STRING e não pode ser somada
    df = df[df['DATA'].dt.month == now]
    df['DATA'] = df['DATA'].dt.month
    plus = df[df['TIPO'] == 0]['VALOR'].sum()  # Soma dos valores onde TIPO é 0
    minus = df[df['TIPO'] == 1]['VALOR'].sum()  # Soma dos valores onde TIPO é 1
    return (plus - minus)
    
def get_data_last_6_months() -> list:
    '''Returns a list with the total revenue for the last 6 months.'''
    now = datetime.datetime.now()
    six_months_ago = now - pd.DateOffset(months=6)
    df = get_df()
    df.drop('DESCRICAO', axis=1, inplace=True)
    df['DATA'] = pd.to_datetime(df['DATA'])
    df = df[df['DATA'] >= six_months_ago]
    grouped = df.groupby(df['DATA'].dt.month)['VALOR'].sum()
    revenue = grouped.tolist()
    return revenue


def get_correlation() -> pd.Series:
    '''Returns a dataframe with the correlation between the columns of the dataframe.
     ______________________________________________
    |Autocorrelation|_Interpretation_______________|\n
    |_______________|_____________________________ |\n
    |1______________|_perfect_positive_correlation_|\n
    |0,7_to_0,9_____|_strong_correlation___________|\n
    |0,4_to_0,7_____|_moderate_correlation_________|\n
    |0,2_to_0,4_____|_weak_correlation_____________|\n
    |0______________|_null_correlation_____________|\n
    |<_0____________|_negative_correlation_________|\n
    |-1_____________|_perfect_negative_correlation_|\n
    |______________________________________________|\n
    '''
    
    '''
    Explicando melhor o que está acontecendo aqui:
    Eu quero descobrir quando a coluna 'VALOR' (quando seu VALOR == DESPESA) é afetada por outras colunas.
    Assim, eu consigo perceber uma correlation linear entre 'colunas' x 'gastos'
    '''
    
    df = get_df()
    
    # Aqui eu to filtrando para eu ver somente a correlation entre as colunas que são DESPESA do cliente
    filtered = df[df['TIPO'] == 1]
    
    # Aqui eu estou filtrando para retirar valores de SYSTEM_DATE (que é apenas um valor burocrático) e
    # Também estou retirando a coluna DESCRIÇÃO, pois ela não é relevante para a análise, já que além de ser um valor
    # String e ser um valor de controle do usuário, é também um valor único para cada linha, ou seja, não há correlation entre ela e outras colunas
    filtered = df.drop(['DESCRICAO', 'SYSTEM_DATE'], axis=1)
    
    # Aqui to calculando a matriz de correlation com o método corr()
    matrix = filtered.corr()
    # Finalmente, obtenho a correlation da coluna 'VALOR' com todas as outras colunas
    corr_values = matrix['VALOR']
    # E aqui eu removo a correlation da coluna 'VALOR' consigo mesma, já que ela é sempre 1
    corr_values = corr_values.drop('VALOR')

    # Para essa função, vou validar somente as correlações positivas
    return corr_values