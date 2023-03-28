import numpy as np

def lookAhead(posicao):
    return posicao + 1

def mensagemErro(mensagem):
    if(isinstance(mensagem, np.ndarray)):
        print(mensagem[0])
    else:
        print(mensagem)
    exit()

def verificarEscopo(tabelaDeTokens, posicaoToken):
    for i in range(lookAhead(posicaoToken), -1, -1):
        if tabelaDeTokens["Token"][i] == "funcao":
            if estaDentroDoEscopo(tabelaDeTokens, i, posicaoToken):
                return tabelaDeTokens["Lexema"][i+2]
        elif tabelaDeTokens["Token"][i] == "procedimento":
            if estaDentroDoEscopo(tabelaDeTokens, i, posicaoToken):
                return tabelaDeTokens["Lexema"][i+1]
    return "Global"

def estaDentroDoEscopo(tabelaDeTokens, x, posicaoToken):
    abreChave = 0
    fechaChave = 0
    comeco = 0
    fim = 0
   
    tamanhoDaTabela = len(tabelaDeTokens)
    for i in range(x, tamanhoDaTabela):
        if tabelaDeTokens["Token"][i] == "abreChave":
            comeco = i
            break

    abreChave = 1
    for i in range(comeco + 1, tamanhoDaTabela):
        if tabelaDeTokens["Token"][i] == "abreChave":
            abreChave += 1
        elif tabelaDeTokens["Token"][i] == "fechaChave":
            fechaChave += 1
            if abreChave == fechaChave:
                fim = i
                return (posicaoToken > comeco and posicaoToken < fim)

def verificarSeDeclarouProcedimento(posicao, lexemas, numeroLinhas):
    #ehProcedimentoDeclarado
    ehJaDeclarado = False
    nomeProcedimento = lexemas[posicao-1]
    
    for i in range(posicao-1):
        if(nomeProcedimento == lexemas[i]):
            #Achei o mesmo nome: pode ser uma declaracao ou uma chamada
            #Vamos confirmar se eh declaracao
            if(lexemas[i-1] == 'proc'):
                #Eh declaracao. Ok
                ehJaDeclarado = True
    
    if ehJaDeclarado == False:
        mensagemErro("ERRO SEMANTICO - Linha " + str(numeroLinhas[posicao]) + " - " + str(numeroLinhas[posicao-1]) + " procedimento nao declarado anteriormente.")         


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
        mensagemErro("ERRO SEMÂNTICO - Linha " + str(numeroLinhas[posicao]) + str(lexemas[posicao - 1]) + " função não declarada anteriormente.")         
    
    if tipoFuncao != tipoVariavel:
        mensagemErro("ERRO SEMÂNTICO - Linha " + str(numeroLinhas[posicao]) + str(lexemas[posicao - 3]) + " tipo de variável diferente do retorno da função.")
