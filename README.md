# 🎮 Quiz no Terminal

Um jogo de perguntas e respostas feito em Python para rodar direto no terminal.
Sem dependências externas.

## Funcionalidades

- Perguntas separadas por categoria (ou todas misturadas)
- Você escolhe quantas perguntas quer responder
- Alternativas embaralhadas a cada rodada
- Pontuação com **bônus de velocidade** ⚡
- Ranking Top 5 salvo localmente
- Cores no terminal e feedback imediato de acerto/erro
- Banco de perguntas em JSON, fácil de editar

##  Como rodar

Requisito: Python 3.8 ou superior.

```bash
git clone https://github.com/SEU-USUARIO/quiz-terminal.git
cd quiz-terminal
python quiz.py
```

No Linux/macOS, se `python` não funcionar, use `python3 quiz.py`.

Durante o jogo, digite `q` a qualquer momento para sair.

## ➕ Como adicionar perguntas

Edite o arquivo `perguntas.json` e adicione um objeto neste formato:

```json
{
  "categoria": "Programação",
  "pergunta": "Qual comando lista os arquivos de uma pasta no Linux?",
  "opcoes": ["ls", "cd", "rm", "mv"],
  "resposta": 0
}
```

- `opcoes`: lista de alternativas (as posições são embaralhadas durante o jogo)
- `resposta`: índice da alternativa correta, **começando do zero** (`0` = primeira opção)
- Categorias novas aparecem automaticamente no menu

## Pontuação

- Cada acerto vale **10 pontos**
- Responder rápido dá até **+5 de bônus** (5 pontos em menos de 2s, caindo 1 ponto a cada 2s)

## Estrutura

```
quiz-terminal/
├── quiz.py          # lógica do jogo
├── perguntas.json   # banco de perguntas
├── ranking.json     # criado automaticamente (ignorado pelo Git)
└── README.md
```

## Ideias para evoluir

- Limite de tempo por pergunta
- Níveis de dificuldade
- Importar perguntas de uma API
- Modo multijogador local
