import sys
sys.path.insert(1, './AnaliseLexica')

import AnalisadorLexico as lex
import pandas as pd
from tabulate import tabulate

# Programa a ser analisado
codigo = open('CodigoDeExemplo.txt', 'r')

tabela_tokens = lex.realizarAnaliseLexica(codigo)

# Guardando resultado da analise em um arquivo
arquivo = open("SaidaLexico.txt", 'w')
str = tabela_tokens.to_string()
arquivo.write(str)

# Configurando exibicao da tabela
tabela_tokens.style.set_properties(**{'background-color': 'black', 'color': 'lawngreen', 'border-color' : 'white'})

tabela_tokens.style.set_caption('Analise lexica').set_table_styles([{'selector': 'caption', 'props': 'font-size: 20px; font-weight: bold'}])

# Imprimindo toda a tabela no console de execucao
with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                       'display.precision', 3,
                       ): print(tabulate(tabela_tokens, headers='keys', tablefmt='pretty'))

# Fechando os arquivos
codigo.close()
arquivo.close()