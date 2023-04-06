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
    try:
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
    except IndexError:
        mensagemErro("Excecao na verificacao de escopo")

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

# Verifica se o procedimento ja foi declarado anteriormente
def verificarSeDeclarouProcedimento(posicao, lexemas, numeroLinhas):
    try:
        declaradoAnteriormente = False
        nomeProcedimento = lexemas[posicao-1]
        
        for i in range(posicao-1):
            if(nomeProcedimento == lexemas[i]):
                if(lexemas[i-1] == 'proc'): # Verificando se eh declaracao ou chamada
                    declaradoAnteriormente = True
        
        if not declaradoAnteriormente:
            mensagemErro("Ocorreu um erro semantico na linha " + str(numeroLinhas[posicao]) + ". Procedimento " + str(lexemas[posicao-1][0]) + " nao declarado anteriormente.")         

    except IndexError:
        mensagemErro("Excecao na verificacao de procedimento")

# Verifica se a funcao ja foi declarada anteriormente e se o tipo de retorno eh o esperado
def verificarTipoRetornoESeDeclarouFuncao(posicao, lexemas, numeroLinhas):
    try:
        declaradaAnteriormente = False
        tipoFuncao = ''
        nomeFuncao = lexemas[posicao - 1]
        tipoVariavel = lexemas[posicao - 4]

        for i in range(posicao - 1):
            if nomeFuncao == lexemas[i]:
                if lexemas[i - 2] == 'func': # Verificando se eh declaracao ou chamada
                    declaradaAnteriormente = True
                    tipoFuncao = lexemas[i - 1]
                    
        if not declaradaAnteriormente:
            mensagemErro("Ocorreu um erro semantico na linha " + str(numeroLinhas[posicao]) + ". Funcao " + str(lexemas[posicao - 1][0]) + " nao declarada anteriormente.")         
        
        if tipoFuncao != tipoVariavel:
            mensagemErro("Ocorreu um erro semantico na linha " + str(numeroLinhas[posicao][0]) + ". Tipo de variavel " + str(lexemas[posicao - 3][0]) + " diferente do retorno da funcao.")

    except IndexError:
        mensagemErro("Excecao na verificacao de funcao")

# Verifica se o boolean recebeu 'true' ou 'false'
def verificarSeVariavelEhBooleana(posicao, tokens, lexemas, numeroLinhas):
    posicaoDoTipo = posicao - 3
    if lexemas[posicaoDoTipo] != 'boolean':
        mensagemErro("Ocorreu um erro semantico na linha " + str(numeroLinhas[posicao][0]) + 
            ". Tipo de variavel " + str(lexemas[posicao - 2][0]) + " diferente do tipo da atribuicao (foi informado um booleano).")

# Verifica se o int recebeu uma constante numerica
def verificarSeVariavelEhInteira(posicao, tokens, lexemas, numeroLinhas):
    posicaoDoTipo = posicao - 3
    if lexemas[posicaoDoTipo] != 'int':
        mensagemErro("Ocorreu um erro semantico na linha " + str(numeroLinhas[posicao][0]) + 
            ". Tipo de variavel " + str(lexemas[posicao - 2][0]) + " diferente do tipo da atribuicao (foi informado um inteiro).")

# Na atribuicao, verifica se a variavel existia anteriormente e se os tipos sao iguais
def verificarSeVariavelExisteETiposSaoIguais(posicao, tokens, lexemas, numeroLinhas):
    declaradaAnteriormente = False
    nomeVariavel = lexemas[posicao]
    posicao = posicao - 3 # Voltando para antes da variavel que esta recebendo a atribuicao
    tipo = lexemas[posicao]
    
    for i in range(posicao-1):
        if(nomeVariavel == lexemas[i]):
                declaradaAnteriormente = True
                tipoAtribuido = lexemas[i - 1]
                break
    
    if not declaradaAnteriormente:
        mensagemErro("Ocorreu um erro semantico na linha " + str(numeroLinhas[posicao][0]) + ". Variavel " + nomeVariavel + " nao declarada anteriormente.")         

    if tipo != tipoAtribuido:
        mensagemErro("Ocorreu um erro semantico na linha " + str(numeroLinhas[posicao][0]) + ". Variavel " + nomeVariavel + " possui tipo diferente do esperado.")         

# Na atribuicao, verifica se a variavel existia anteriormente
def verificarSeVariavelExiste(posicao, tokens, lexemas, numeroLinhas):
    declaradaAnteriormente = False
    nomeVariavel = lexemas[posicao]
    posicao = posicao - 3 # Voltando para antes da variavel que esta recebendo a atribuicao
    
    for i in range(posicao-1):
        if(nomeVariavel == lexemas[i]):
                declaradaAnteriormente = True
                break

    if not declaradaAnteriormente:
        mensagemErro("Ocorreu um erro semantico na linha " + str(numeroLinhas[posicao][0]) + ". Variavel " + nomeVariavel + " nao declarada anteriormente.")         

