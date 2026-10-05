# 🌉 Ponte

> Uma ponte simples entre **C** e **Python**: o C faz o trabalho pesado, o Python entrega a conveniência.

Ponte é um projeto didático que mostra, na prática, como escrever funções em C, compilá-las como biblioteca compartilhada e usá-las diretamente em Python com `ctypes`, sem dependências externas.

## Por que existe

C é rápido e ótimo para cálculos. Python é prático para escrever, testar e integrar. Este projeto junta os dois com o menor código possível, servindo de ponto de partida para quem quer aprender a integração ou criar o próprio módulo híbrido.

## Estrutura

```
ponte/
├── c/
│   ├── mathlib.c      # implementação das funções em C
│   ├── mathlib.h      # declarações (cabeçalho)
│   └── main.c         # programa C standalone
├── python/
│   ├── mathlib.py     # wrapper em Python (ctypes)
│   └── main.py        # exemplo de uso
├── tests/
│   └── test_mathlib.py
├── Makefile
└── README.md
```

## Requisitos

- `gcc` e `make`
- Python 3.8 ou superior

No Windows, use o WSL ou o MinGW para rodar o `Makefile`.

## Como usar

```bash
make          # compila a biblioteca (.so/.dylib) e o programa C
make run-c    # executa a versão em C
make run-py   # executa a versão em Python chamando a lib C
make test     # roda os testes
make clean    # remove a pasta build
```

## Funções disponíveis

| Função | Descrição |
|---|---|
| `add(a, b)` | soma dois inteiros |
| `factorial(n)` | fatorial de `n` (erro se `n < 0`) |
| `is_prime(n)` | verifica se `n` é primo |
| `average(valores)` | média de uma lista de números |

## Exemplo em Python

```python
from mathlib import add, factorial, is_prime, average

print(add(2, 3))                    # 5
print(factorial(5))                 # 120
print(is_prime(17))                 # True
print(average([7.5, 8.0, 9.5, 6.0]))  # 7.75
```

## Como funciona

1. O `Makefile` compila `c/mathlib.c` como biblioteca compartilhada em `build/`.
2. O `python/mathlib.py` carrega essa biblioteca com `ctypes.CDLL`.
3. Cada função C tem seus tipos de argumento e retorno declarados (`argtypes` e `restype`), e o wrapper expõe tudo como funções Python normais.

## Adicionando uma nova função

1. Declare em `c/mathlib.h` e implemente em `c/mathlib.c`.
2. Registre os tipos e crie o wrapper em `python/mathlib.py`.
3. Adicione um teste em `tests/test_mathlib.py`.
4. Rode `make test`.

## Ideias para evoluir

- Trocar `ctypes` por uma extensão C da API do Python ou por `cffi`
- Adicionar mais funções (ordenação, estatísticas, strings)
- Medir o ganho de desempenho em relação ao Python puro
