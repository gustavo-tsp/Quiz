#!/usr/bin/env python3
"""Quiz no Terminal 🎮

Um jogo de perguntas e respostas para rodar direto no terminal.
Sem dependências externas: só precisa do Python 3.8+.
"""

import json
import os
import random
import time
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
PERGUNTAS_ARQUIVO = BASE_DIR / "perguntas.json"
RANKING_ARQUIVO = BASE_DIR / "ranking.json"

PONTOS_POR_ACERTO = 10
BONUS_MAXIMO_VELOCIDADE = 5
TAMANHO_RANKING = 5

# Habilita cores ANSI no Windows 10+
if os.name == "nt":
    os.system("")


class Cor:
    VERDE = "\033[92m"
    VERMELHO = "\033[91m"
    AMARELO = "\033[93m"
    AZUL = "\033[94m"
    CIANO = "\033[96m"
    NEGRITO = "\033[1m"
    FIM = "\033[0m"


class SairDoJogo(Exception):
    """Lançada quando o jogador digita 'q' para sair."""


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input(f"\n{Cor.CIANO}Pressione ENTER para continuar...{Cor.FIM}")


def ler_entrada(texto):
    """Lê uma entrada; 'q' encerra o jogo."""
    resposta = input(texto).strip()
    if resposta.lower() == "q":
        raise SairDoJogo
    return resposta


