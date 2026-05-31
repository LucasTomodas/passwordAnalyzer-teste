#!/usr/bin/env python3
"""
Password Strength Analyzer
Analisa a força de senhas e sugere melhorias.
"""

import re
import math
import secrets
import string
import argparse
import os


# Lista de senhas mais comuns (simplificada — em produção, use rockyou.txt)
COMMON_PASSWORDS = {
    "123456", "password", "123456789", "12345678", "12345", "1234567",
    "1234567890", "qwerty", "abc123", "111111", "password1", "iloveyou",
    "admin", "letmein", "monkey", "1234", "senha", "123123", "dragon",
    "master", "hello", "login", "welcome", "solo", "princess", "passw0rd",
    "senha123", "brasil", "flamengo", "corinthians"
}


def calcular_entropia(senha: str) -> float:
    """Calcula a entropia da senha em bits."""
    charset = 0
    if re.search(r"[a-z]", senha):
        charset += 26
    if re.search(r"[A-Z]", senha):
        charset += 26
    if re.search(r"[0-9]", senha):
        charset += 10
    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]", senha):
        charset += 32

    if charset == 0:
        return 0.0
    return len(senha) * math.log2(charset)


def analisar_senha(senha: str) -> dict:
    """Analisa a senha e retorna um dicionário com os resultados."""
    resultado = {
        "senha": senha,
        "pontuacao": 0,
        "forca": "",
        "detalhes": [],
        "sugestoes": [],
        "entropia": 0.0,
    }

    pontos = 0

    # Verificar se é senha comum
    if senha.lower() in COMMON_PASSWORDS:
        resultado["detalhes"].append("❌ Senha está na lista das mais usadas (vazadas)")
        resultado["sugestoes"].append("Evite senhas comuns como 'senha123' ou 'qwerty'")
        resultado["forca"] = "☠️  PÉSSIMA"
        resultado["pontuacao"] = 0
        return resultado

    # Comprimento
    if len(senha) >= 16:
        pontos += 30
        resultado["detalhes"].append("✅ Comprimento excelente (16+ caracteres)")
    elif len(senha) >= 12:
        pontos += 20
        resultado["detalhes"].append("✅ Comprimento bom (12–15 caracteres)")
    elif len(senha) >= 8:
        pontos += 10
        resultado["detalhes"].append("⚠️  Comprimento aceitável (8–11 caracteres)")
        resultado["sugestoes"].append("Aumente para pelo menos 12 caracteres")
    else:
        resultado["detalhes"].append("❌ Senha muito curta (menos de 8 caracteres)")
        resultado["sugestoes"].append("Use no mínimo 8 caracteres, idealmente 12+")

    # Letras minúsculas
    if re.search(r"[a-z]", senha):
        pontos += 10
        resultado["detalhes"].append("✅ Contém letras minúsculas")
    else:
        resultado["detalhes"].append("❌ Sem letras minúsculas")
        resultado["sugestoes"].append("Adicione letras minúsculas (a-z)")

    # Letras maiúsculas
    if re.search(r"[A-Z]", senha):
        pontos += 20
        resultado["detalhes"].append("✅ Contém letras maiúsculas")
    else:
        resultado["detalhes"].append("❌ Sem letras maiúsculas")
        resultado["sugestoes"].append("Adicione letras maiúsculas (A-Z)")

    # Números
    if re.search(r"[0-9]", senha):
        pontos += 20
        resultado["detalhes"].append("✅ Contém números")
    else:
        resultado["detalhes"].append("❌ Sem números")
        resultado["sugestoes"].append("Adicione pelo menos um número")

    # Símbolos especiais
    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]", senha):
        pontos += 20
        resultado["detalhes"].append("✅ Contém símbolos especiais")
    else:
        resultado["detalhes"].append("❌ Sem símbolos especiais")
        resultado["sugestoes"].append("Adicione símbolos como !@#$%&*")

    # Padrões previsíveis
    if re.search(r"(.)\1{2,}", senha):
        pontos -= 10
        resultado["detalhes"].append("⚠️  Contém caracteres repetidos (aaa, 111...)")
        resultado["sugestoes"].append("Evite repetir o mesmo caractere consecutivamente")

    if re.search(r"(012|123|234|345|456|567|678|789|890|abc|bcd|cde|qwe|asd)", senha.lower()):
        pontos -= 10
        resultado["detalhes"].append("⚠️  Contém sequências previsíveis (123, abc, qwe...)")
        resultado["sugestoes"].append("Evite sequências de teclado ou numéricas")

    # Entropia
    entropia = calcular_entropia(senha)
    resultado["entropia"] = round(entropia, 2)

    if entropia >= 60:
        pontos += 10
        resultado["detalhes"].append(f"✅ Entropia alta ({entropia:.1f} bits)")
    elif entropia >= 40:
        resultado["detalhes"].append(f"⚠️  Entropia média ({entropia:.1f} bits)")
    else:
        resultado["detalhes"].append(f"❌ Entropia baixa ({entropia:.1f} bits)")

    # Garantir que pontuação fique entre 0 e 100
    pontos = max(0, min(100, pontos))
    resultado["pontuacao"] = pontos

    # Classificar força
    if pontos >= 80:
        resultado["forca"] = "🟢 FORTE"
    elif pontos >= 60:
        resultado["forca"] = "🟡 MÉDIA"
    elif pontos >= 40:
        resultado["forca"] = "🟠 FRACA"
    else:
        resultado["forca"] = "🔴 MUITO FRACA"

    return resultado


