# Tipos de tokens
laco = ['while']
booleanos = ['true', 'false']
condicionais = ['if', 'else']
tipos = ['int', 'boolean']
constantes = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

caracteres = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
    ";", "(", ")", "{", "}", " ", "\n", ">", "<", 
    "=", "!", "+", "-", "*", "/", ","
]

operadoresLogicos = [">=", ">", "<", "<=", "!=", "=="]

operadoresAritmeticos = ["+", "-", "*", "/"]


#################### Funcoes de verificacao de caracteres ####################


# Verifica se o lexema e um operador aritmetico ou uma atribuicao
def operadoresAritmeticosAtribuicao(lexema):
    if lexema in operadoresAritmeticos:
        return "Operador Aritmetico"
    elif lexema == "=":
        return "Atribuicao"

# Verifica se o lexema e um operador logico    
def operadoresLogicos(lexema):
    if lexema in operadoresLogicos:
        return "Operador Logico"
