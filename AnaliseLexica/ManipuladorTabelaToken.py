import pandas as pd

palavrasReservadas = {
    "while": "laço",
    "if": "if",
    "else": "else",
    "int" : "tipo",
    "boolean": "tipo",
    "func": "funcao",
    "return": "return",
    "print": "print",
    "proc": "procedimento",
    "break": "auxLaco",
    "continue": "auxLaco"
}

def verificarToken(lexema, numeroLinha):
    if(lexema == ''):
        return ''
    else:
        tokens = palavrasReservadas.get(lexema)
        if tokens:
            return tokens
        elif lexema[0] == 'v':
            return 'idVariavel'
        elif lexema[0] == 'f':
            return 'idFuncao'
        elif lexema[0] == 'p':
            return 'idProcedimento'
        else:
            try:
                constante = int(lexema)
                return "constante"
            except:
                print("="*25)
                print("Erro lexico na linha "+ str(numeroLinha))
                print("Lexema '"+ lexema +"' invalido.")
                print("="*25)
                exit()

# Salva o token na tabela
def inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token=None):
    if lexema:
        if not token:
            token = verificarToken(lexema, numeroDaLinhaAtual)
        tabelaDeTokens.loc[len(tabelaDeTokens)] = [token, lexema, numeroDaLinhaAtual]
    lexema = ""