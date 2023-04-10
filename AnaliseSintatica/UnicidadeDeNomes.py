import pandas as pd
import numpy as np

def mensagemErro(mensagem):
    if(isinstance(mensagem, np.ndarray)):
        print(mensagem[0])
    else:
        print(mensagem)
    exit()

# Verifica se existem nomes ja utilizados
def verificarUnicidadeDeNomes(tabelaDeSimbolos):
    verificarUnicidadeNoNomeDeFuncao(tabelaDeSimbolos)
    verificarUnicidadeNoNomeDeProcedimento(tabelaDeSimbolos)
    verificarUnicidadeNoNomeDeVariavel(tabelaDeSimbolos)

# Verifica se existe mais de uma funcao com o mesmo nome
def verificarUnicidadeNoNomeDeFuncao(tabelaDeSimbolos):
    nomesFuncoes = []
    
    for linha, coluna in tabelaDeSimbolos.iterrows():
        if(coluna['Token'] == 'funcao'):
            if(not coluna['Lexema'] in nomesFuncoes):
                nomesFuncoes.append(coluna['Lexema'])
            else:
                mensagemErro("Ocorreu um erro semantico na linha "+ str(coluna['Linha']) + ". Ja existe uma funcao chamada " + coluna['Lexema'])

# Verifica se existe mais de um procedimento com o mesmo nome
def verificarUnicidadeNoNomeDeProcedimento(tabelaDeSimbolos):
    nomesProcedimento = []
    
    for linha, coluna in tabelaDeSimbolos.iterrows():
        if(coluna['Token'] == 'procedimento'):
            if(not coluna['Lexema'] in nomesProcedimento):
                nomesProcedimento.append(coluna['Lexema'])
            else:
                mensagemErro("Ocorreu um erro semantico na linha "+ str(coluna['Linha']) + ". Ja existe um procedimento chamado " + coluna['Lexema'])

# Verifica se existe mais de uma variavel com o mesmo nome e escopo
def verificarUnicidadeNoNomeDeVariavel(tabelaDeSimbolos):
    escopos = tabelaDeSimbolos['Escopo'].unique()

    if 'NA' in escopos:
        indice = np.where(escopos == 'NA')
        escopos = np.delete(escopos, indice[0][0])
    
    for posicao in range(len(escopos)):
        variaveis = []
        escopo = escopos[posicao]

        for linha, coluna in tabelaDeSimbolos.iterrows():
            if coluna['Token'] == 'idVariavel':
                if coluna['Escopo'] == escopo:
                    if not coluna['Lexema'] in variaveis:
                        variaveis.append(coluna['Lexema'])
                    else:
                        mensagemErro("Ocorreu um erro semantico na linha "+ str(coluna['Linha']) + ". A variavel " + coluna['Lexema'] + " ja foi declarada neste escopo ")
            
            # Devemos obter os parametros para analisar se a variavel do escopo possui mesmo nome deles
            elif coluna['Escopo'] == 'NA' and coluna['Lexema'] == escopo: # Declaracao de funcao ou procedimento
                    parametros = coluna['Variaveis']
                    for variavel in parametros:
                        if not variavel in variaveis:
                            variaveis.append(variavel)