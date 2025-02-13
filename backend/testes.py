import pandas as pd

# Supondo que o CSV seja armazenado localmente, substitua 'caminho_do_arquivo.csv' pelo seu caminho real.
arquivo_csv = 'novo.csv'

# Carregar o CSV com o delimitador correto (neste caso, ponto e vírgula)
dados = pd.read_csv(arquivo_csv, delimiter=';')

# Exibir os dados carregados
print(dados)
