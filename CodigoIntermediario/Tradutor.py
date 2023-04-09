import ast

# Recebe uma lista de expressoes e traduz para codigo de 3 enderecos
def traduzirExpressoes(expressoes):
    # Analisa cada expressao e gera a arvore sintatica
    arvores = [ast.parse(expr, mode='eval') for expr in expressoes]

    # Gera o codigo de 3 endereços para cada expressao
    for i, arvore in enumerate(arvores):
        print(f"\nExpressao {i+1}: {expressoes[i]}")

        codigoTresEnderecos, qtdVarTemp = gerarCodigoTresEnderecos(arvore.body, qtdVarTemp=0)

        if(qtdVarTemp > 0):
            print(codigoTresEnderecos, end='')
            print(f"Quantidade de variaveis temporarias geradas: {qtdVarTemp}")

 # Gera o codigo de 3 endereços a partir da arvore sintatica
def gerarCodigoTresEnderecos(no, qtdVarTemp=0):
    codigo = ""
    if isinstance(no, ast.BinOp):
        temp1 = f"t{qtdVarTemp}"
        no.temp = qtdVarTemp  # adiciona o atributo 'temp' ao no
        qtdVarTemp += 1
        
        codigoDaEsquerda, qtdVarTemp = gerarCodigoTresEnderecos(no.left, qtdVarTemp)
        codigoDaDireita, qtdVarTemp = gerarCodigoTresEnderecos(no.right, qtdVarTemp)
        codigo += codigoDaEsquerda
        codigo += codigoDaDireita
        
        codigo += f"{temp1} = {obterExpressaoDoNo(no.left)} {obterOperadorDoNo(no.op)} {obterExpressaoDoNo(no.right)}\n"
        return codigo, qtdVarTemp
    elif isinstance(no, ast.Name):
        return "", qtdVarTemp
    elif isinstance(no, ast.Constant):
        return "", qtdVarTemp
    else:
        raise ValueError("Tipo de no invalido")

# Retorna a expressao de um no
def obterExpressaoDoNo(no):
    if isinstance(no, ast.BinOp):
        return f"t{no.temp}"
    elif isinstance(no, ast.Name):
        return no.id
    elif isinstance(no, ast.Constant):
        return str(no.value)
    else:
        raise ValueError("Tipo de no invalido")

# Retorna o operador de um no
def obterOperadorDoNo(no):
    if isinstance(no, ast.Add):
        return "+"
    elif isinstance(no, ast.Sub):
        return "-"
    elif isinstance(no, ast.Mult):
        return "*"
    elif isinstance(no, ast.Div):
        return "/"
    else:
        raise ValueError("Operador invalido")