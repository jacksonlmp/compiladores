import sys
sys.path.insert(1, './AnaliseLexica')
import AnalisadorLexico as lex
import pandas as pd

# Programa a ser analisado
codigo = open('CodigoDeExemplo.txt', 'r')

tabela_tokens = lex.realizarAnaliseLexica(codigo)

codigo.close()

# Modificando visualizacao do dataframe
estilos = [
{'selector': 'caption', 'props': [('font-size', '20px'), ('font-weight', 'bold')]}, 
{'selector': 'tr:hover', 'props': [('background-color', 'white'), ('color', 'black'), ('font-weight', 'bold')]}     
]
tabela_tokens.style.set_caption("Analise lexica").set_table_styles(estilos)