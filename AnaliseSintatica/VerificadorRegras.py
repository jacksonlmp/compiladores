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