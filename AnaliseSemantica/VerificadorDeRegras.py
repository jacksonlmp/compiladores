import numpy as np

def lookAhead(posicao):
    return posicao + 1

def mensagemErro(mensagem):
    if(isinstance(mensagem, np.ndarray)):
        print(mensagem[0])
    else:
        print(mensagem)
    exit()

# Retorna o escopo da variavel (a funcao/procedimento que ela pertence ou se eh global)
def verificarEscopo(tabelaDeTokens, posicaoToken):
    # Percorre da posicao atual, ate o inicio do codigo, voltando um token de cada vez
    for i in range(lookAhead(posicaoToken), -1, -1):
        if tabelaDeTokens["Token"][i] == "funcao":
            if estaDentroDoEscopo(tabelaDeTokens, posicaoToken, i):
                # Retorna o identificador da funcao
                return tabelaDeTokens["Lexema"][i+2] # (pulando o 'func tipoDeRetorno')
        elif tabelaDeTokens["Token"][i] == "procedimento":
            if estaDentroDoEscopo(tabelaDeTokens, posicaoToken, i):
                # Retorna o identificador do procedimento
                return tabelaDeTokens["Lexema"][i+1] # (pulando o 'proc')
    return "Global"

# Retorna se a posicao do token esta dentro do escopo da funcao/procedimento
def estaDentroDoEscopo(tabelaDeTokens, posicaoDoToken, posicaoDoMetodo):
    qtdAbreChave = 0
    qtdFechaChave = 0
    posicaoInicioDoMetodo = 0
    posicaoFimDoMetodo = 0
    tamanhoDaTabela = len(tabelaDeTokens)

    # Define o inicio do metodo (abertuda de chave)
    for tokenAtual in range(posicaoDoMetodo, tamanhoDaTabela):
        if tabelaDeTokens["Token"][tokenAtual] == "abreChave":
            posicaoInicioDoMetodo = tokenAtual
            qtdAbreChave += 1
            break

    # Percorrer ate o fim do metodo para verificar se o token esta nesse intervalo
    for tokenAtual in range(posicaoInicioDoMetodo + 1, tamanhoDaTabela):
        if tabelaDeTokens["Token"][tokenAtual] == "abreChave":
            qtdAbreChave += 1
        elif tabelaDeTokens["Token"][tokenAtual] == "fechaChave":
            qtdFechaChave += 1
            # Chegou no fim do metodo, verifica se o token esta contido nele
            if qtdAbreChave == qtdFechaChave:
                posicaoFimDoMetodo = tokenAtual
                return (posicaoDoToken > posicaoInicioDoMetodo and posicaoDoToken < posicaoFimDoMetodo)

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
        mensagemErro("Ocorreu um erro semantico na linha " + str(numeroLinhas[posicao]) + ". Procedimento " + str(lexemas[posicao-1]) + " nao declarado anteriormente.")         


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
        mensagemErro("Ocorreu um erro semantico na linha " + str(numeroLinhas[posicao]) + ". Funcao " + str(lexemas[posicao - 1]) + " nao declarada anteriormente.")         
    
    if tipoFuncao != tipoVariavel:
        mensagemErro("Ocorreu um erro semantico na linha " + str(numeroLinhas[posicao]) + ". Tipo de variavel " + str(lexemas[posicao - 3]) + " diferente do retorno da funcao.")
