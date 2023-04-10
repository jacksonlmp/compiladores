def gerarCodigoIntermediario(tabelaDeTokens):
    linha = ""
    qtdLabel = 0
    ultimaPosicaoLida = -1 # Deve comecar menor que a primeira iteracao

    arquivo = open("./CodigoIntermediario.txt", "w")

    for posicao in range(len(tabelaDeTokens)):
        if ultimaPosicaoLida >= posicao:
            continue

        if tabelaDeTokens["Token"][posicao] == "pontoEVirgula" or tabelaDeTokens["Token"][posicao] == "abreChave" or tabelaDeTokens["Token"][posicao] == "fechaChave":
            linha += tabelaDeTokens["Lexema"][posicao] + "\n"
            arquivo.write(linha)
            linha = ""
            continue

        elif tabelaDeTokens["Token"][posicao] == "laco":
            qtdLabel += 1
            info = gerarBlocoLaco(arquivo, tabelaDeTokens, posicao, qtdLabel)
            ultimaPosicaoLida = info[0]
            qtdLabel = info[1]
            linha = info[2]
            continue

        elif tabelaDeTokens["Token"][posicao] == "funcao":
            info = gerarBlocoDeclaracaoFuncao(arquivo, tabelaDeTokens, posicao, qtdLabel)
            ultimaPosicaoLida = info[0]
            qtdLabel = info[1]
            continue
    
        elif tabelaDeTokens["Token"][posicao] == "idFuncao":
            info = gerarBlocoChamadaFuncao(arquivo, tabelaDeTokens, posicao, qtdLabel, linha)
            ultimaPosicaoLida = info[0]
            qtdLabel = info[1]
            linha = info[2]
            continue

        elif tabelaDeTokens["Token"][posicao] == "procedimento":
            info = gerarBlocoDeclaracaoProcedimento(arquivo, tabelaDeTokens, posicao, qtdLabel)
            ultimaPosicaoLida = info[0]
            qtdLabel = info[1]
            continue

        elif tabelaDeTokens["Token"][posicao] == "idProcedimento":
            info = gerarBlocoChamadaProcedimento(arquivo, tabelaDeTokens, posicao, qtdLabel, linha)
            ultimaPosicaoLida = info[0]
            qtdLabel = info[1]
            linha = info[2]
            continue

        linha += tabelaDeTokens["Lexema"][posicao] + " "

def gerarBlocoDeclaracaoFuncao(arquivo, tabelaDeTokens, posicao, qtdLabel):
    abreChave = 0
    fechaChave = 0
    buffer = ""

    for j in range(posicao, len(tabelaDeTokens)):
        if tabelaDeTokens["Token"][j] == "idFuncao":
            buffer = tabelaDeTokens["Lexema"][j] + ":\nBeginFunc;\n"
            arquivo.write(buffer)
            buffer = ""
        elif tabelaDeTokens["Token"][j] == "abreChave":
            abreChave += 1

        if abreChave > 0:
            if tabelaDeTokens["Token"][j] == "pontoEVirgula":
                buffer += tabelaDeTokens["Lexema"][j] + "\n"
            elif tabelaDeTokens["Token"][j] == "fechaChave":
                fechaChave += 1
                if abreChave == fechaChave:
                    if tabelaDeTokens["Lexema"][j] != '}':
                        buffer += tabelaDeTokens["Lexema"][j] + " "
                    buffer += "EndFunc;\n"
                    arquivo.write(buffer)
                    break
            elif tabelaDeTokens["Token"][j] != "abreChave":
                buffer += tabelaDeTokens["Lexema"][j] + " "
                arquivo.write(buffer)
                buffer = ""

    return j, qtdLabel

def gerarBlocoChamadaFuncao(arquivo, tabelaDeTokens, posicao, qtdLabel, linha):
    posicaoInicioArgumentos = posicao + 2
    posicaoAposArgumentos = -1
    argumentos = []
    qtdArgumentos = 0
    buffer = linha + "call " + tabelaDeTokens["Lexema"][posicao] + ", "
    
    for j in range(posicaoInicioArgumentos, len(tabelaDeTokens)):
        if tabelaDeTokens["Token"][j] == "fechaParentese":
            posicaoAposArgumentos = j + 1
            break
        elif tabelaDeTokens["Token"][j] == "idVariavel":
            argumentos.append(tabelaDeTokens["Lexema"][j])
            qtdArgumentos += 1
    
    buffer += str(qtdArgumentos) + ";\n"
    for j in range((len(argumentos)-1), -1, -1):
        arquivo.write("param " + argumentos[j] + "\n")
    arquivo.write(buffer)
    linha = ""

    return posicaoAposArgumentos, qtdLabel, linha