# ---------------------------------------------------------------- dados
def carregar_perguntas():
    try:
        with open(PERGUNTAS_ARQUIVO, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo {PERGUNTAS_ARQUIVO.name} não encontrado.")
        raise SystemExit(1)
    except json.JSONDecodeError as erro:
        print(f"Erro de formatação em {PERGUNTAS_ARQUIVO.name}: {erro}")
        raise SystemExit(1)


def carregar_ranking():
    if not RANKING_ARQUIVO.exists():
        return []
    try:
        with open(RANKING_ARQUIVO, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def salvar_ranking(ranking):
    with open(RANKING_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- telas
def mostrar_titulo():
    limpar_tela()
    print(f"{Cor.AZUL}{Cor.NEGRITO}")
    print("╔══════════════════════════════════════╗")
    print("║          🎮  QUIZ NO TERMINAL        ║")
    print("╚══════════════════════════════════════╝")
    print(Cor.FIM)


def menu_principal():
    mostrar_titulo()
    print("  1) Jogar")
    print("  2) Ver ranking")
    print("  3) Sair")
    return input("\nEscolha uma opção: ").strip()


def escolher_categoria(perguntas):
    categorias = sorted({p["categoria"] for p in perguntas})
    mostrar_titulo()
    print("Escolha uma categoria:\n")
    for i, cat in enumerate(categorias, 1):
        qtd = sum(1 for p in perguntas if p["categoria"] == cat)
        print(f"  {i}) {cat} ({qtd} perguntas)")
    print(f"  {len(categorias) + 1}) Todas misturadas")
    print("\n(digite 'q' a qualquer momento para sair)")

    while True:
        escolha = ler_entrada("\nCategoria: ")
        if escolha.isdigit():
            n = int(escolha)
            if 1 <= n <= len(categorias):
                return categorias[n - 1]
            if n == len(categorias) + 1:
                return None
        print(f"{Cor.VERMELHO}Opção inválida.{Cor.FIM}")


def escolher_quantidade(maximo):
    padrao = min(5, maximo)
    while True:
        escolha = ler_entrada(f"Quantas perguntas? (1-{maximo}, ENTER = {padrao}): ")
        if escolha == "":
            return padrao
        if escolha.isdigit() and 1 <= int(escolha) <= maximo:
            return int(escolha)
        print(f"{Cor.VERMELHO}Digite um número entre 1 e {maximo}.{Cor.FIM}")


def mostrar_ranking():
    mostrar_titulo()
    ranking = carregar_ranking()
    print(f"{Cor.AMARELO}{Cor.NEGRITO}🏆 TOP {TAMANHO_RANKING}{Cor.FIM}\n")
    if not ranking:
        print("Nenhuma partida registrada ainda. Seja o primeiro!")
    else:
        medalhas = ["🥇", "🥈", "🥉"]
        for i, r in enumerate(ranking, 1):
            icone = medalhas[i - 1] if i <= 3 else f"{i}º"
            print(
                f" {icone}  {r['nome']:<15} {r['pontos']:>4} pts  "
                f"({r['acertos']}/{r['total']})  {r['categoria']}  {r['data']}"
            )
    pausar()


# ---------------------------------------------------------------- jogo
def fazer_pergunta(numero, total, pergunta):
    """Exibe a pergunta e devolve (acertou, tempo_em_segundos)."""
    opcoes = pergunta["opcoes"][:]
    correta = pergunta["opcoes"][pergunta["resposta"]]
    random.shuffle(opcoes)
    indice_correto = opcoes.index(correta)

    print(f"{Cor.CIANO}Pergunta {numero}/{total}  •  {pergunta['categoria']}{Cor.FIM}")
    print(f"\n{Cor.NEGRITO}{pergunta['pergunta']}{Cor.FIM}\n")
    for i, op in enumerate(opcoes, 1):
        print(f"  {i}) {op}")

    inicio = time.time()
    while True:
        escolha = ler_entrada("\nSua resposta: ")
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            break
        print(f"{Cor.VERMELHO}Digite um número de 1 a {len(opcoes)}.{Cor.FIM}")
    tempo = time.time() - inicio

    acertou = int(escolha) - 1 == indice_correto
    if acertou:
        print(f"\n{Cor.VERDE}✔ Correto!{Cor.FIM}")
    else:
        print(f"\n{Cor.VERMELHO}✘ Errado.{Cor.FIM} A resposta certa era: "
              f"{Cor.VERDE}{correta}{Cor.FIM}")
    return acertou, tempo


def calcular_pontos(tempo):
    bonus = max(0, BONUS_MAXIMO_VELOCIDADE - int(tempo // 2))
    return PONTOS_POR_ACERTO + bonus, bonus


def registrar_no_ranking(nome, pontos, acertos, total, categoria):
    ranking = carregar_ranking()
    ranking.append({
        "nome": nome,
        "pontos": pontos,
        "acertos": acertos,
        "total": total,
        "categoria": categoria or "Todas",
        "data": datetime.now().strftime("%d/%m/%Y"),
    })
    ranking.sort(key=lambda r: r["pontos"], reverse=True)
    salvar_ranking(ranking[:TAMANHO_RANKING])


def mensagem_final(acertos, total):
    percentual = acertos / total
    if percentual == 1:
        return "🏆 Perfeito! Você mandou muito bem!"
    if percentual >= 0.7:
        return "😎 Ótimo resultado!"
    if percentual >= 0.4:
        return "🙂 Nada mal, dá pra melhorar!"
    return "📚 Hora de estudar um pouco mais!"


def jogar(perguntas):
    categoria = escolher_categoria(perguntas)
    banco = [p for p in perguntas if categoria is None or p["categoria"] == categoria]
    quantidade = escolher_quantidade(len(banco))
    nome = ler_entrada("Seu nome: ")[:15] or "Anônimo"

    rodada = random.sample(banco, quantidade)
    pontos = acertos = 0

    for i, pergunta in enumerate(rodada, 1):
        mostrar_titulo()
        print(f"{Cor.AMARELO}Pontos: {pontos}{Cor.FIM}\n")
        acertou, tempo = fazer_pergunta(i, quantidade, pergunta)
        if acertou:
            ganho, bonus = calcular_pontos(tempo)
            pontos += ganho
            acertos += 1
            extra = f" (+{bonus} de bônus de velocidade ⚡)" if bonus else ""
            print(f"+{ganho} pontos{extra}")
        pausar()

    mostrar_titulo()
    print(f"{Cor.NEGRITO}Fim de jogo, {nome}!{Cor.FIM}\n")
    print(f"Acertos: {acertos}/{quantidade}")
    print(f"Pontuação: {Cor.AMARELO}{pontos}{Cor.FIM}")
    print(f"\n{mensagem_final(acertos, quantidade)}")
    registrar_no_ranking(nome, pontos, acertos, quantidade, categoria)
    pausar()


def main():
    perguntas = carregar_perguntas()
    try:
        while True:
            opcao = menu_principal()
            if opcao == "1":
                jogar(perguntas)
            elif opcao == "2":
                mostrar_ranking()
            elif opcao == "3":
                break
            else:
                print(f"{Cor.VERMELHO}Opção inválida.{Cor.FIM}")
                time.sleep(1)
    except (SairDoJogo, KeyboardInterrupt, EOFError):
        pass
    print("\nValeu por jogar! 👋")


if __name__ == "__main__":
    main()
