# Projeto de compiladores 💻
Disciplina de Compiladores, ministrada pela professora Maria Sibaldo na UFAPE, referente ao período de 2022.1. 

## Sobre o projeto 📑
Implementação de um compilador, com linguagem de livre escolha, com uso de gramática preditiva.

A linguagem escolhida para desenvolvimento foi python, na versão 3.9.5.

## Objetivo ✅
Seu intuito é a prática dos conhecimentos teóricos vistos em aula, para a verificação de aprendizagem.

## Sobre a gramática 📒
A gramática deve ser LL1 (podem ser analisadas por um simples parser descentente recursivo), ou seja, seguir estes requisitos:
+ Fatorada à esquerda;
+ Sem recursão à esquerda.

Ademais, deve possuir apenas 1 símbolo de look-ahead.

## Sobre a linguagem 📖
A linguagem deve cobrir os seguintes aspectos:
1. Declaração de variáveis de tipo inteiro e booleano;
2. Declaração de procedimentos e funções (sem e com parâmetros);
3. Comandos de atribuição;
4. Chamada de procedimentos e funções;
5. Comando de desvio condicional (if e else);
6. Comando de laço (while);
7. Comando de retorno de valor;
8. Comandos de desvio incondicional (break e continue);
9. Comando de impressão de constante e variável na tela;
10. Expressões aritméticas (+, -, * e /);
11. Expressões booleanas (==, !=, >, >=, < e <=).

## Integrantes 👦
+   [Jackson Lima](https://github.com/jacksonlmp)
+   [Thiago Cavalcanti](https://github.com/ThiagoCavalcantiSilva)

## Para rodar 🎡
+ Utilize o Python na versão 3.9.5 ou superior.
+ Instale o pandas (para criar os dataframes) e também o tabulate (formatação das tabelas):
    - pip install pandas
    - pip install tabulate
+ Execute o arquivo Main.py.

## Testes - Léxicos e sintáticos
- [x] - Utilização de operadores de comparação
- [x] - Erros de digitação (whle, it, bolean)
- [x] - if x > 0 or and y < 10
- [x] - if x > y + z:
- [x] - Colocar vírgulas aleatórias dentro de funções, procedimentos, while
- [x] - Inverter ordem de parâmetros: declaracaoDeFuncao(variavel tipo)
- [x] - chamadaDeFuncao(int) -> em vez de chamadaDeFuncao(10 ou idVariavel)
- [x] - Adicionar múltiplos ponto e vírgula
- [x] - Declaração de variável sem ponto e vírgula
- [x] - Verificar int vA = + 10;
- [x] - int vA = 2 + * 5;
- [x] - int vA = 10 2 +;

## Testes - Semânticos
- [X] - Chamar procedimento/função que não tenha sido declarado ainda;
- [X] - Chamar procedimento/função inexistente;
- [ ] - Atribuir retorno de função booleana à variável inteira;
- [ ] - Atribuir retorno de função inteira à variável booleano;
- [ ] - Atribuir valor booleano à variável inteira;
- [ ] - Atribuir valor inteiro à variável booleana;
- [ ] - Passar valor inteiro como argumento em vez de booleano;
- [ ] - Passar valor booleano como argumento em vez de inteiro;
- [ ] - Comparar inteiro com booleano;
- [ ] - Usar variável de uma função/procedimento fora do seu escopo.