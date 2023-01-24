
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

# Variáveis auxiliares
lexema = ""


# def analiseLexica(code):
    
def operadoresLogicos(lexema):
    if lexema == ">=":
        return "Operador Logico"
    elif lexema == ">":
        return "Operador Logico"
    elif lexema == "<":
        return "Operador Logico"
    elif lexema == "<=":
        return "Operador Logico"
    elif lexema == "!=":
        return "Operador Logico"
    elif lexema == "==":
        return "Operador Logico"