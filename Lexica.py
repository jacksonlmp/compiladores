# Tipos de variáveis
laco = ['while']
boolean = ['true', 'false']
condicionais = ['if', 'else']
tipos = ['int', 'boolean']
constante = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

caracteres = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
    ";", "(", ")", "{", "}", " ", "\n", ">", "<", 
    "=", "!", "+", "-", "*", "/", ","
]

listaOperadoresLogicos = [">=", ">", "<", "<=", "!=", "=="]

listaOperadoresAritmeticos = ["+", "-", "*", "/"]

# Variáveis auxiliares
lexema = ""

# Lista para armazenas Tokens
tokens = []


def analiseLexica(code):
    #Implementar
    return


# Verifica se o lexema é um operador aritmético ou uma atribuiçaõ    
def operadoresAritmeticosAtribuicao(lexema):
    if lexema in listaOperadoresAritmeticos:
        return "Operador Aritmetico"
    elif lexema == "=":
        return "Atribuicao"

    
# Verifica se o lexema é um operador lógico    
def operadoresLogicos(lexema):
    if lexema in listaOperadoresLogicos:
        return "Operador Logico"