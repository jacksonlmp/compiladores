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

# Verifica se o codigo esta de acordo com a gramatica (seguindo ordem nela descrita)
def verificarBloco(indice, tokens, lexemas, numeroLinhas):
    try:
        if (tokens[indice] == "tipo"):
            indice = lookAhead(indice)
            # return verificarDeclaracaoDeVariavel(tokens, lexemas, numeroLinhas, indice)

        elif tokens[indice] == "if":
            indice = lookAhead(indice)
            # return verificarIf(tokens, lexemas, numeroLinhas, indice)
        
        elif tokens[indice] == "laco":
            indice = lookAhead(indice)
            # return verificarLaco(tokens, lexemas, numeroLinhas, indice)

        elif tokens[indice] == "funcao":
            indice = lookAhead(indice)
            # return verificarDeclaracaoDeFuncao(tokens, lexemas, numeroLinhas, indice)
        
        elif tokens[indice] == "procedimento":
            indice = lookAhead(indice)
            # return verificarDeclaracaoDeProcedimento(tokens, lexemas, numeroLinhas, indice)

        elif tokens[indice] == "idProcedimento":
            indice = lookAhead(indice)
            # return verificarChamadaDeProcedimento(tokens, lexemas, numeroLinhas, indice)

        elif tokens[indice] == "print":
            indice = lookAhead(indice)
            # return verificarPrint(tokens, lexemas, numeroLinhas, indice)

        else:
            exit("Ocorreu um erro sintatico na linha "+ str(numeroLinhas[indice]) + ". Lexema "+ lexemas[indice] + " invalido.")

    except IndexError:
        exit("Ocorreu um erro sintatico na linha " + str(numeroLinhas[indice - 1]) + ". Lexema " + str(lexemas[indice - 1]) + " invalido.")