def gerar_senha_forte(tamanho: int = 16) -> str:
    """Gera uma senha forte e aleatória."""
    alfabeto = string.ascii_letters + string.digits + "!@#$%&*_-"
    while True:
        senha = "".join(secrets.choice(alfabeto) for _ in range(tamanho))
        # Garante que a senha gerada tem todos os tipos de caractere
        if (re.search(r"[a-z]", senha) and
                re.search(r"[A-Z]", senha) and
                re.search(r"[0-9]", senha) and
                re.search(r"[!@#$%&*_\-]", senha)):
            return senha


def barra_progresso(pontuacao: int, largura: int = 30) -> str:
    """Gera uma barra de progresso visual."""
    preenchido = int((pontuacao / 100) * largura)
    vazio = largura - preenchido

    if pontuacao >= 80:
        cor = "\033[92m"   # Verde
    elif pontuacao >= 60:
        cor = "\033[93m"   # Amarelo
    elif pontuacao >= 40:
        cor = "\033[33m"   # Laranja
    else:
        cor = "\033[91m"   # Vermelho

    reset = "\033[0m"
    barra = f"{cor}{'█' * preenchido}{'░' * vazio}{reset}"
    return f"[{barra}] {pontuacao}/100"


def exibir_resultado(resultado: dict):
    """Exibe o resultado da análise no terminal."""
    print("\n" + "═" * 50)
    print("       🔐 PASSWORD STRENGTH ANALYZER")
    print("═" * 50)

    print(f"\n📋 Senha analisada : {'*' * len(resultado['senha'])}")
    print(f"💪 Força           : {resultado['forca']}")
    print(f"📊 Pontuação       : {barra_progresso(resultado['pontuacao'])}")
    print(f"🎲 Entropia        : {resultado['entropia']} bits")

    print("\n─── Detalhes ───────────────────────────────")
    for detalhe in resultado["detalhes"]:
        print(f"  {detalhe}")

    if resultado["sugestoes"]:
        print("\n─── Sugestões de Melhoria ──────────────────")
        for i, sugestao in enumerate(resultado["sugestoes"], 1):
            print(f"  {i}. {sugestao}")

    print("\n" + "═" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="🔐 Analisa a força de uma senha",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python analyzer.py -p "MinhaS3nh@"
  python analyzer.py -p "abc123"
  python analyzer.py --gerar
  python analyzer.py --gerar --tamanho 20
        """
    )

    parser.add_argument(
        "-p", "--password",
        type=str,
        help="Senha a ser analisada"
    )
    parser.add_argument(
        "--gerar",
        action="store_true",
        help="Gera uma senha forte aleatória"
    )
    parser.add_argument(
        "--tamanho",
        type=int,
        default=16,
        help="Tamanho da senha gerada (padrão: 16)"
    )

    args = parser.parse_args()

    if args.gerar:
        senha_gerada = gerar_senha_forte(args.tamanho)
        print(f"\n✨ Senha gerada: \033[92m{senha_gerada}\033[0m")
        resultado = analisar_senha(senha_gerada)
        exibir_resultado(resultado)

    elif args.password:
        resultado = analisar_senha(args.password)
        exibir_resultado(resultado)

    else:
        # Modo interativo
        print("\n🔐 Password Strength Analyzer")
        print("─────────────────────────────")
        senha = input("Digite a senha para analisar: ")
        if not senha:
            print("❌ Nenhuma senha informada.")
            return
        resultado = analisar_senha(senha)
        exibir_resultado(resultado)


if __name__ == "__main__":
    main()
