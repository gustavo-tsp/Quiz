# py-c-demo

Projeto simples que mostra **C e Python trabalhando juntos**: as funções
matemáticas são escritas em C, compiladas como biblioteca compartilhada e
chamadas pelo Python usando `ctypes`.

## Estrutura

```
py-c-demo/
├── c/
│   ├── mathlib.c      # implementação das funções
│   ├── mathlib.h      # declarações
│   └── main.c         # programa C standalone
├── python/
│   ├── mathlib.py     # wrapper ctypes
│   └── main.py        # programa Python que usa a lib C
├── tests/
│   └── test_mathlib.py
├── Makefile
└── README.md
```

## Requisitos

- `gcc` e `make`
- Python 3.8+

## Como usar

```bash
make          # compila a biblioteca e o programa C
make run-c    # roda a versão em C
make run-py   # roda a versão em Python (chamando C)
make test     # roda os testes
make clean    # limpa a pasta build
```

## Funções disponíveis

| Função | Descrição |
|---|---|
| `add(a, b)` | soma dois inteiros |
| `factorial(n)` | fatorial de `n` |
| `is_prime(n)` | verifica se `n` é primo |
| `average(valores)` | média de uma lista de números |