# Verifica se o tipo de variavel recebida eh igual ao tipo de parametro em funcoes
def verificarTipoDeParametroEArgumentoDeFuncao(tabelaDeSimbolos):
    tamanhoDaTabela = len(tabelaDeSimbolos)
    for posicao in range(tamanhoDaTabela):
        if tabelaDeSimbolos['Valor'][posicao][0] == 'f': # Toda funcao comeca com f, logo a chamada dela tambem

            # Para cada funcao, guarda as variaveis e os tipos para comparar logo em seguida onde foi chamada
            nomeDoMetodo = tabelaDeSimbolos['Valor'][posicao].split("(")[0]
            variaveis = tabelaDeSimbolos['Variaveis'][posicao]

            # Obtendo os tipos a partir da declaracao/assinatura da funcao
            indiceDeclaracaoFuncao = tabelaDeSimbolos['Lexema'].eq(nomeDoMetodo).idxmax() # Como a declaracao vem antes do uso, pega a primeira ocorrencia
            tiposVariaveis = tabelaDeSimbolos['TiposVariaveis'][indiceDeclaracaoFuncao]
            
            for indice in range(len(variaveis)):
                # Para cada variavel, busca seu indice e compara se o tipo da sua declaracao eh diferente do tipo de argumento da funcao
                nomeVariavel = variaveis[indice]
                indiceLexema = tabelaDeSimbolos['Lexema'].eq(nomeVariavel).idxmax()

                # Se a variavel nao existir na tabela de simbolos, o idxmax retornara zero. 
                # Como zero eh um numero valido, devemos verificar se realmente nao se trata da variavel esperada
                if tabelaDeSimbolos['Lexema'][indiceLexema] != nomeVariavel:
                    mensagemErro("Ocorreu um erro semantico na linha " + str(tabelaDeSimbolos['Linha'][posicao]) + ". Variavel " + nomeVariavel + " nao declarada anteriormente.")

                if tabelaDeSimbolos['Tipo'][indiceLexema] != tiposVariaveis[indice]:
                    mensagemErro("Ocorreu um erro semantico na linha " + str(tabelaDeSimbolos['Linha'][posicao]) + 
                    ". Variavel " + nomeVariavel + " declarada com um tipo diferente do esperado pela funcao " + nomeDoMetodo +
                    ". Deveria ser um " + tiposVariaveis[indice] + " em vez de um " + tabelaDeSimbolos['Tipo'][indiceLexema]) 

                #print(tabelaDeSimbolos['Lexema'].eq(variavel).idxmax())
                #print('Tipo ' + tabelaDeSimbolos.loc[tabelaDeSimbolos['Lexema'] == variavel, 'Tipo'].iloc[0])
                # Buscando o indice da variavel na coluna dos lexemas
                #indice = tabelaDeSimbolos.loc[tabelaDeSimbolos['Lexema'] == variavel].index[0]
                #print(variavel + ' no indice ' + indice)

            # Atualizar valor dos argumentos nos tipos de variaveis da tabela de simbolos
            tabelaDeSimbolos.at[posicao, 'TiposVariaveis'] = tiposVariaveis
    return tabelaDeSimbolos

# Verifica se o tipo de variavel recebida eh igual ao tipo de parametro em procedimentos
def verificarTipoDeParametroEArgumentoDeProcedimento(tabelaDeSimbolos):
    tamanhoDaTabela = len(tabelaDeSimbolos)
    for posicao in range(tamanhoDaTabela):
        if tabelaDeSimbolos['Token'][posicao] == 'idProcedimento':
            # Para cada  procedimento, guarda as variaveis e os tipos para comparar logo em seguida onde foi chamado
            nomeDoMetodo = tabelaDeSimbolos['Lexema'][posicao]
            variaveis = tabelaDeSimbolos['Variaveis'][posicao]

            # Obtendo os tipos a partir da declaracao/assinatura do procedimento
            indiceDeclaracaoProc = tabelaDeSimbolos['Lexema'].eq(nomeDoMetodo).idxmax() # Como a declaracao vem antes do uso, pega a primeira ocorrencia
            tiposVariaveis = tabelaDeSimbolos['TiposVariaveis'][indiceDeclaracaoProc]
            
            for indice in range(len(variaveis)):
                # Para cada variavel, busca seu indice e compara se o tipo da sua declaracao eh diferente do tipo de argumento do procedimento
                nomeVariavel = variaveis[indice]
                indiceLexema = tabelaDeSimbolos['Lexema'].eq(nomeVariavel).idxmax()
                
                # Se a variavel nao existir na tabela de simbolos, o idxmax retornara zero. 
                # Como zero eh um numero valido, devemos verificar se realmente nao se trata da variavel esperada
                if tabelaDeSimbolos['Lexema'][indiceLexema] != nomeVariavel:
                    mensagemErro("Ocorreu um erro semantico na linha " + str(tabelaDeSimbolos['Linha'][posicao]) + ". Variavel " + nomeVariavel + " nao declarada anteriormente.")

                if tabelaDeSimbolos['Tipo'][indiceLexema] != tiposVariaveis[indice]:
                    mensagemErro("Ocorreu um erro semantico na linha " + str(tabelaDeSimbolos['Linha'][posicao]) + 
                    ". Variavel " + nomeVariavel + " declarada com um tipo diferente do esperado pelo procedimento " + nomeDoMetodo +
                    ". Deveria ser um " + tiposVariaveis[indice] + " em vez de um " + tabelaDeSimbolos['Tipo'][indiceLexema])         

            # Atualizar valor dos argumentos nos tipos de variaveis da tabela de simbolos
            tabelaDeSimbolos.at[posicao, 'TiposVariaveis'] = tiposVariaveis
    return tabelaDeSimbolos

def verificarTiposDentroDeIfEWhile(posicao, tokens, lexemas, numeroLinhas, tabelaDeSimbolos):
    # Verifica comparacao de tipos, por exemplo inteiro com booleano
    # Analisa se operadores fazem sentido para aquele tipo. Ex: boolean > boolean, deveria dar erro (aceita apenas == ou !=)
    # Percorre ate achar o fim do if ou while, ou seja, ate encontrar um fecha parentese seguido de abertura de chave
    print('Work in progress')
    ### MODIFICAR ESTE TRECHO - Deverá retornar posição final do if ou while
    return posicao