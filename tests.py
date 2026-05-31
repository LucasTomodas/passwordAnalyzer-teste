"""
Testes unitários para o Password Strength Analyzer.
Execute com: python -m pytest tests.py -v
"""

import pytest
from analyzer import analisar_senha, gerar_senha_forte, calcular_entropia


class TestAnalisarSenha:

    def test_senha_comum_retorna_zero(self):
        resultado = analisar_senha("123456")
        assert resultado["pontuacao"] == 0
        assert "PÉSSIMA" in resultado["forca"]

    def test_senha_forte(self):
        resultado = analisar_senha("X#9kLm@2vPqR!5wZ")
        assert resultado["pontuacao"] >= 80
        assert "FORTE" in resultado["forca"]

    def test_senha_sem_maiuscula(self):
        resultado = analisar_senha("minhasenha123!")
        sugestoes = " ".join(resultado["sugestoes"]).lower()
        assert "maiúscula" in sugestoes or "maiuscula" in sugestoes

    def test_senha_sem_simbolo(self):
        resultado = analisar_senha("MinhaSenha123")
        sugestoes = " ".join(resultado["sugestoes"]).lower()
        assert "símbolo" in sugestoes or "simbolo" in sugestoes

    def test_senha_curta(self):
        resultado = analisar_senha("Ab1!")
        sugestoes = " ".join(resultado["sugestoes"]).lower()
        assert "caractere" in sugestoes

    def test_senha_com_repeticao(self):
        resultado = analisar_senha("Senha!!!111aaa")
        detalhes = " ".join(resultado["detalhes"]).lower()
        assert "repetido" in detalhes

    def test_senha_com_sequencia(self):
        resultado = analisar_senha("Abc123456!qwerty")
        detalhes = " ".join(resultado["detalhes"]).lower()
        assert "sequência" in detalhes or "sequencia" in detalhes


class TestGerarSenha:

    def test_tamanho_padrao(self):
        senha = gerar_senha_forte()
        assert len(senha) == 16

    def test_tamanho_customizado(self):
        senha = gerar_senha_forte(24)
        assert len(senha) == 24

    def test_senha_gerada_e_forte(self):
        senha = gerar_senha_forte()
        resultado = analisar_senha(senha)
        assert resultado["pontuacao"] >= 80

    def test_senha_tem_todos_tipos(self):
        import re
        for _ in range(10):
            senha = gerar_senha_forte()
            assert re.search(r"[a-z]", senha)
            assert re.search(r"[A-Z]", senha)
            assert re.search(r"[0-9]", senha)
            assert re.search(r"[!@#$%&*_\-]", senha)


class TestEntropia:

    def test_entropia_senha_vazia(self):
        assert calcular_entropia("") == 0.0

    def test_entropia_maior_com_simbolos(self):
        sem_simbolo = calcular_entropia("Abcdef123456")
        com_simbolo = calcular_entropia("Abcdef12345!")
        assert com_simbolo > sem_simbolo

    def test_entropia_maior_com_tamanho(self):
        curta = calcular_entropia("Abc1!")
        longa = calcular_entropia("Abcdefgh1234!")
        assert longa > curta
