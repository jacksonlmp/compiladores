import numpy as np

def lookAhead(posicao):
    return posicao + 1

def mensagemErro(mensagem):
    if(isinstance(mensagem, np.ndarray)):
        print(mensagem[0])
    else:
        print(mensagem)
    exit()

def verificarEscopo():
    print("Work in progress")

def verificarSeDeclarouProcedimento(posicao, lexemas, numeroLinhas):
    #ehProcedimentoDeclarado
    nomeProcedimento = lexemas[posicao-1]
    
    #set() para criar um conjunto a partir da lista de lexemas
    #discard() para remover a string "proc" do conjunto.
    nomesProcedimentosDeclarados = set(lexemas[:posicao - 1])
    nomesProcedimentosDeclarados.discard('proc')

    if nomeProcedimento in nomesProcedimentosDeclarados:
        return True

    mensagemErro("ERRO SEMANTICO - Linha " +  str(numeroLinhas) + str(nomeProcedimento) + " procedimento nao declarado anteriormente.")


def verificarSeDeclarouFuncao(posicao, lexemas, numeroLinhas):
    #ehFuncaoDeclaradaEAtribuicaoRetorno
    ehDeclarada = False
    tipoFuncao = ''
    nomeFuncao = lexemas[posicao - 1]
    tipoVariavel = lexemas[posicao - 4]

    for i in range(posicao - 1):
        if nomeFuncao == lexemas[i]:
            if lexemas[i - 2] == 'func':
                # É declaração. Ok
                ehDeclarada = True
                tipoFuncao = lexemas[i - 1]
                
    if not ehDeclarada:
        mensagemErro("ERRO SEMÂNTICO - Linha " + str(numeroLinhas[posicao]), str(lexemas[posicao - 1]) + " função não declarada anteriormente.")         
    
    if tipoFuncao != tipoVariavel:
        mensagemErro("ERRO SEMÂNTICO - Linha " + str(numeroLinhas[posicao]), str(lexemas[posicao - 3]) + " tipo de variável diferente do retorno da função.")
