# Dicionário de Dados Database YETI

AUTHOR: Gabriela Dellamora Paim

VERSION: 1.0.3

## **DATA**
    Type: DATETIME

    Description: Data que o cliente preenche.

## **TIPO**
    Type: int8

    Description: Tipo de operação.
    0 - Entrada;
    1 - Saída.

## **CATEGORIA**
    Type: int16

    Description: Categoria de saída ou entrada:
    == Saída ==
     0 - Casa;
     1 - Transporte;
     2 - Alimentação;
     3 - Saúde;
     4 - Lazer;
     5 - Educação;
     20 - Outro.
     
    == Entrada ==
    0 - Salário;
    1 - Bonificação;
    2 - Auxílio;
    3 - Comissão;
    4 - 13º Salário;
    20 - Outro.


## **DESCRICAO**
    Type: String

    Description: Descrição do cliente sobre o gasto descrito.

## **VALOR**
    Type: float

    Description: Valor da operação.

## **SYSTEM_DATE**
    Type: DATETIME

    Description: Data de recebimento dos dados no dataframe.

**Referência:**

[xpeducação: Como classificar gastos pessoais](https://blog.xpeducacao.com.br/como-classificar-gastos-pessoais/)

