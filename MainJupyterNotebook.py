import sys
sys.path.insert(1, './AnaliseLexica')
sys.path.insert(1, './AnaliseSintatica')
import AnalisadorLexico as lex
import AnalisadorSintatico as sint
import pandas as pd

# Programa a ser analisado
codigo = open('CodigoDeExemplo.txt', 'r')

tabelaDeTokens = lex.realizarAnaliseLexica(codigo)

codigo.close()

# Modificando visualizacao do dataframe
estilos = [
{'selector': 'caption', 'props': [('font-size', '20px'), ('font-weight', 'bold')]}, 
{'selector': 'tr:hover', 'props': [('background-color', 'white'), ('color', 'black'), ('font-weight', 'bold')]}     
]
tabelaDeTokens.style.set_caption("Analise lexica").set_table_styles(estilos)

tabelaDeSimbolos = sint.realizarAnaliseSintatica(tabelaDeTokens)
print(tabelaDeSimbolos)