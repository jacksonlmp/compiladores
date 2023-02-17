# Adianta o ponteiro para ler uma casa a frente
def lookAhead(posicao):
    return posicao + 1

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
        if tokens[posicao] == "tipo":
            posicao = lookAhead(posicao)
            return verificarDeclaracaoDeVariavel(posicao, tokens, lexemas, numeroLinhas)

        elif tokens[posicao] == "if":
            posicao = lookAhead(posicao)
            return verificarIf(posicao, tokens, lexemas, numeroLinhas)
        
        elif tokens[posicao] == "laco":
            posicao = lookAhead(posicao)
            # return verificarLaco(posicao, tokens, lexemas, numeroLinhas)

        elif tokens[posicao] == "funcao":
            posicao = lookAhead(posicao)
            # return verificarDeclaracaoDeFuncao(posicao, tokens, lexemas, numeroLinhas)
        
        elif tokens[posicao] == "procedimento":
            posicao = lookAhead(posicao)
            return verificarDeclaracaoDeProcedimento(posicao, tokens, lexemas, numeroLinhas)

        elif tokens[posicao] == "idProcedimento":
            posicao = lookAhead(posicao)
            # return verificarChamadaDeProcedimento(posicao, tokens, lexemas, numeroLinhas)

        elif tokens[posicao] == "print":
            posicao = lookAhead(posicao)
            return verificarPrint(posicao, tokens, lexemas, numeroLinhas)

        else:
            exit("Ocorreu um erro sintatico na linha "+ str(numeroLinhas[posicao]) + ". Lexema "+ lexemas[posicao]
                + " invalido. Linguagem nao reconhecida.")

    except IndexError:
        exit("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao - 1]) + ". Lexema " + str(lexemas[posicao - 1]) 
            + " invalido. Linguagem nao reconhecida.")

def verificarDeclaracaoDeVariavel(posicao, tokens, lexemas, numeroLinhas):
    if tokens[posicao] == "idVariavel":
        posicao = lookAhead(posicao)
        if tokens[posicao] == "atribuicao":
            posicao = lookAhead(posicao)
            # Analisa se apos a igualdade, ha uma expressao atribuindo valor a variavel
            posicao = verificarExpressao(posicao, tokens, lexemas, numeroLinhas)
            
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

# Verifica a estrutura condicional
def verificarIf(posicao, tokens, lexemas, numeroLinhas):
    try:
        if tokens[posicao] == "abreParentese":
            posicao = lookAhead(posicao)

            # Analisar expressao dentro da estrutura condicional
            posicao = verificarExpressao(posicao, tokens, lexemas, numeroLinhas)

            # Continuacao da condicao apos a expressao
            if tokens[posicao] == "fechaParentese":
                posicao = lookAhead(posicao)
                
                if tokens[posicao] == "abreChave":
                    posicao = lookAhead(posicao)
                    while(tokens[posicao] != "fechaChave"):
                        posicao = verificarBloco(posicao, tokens, lexemas, numeroLinhas)
                        posicao = lookAhead(posicao)
                    
                    # Finalizou a execucao. Ou terminou o if ou aconteceu erro (analisamos proximo caractere para verificar)
                    posicao = lookAhead(posicao)
                    if posicao < (len(tokens) - 1):
                        if tokens[posicao] == "else":
                            posicao = lookAhead(posicao)
                            posicao = verificarElse(posicao, tokens, lexemas, numeroLinhas)
                        else:
                            return posicao - 1
                    return posicao
                else:
                    exit("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao]) 
                        + ". Lexema " + str(lexemas[posicao]) + " invalido. Era esperado uma abertura de chaves.")
            else:
                exit("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao]) 
                    + ". Lexema " + str(lexemas[posicao]) + " invalido. Era esperado um fechamento de parenteses.")
        else:
                exit("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao]) 
                    + ". Lexema " + str(lexemas[posicao]) + " invalido. Era esperado uma abertura de parenteses.")
    except IndexError:
        exit("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao - 1]) 
            + ". Lexema" + str(lexemas[posicao - 1]) + " invalido.")

# Verifica parte contraria da estrutura condicional
def verificarElse(posicao, tokens, lexemas, numeroLinha):
    try:    
        if tokens[posicao] == "abreChave":
            posicao = lookAhead(posicao) 
            while(tokens[posicao] != "fechaChave"): 
                posicao = verificarBloco(posicao, tokens, lexemas, numeroLinhas)
                posicao = lookAhead(posicao)
            
            # Finalizou a execucao. Ou terminou o else ou aconteceu erro
            return posicao    
            
        else:
            exit("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao]) 
                        + ". Lexema " + str(lexemas[posicao]) + " invalido. Era esperado uma abertura de chaves.")
    except IndexError:
        exit("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao - 1]) 
            + ". Lexema" + str(lexemas[posicao - 1]) + " invalido.") 

def verificarPrint(posicao, tokens, lexemas, numeroLinhas):
    if (tokens[posicao] == "idVariavel") or (tokens[posicao] == "constante"):
        posicao = lookAhead(posicao)
        if tokens[posicao] == "pontoEVirgula":
            return posicao
        else:
            exit("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + str(lexemas[posicao]) + " invalido. Verifique a separacao das linhas com ;")
    else:
        exit("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + str(lexemas[posicao]) + " invalido. Verifique o parametro informado na impressao")

def verificarDeclaracaoDeProcedimento(posicao, tokens, lexemas, numeroLinhas):
    if tokens[posicao] == "idProcedimento":
        posicao = lookAhead(posicao)

        if tokens[posicao] == "abreParentese":
            posicao = lookAhead(posicao)
            
            posicao = verificarParametros(posicao, tokens, lexemas, numeroLinhas)
            
            if tokens[posicao] == "abreChave":
                
                while(tokens[posicao] != "fechaChave"):
                    posicao = lookAhead(posicao) 
                                  
                    if tokens[posicao] != "fechaChave":
                        posicao = verificarBloco(posicao, tokens, lexemas, numeroLinhas)
                
                return posicao

            else:
                exit("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao]) 
                    + ". Lexema " + str(lexemas[posicao]) + " invalido. Era esperado uma abertura de chaves.")
        else:
            exit("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + str(lexemas[posicao]) + " invalido. Era esperado uma abertura de parenteses.")
    else:
        exit("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao ]) 
            + ". Lexema" + str(lexemas[posicao ]) + " invalido.")