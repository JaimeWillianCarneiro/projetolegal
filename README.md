# Autenticação

Projeto de autenticação de Usuário utilizado o framework Flask.

```python

from calculadora import Calculadora



calc = Calculadora()


# Exemplo de Soma
print('1 + 2 é igual a:')
print(calc.soma(1, 2))
print()
# Exemplo de Multiplicação

print('43 vezes 47 é igual a: ')
print(calc.multiplicacao(43, 47))
print()

# Exemplo de divisão válida
print('43 dividido por 47 é igual a:')
print(calc.divisao(43, 47))
print()


# Exemplo de divisão inválida
print('43 dividido por 0 é igual a:')
print(calc.divisao(43, 0))
print()
```
