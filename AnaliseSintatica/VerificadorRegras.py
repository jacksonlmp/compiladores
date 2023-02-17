# Adianta o ponteiro para ler uma casa a frente
def lookAhead(x):
    return x + 1

# Verifica se as chaves e os parenteses estao duplamente balanceados e retorna o erro caso haja
def verificarBalanceamentoChaveEParentese(listaDeTokens):
    chavesAbertas = 0
    chavesFechadas = 0

    parentesesAbertos = 0
    parentesesFechados = 0

    for token in listaDeTokens:
        if token == "abreChave":
            chavesAbertas += 1
        elif token == "fechaChave":
            chavesFechadas += 1
        elif token == "abreParentese":
            parentesesAbertos += 1
        elif token == "fechaParentese":
            parentesesFechados += 1

    if chavesAbertas > chavesFechadas:
        exit("Ocorreu um erro sintatico no balanceamento de chaves. Ha mais { do que }.")
    elif chavesAbertas < chavesFechadas:
        exit("Ocorreu um erro sintatico no balanceamento de chaves. Ha mais } do que {.")

    if parentesesAbertos > parentesesFechados:
        exit("Ocorreu um erro sintatico na balanceamento de parenteses. Ha mais ( do que ).")
    elif parentesesAbertos < parentesesFechados:
        exit("Ocorreu um erro sintatico no balanceamento de parenteses. Ha mais ) do que (.")

# Verifica se o codigo esta de acordo com a gramatica
def verificarBloco(posicao, tokens, lexemas, numeroLinhas):
    try:
        if (tokens[posicao] == "tipo"):
            posicao = lookAhead(posicao)
            return verificarDeclaracaoDeVariavel(tokens, lexemas, numeroLinhas, posicao)

        elif tokens[posicao] == "if":
            posicao = lookAhead(posicao)
            # return verificarIf(tokens, lexemas, numeroLinhas, posicao)
        
        elif tokens[posicao] == "laco":
            posicao = lookAhead(posicao)
            # return verificarLaco(tokens, lexemas, numeroLinhas, posicao)

        elif tokens[posicao] == "funcao":
            posicao = lookAhead(posicao)
            # return verificarDeclaracaoDeFuncao(tokens, lexemas, numeroLinhas, posicao)
        
        elif tokens[posicao] == "procedimento":
            posicao = lookAhead(posicao)
            # return verificarDeclaracaoDeProcedimento(tokens, lexemas, numeroLinhas, posicao)

        elif tokens[posicao] == "idProcedimento":
            posicao = lookAhead(posicao)
            # return verificarChamadaDeProcedimento(tokens, lexemas, numeroLinhas, posicao)

        elif tokens[posicao] == "print":
            posicao = lookAhead(posicao)
            # return verificarPrint(tokens, lexemas, numeroLinhas, posicao)

        else:
            exit("Ocorreu um erro sintatico na linha "+ str(numeroLinhas[posicao]) + ". Lexema "+ lexemas[posicao] + " invalido.")

    except IndexError:
        exit("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao - 1]) + ". Lexema " + str(lexemas[posicao - 1]) + " invalido.")

def verificarDeclaracaoDeVariavel(tokens, lexemas, numeroLinhas, posicao):
    if tokens[posicao] == "idVariavel":
        posicao = lookAhead(posicao)
        if tokens[posicao] == "atribuicao":
            posicao = lookAhead(posicao)
            # Analisa se apos a igualdade, ha uma expressao atribuindo valor a variavel
            posicao = verificarExpressao(tokens, lexemas, numeroLinhas, posicao)
            
            # Chegou ao fim. Caso nao indique termino, ocorreu erro sintatico
            if tokens[posicao] == "pontoEVirgula":
                return posicao
            else:
                exit("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + str(tokens[posicao]) + " invalido. Verifique a separacao das linhas com ;")
        else:
            exit("Ocorreu um erro sintatico na atribuicao de variavel. Linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + str(tokens[posicao]) + " invalido.")
    else:
        exit("Ocorreu um erro sintatico na declaracao de variavel. Linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + str(tokens[posicao]) + " invalido.")