def gerarBlocoDeclaracaoProcedimento(arquivo, tabelaDeTokens, posicao, qtdLabel):
    posicaoProximoToken = 0
    abreChave = 0
    fechaChave = 0
    ultimaPosicaoProcessada = -1
    for j in range(posicao, len(tabelaDeTokens)):
        if tabelaDeTokens["Token"][j] == "idProcedimento":
            linha = tabelaDeTokens["Lexema"][j] + ":\nBeginProc;\n"
            arquivo.write(linha)
            linha = ""
        elif tabelaDeTokens["Token"][j] == "abreChave":
            posicaoProximoToken = j + 1
            ultimaPosicaoProcessada = j
            abreChave += 1
            break
    
    for j in range(posicaoProximoToken, len(tabelaDeTokens)):
        if ultimaPosicaoProcessada >= j:
            continue

        if tabelaDeTokens["Token"][j] == "pontoEVirgula" or tabelaDeTokens["Token"][j] == "abreChave" or tabelaDeTokens["Token"][j] == "fechaChave":
            if tabelaDeTokens["Token"][j] == "abreChave":
                abreChave += 1
            if tabelaDeTokens["Token"][j] == "fechaChave":
                fechaChave += 1
                if abreChave <= fechaChave:
                    ultimaPosicaoProcessada = j
                    linha1 = "EndProc;\n"
                    arquivo.write(linha1)
                    linha1 = ""
                    break
            linha += tabelaDeTokens["Lexema"][j] + "\n"
            arquivo.write(linha)
            linha = ""
            ultimaPosicaoProcessada = j
            continue

        elif tabelaDeTokens["Token"][j] == "laco":
            qtdLabel+= 1
            ultimaPosicaoProcessada, qtdLabel = gerarBlocoLaco(arquivo, tabelaDeTokens, j, qtdLabel)
            continue
        
        linha += tabelaDeTokens["Lexema"][j] + " "
    return ultimaPosicaoProcessada, qtdLabel
            
def gerarBlocoChamadaProcedimento(arquivo, tabelaDeTokens, posicao, qtdLabel, linha):
    posicaoInicioArgumentos = posicao + 2
    posicaoAposArgumentos = -1
    argumentos = []
    qntParametros = 0
    buffer = linha + "call " + tabelaDeTokens["Lexema"][posicao] + ", "
    
    for j in range(posicaoInicioArgumentos, len(tabelaDeTokens)):
        if tabelaDeTokens["Token"][j] == "fechaParentese":
            posicaoAposArgumentos = j + 1
            break
        elif tabelaDeTokens["Token"][j] == "idVariavel":
            argumentos.append(tabelaDeTokens["Lexema"][j])
            qntParametros += 1
    
    buffer += str(qntParametros) + ";\n"
    for j in range((len(argumentos)-1), -1, -1):
        arquivo.write("param " + argumentos[j] + "\n")
    arquivo.write(buffer)
    linha = ""

    return posicaoAposArgumentos, qtdLabel, linha

def gerarBlocoLaco(arquivo, tabelaDeTokens, posicao, qtdLabel):
    aux = -1
    label1 = "_L" + str(qtdLabel)
    linha = label1 + ": if "
    condicao = ""
    for j in range(posicao + 2, len(tabelaDeTokens)):
        if tabelaDeTokens["Token"][j] == "fechaParentese":
            aux = j + 1
            break

        if tabelaDeTokens["Token"][j] == "operadorRelacional":
            condicao += inverterOperador(tabelaDeTokens["Lexema"][j])
            continue

        condicao += tabelaDeTokens["Lexema"][j] + " "

    qtdLabel += 1
    label2 = "_L" + str(qtdLabel)
    condicao += "goto " + label2 + "\n"

    linha += condicao
    arquivo.write(linha)
    linha = ""
    
    abreChave = 1
    fechaChave = 0
    flag = False

    for j in range(aux + 1, len(tabelaDeTokens)):
        if aux >= j:
            continue
        
        if tabelaDeTokens["Token"][j] == "pontoEVirgula" or tabelaDeTokens["Token"][j] == "abreChave" or tabelaDeTokens["Token"][j] == "fechaChave":
            if tabelaDeTokens["Token"][j] == "abreChave":
                abreChave += 1
            if tabelaDeTokens["Token"][j] == "fechaChave":
                fechaChave += 1
                if abreChave <= fechaChave:
                    aux = j
                    flag = True
                    linha1 = "goto " + label1
                    arquivo.write(linha1)
                    linha1 = ""
                    break
            linha += tabelaDeTokens["Lexema"][j] + "\n"
            arquivo.write(linha)
            linha = ""
            aux = j
            continue
        elif tabelaDeTokens["Token"][j] == "laco":
            qtdLabel+= 1
            aux, qtdLabel = gerarBlocoLaco(arquivo, tabelaDeTokens, j, qtdLabel)
            continue

        elif tabelaDeTokens["Token"][j] == "funcao":
            info = gerarBlocoDeclaracaoFuncao(arquivo, tabelaDeTokens, j, qtdLabel)
            aux = info[0]
            qtdLabel = info[1]
            continue
    
        elif tabelaDeTokens["Token"][j] == "idFuncao":
            info = gerarBlocoChamadaFuncao(arquivo, tabelaDeTokens, j, qtdLabel, linha)
            aux = info[0]
            qtdLabel = info[1]
            linha = info[2]
            continue

        elif tabelaDeTokens["Token"][j] == "procedimento":
            info = gerarBlocoDeclaracaoProcedimento(arquivo, tabelaDeTokens, j, qtdLabel)
            aux = info[0]
            qtdLabel = info[1]
            continue

        elif tabelaDeTokens["Token"][j] == "idProcedimento":
            info = gerarBlocoChamadaProcedimento(arquivo, tabelaDeTokens, j, qtdLabel, linha)
            aux = info[0]
            qtdLabel = info[1]
            linha = info[2]
            continue
        
        linha += tabelaDeTokens["Lexema"][j] + " "

    linha = "\n" + label2 + ":"
    arquivo.write(linha)
    linha = ""
    
    if flag:
        return aux, qtdLabel, linha
    else:
        return len(tabelaDeTokens) - 1, qtdLabel, linha

def inverterOperador(operador):
    if operador == ">":
        return "<= "
    elif operador == "<":
        return ">= "
    elif operador == ">=":
        return "< "
    elif operador == "<=":
        return "> "
    elif operador == "==":
        return "!= "
    elif operador == "!=":
        return "== "