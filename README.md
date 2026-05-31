 Password Strength Analyzer teste

Ferramenta CLI em Python para analisar a força de senhas e identificar vulnerabilidades comuns.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Security](https://img.shields.io/badge/Topic-Cybersecurity-red?style=flat-square)

---

  Funcionalidades

- ✅ Verifica comprimento, complexidade e diversidade de caracteres
- ✅ Detecta senhas comuns e vazadas
- ✅ Identifica padrões previsíveis (sequências, repetições)
- ✅ Calcula a **entropia** da senha em bits
- ✅ Exibe pontuação de 0 a 100 com barra de progresso colorida
- ✅ Sugere melhorias específicas
- ✅ Gera senhas fortes e seguras com `secrets`
- ✅ Testes unitários incluídos

---

##  Demo

```
═══════════════════════════════════════════════════
        PASSWORD STRENGTH ANALYZER
═══════════════════════════════════════════════════

 Senha analisada : ****************
 Força           : 🟢 FORTE
Pontuação       : [██████████████████████████░░░░] 87/100
 Entropia        : 104.1 bits

─── Detalhes ───────────────────────────────────────
  ✅ Comprimento excelente (16+ caracteres)
  ✅ Contém letras minúsculas
  ✅ Contém letras maiúsculas
  ✅ Contém números
  ✅ Contém símbolos especiais
  ✅ Entropia alta (104.1 bits)

═══════════════════════════════════════════════════
```

---

 Como usar

 Pré-requisitos

 Python 3.8+

 Instalação

```bash
git clone https://github.com/seu-usuario/password-analyzer.git
cd password-analyzer
```

### Analisar uma senha

```bash
python analyzer.py -p "SuaSenhaAqui@123"
```

### Modo interativo

```bash
python analyzer.py
```

### Gerar uma senha forte

```bash
python analyzer.py --gerar
```

### Gerar senha com tamanho customizado

```bash
python analyzer.py --gerar --tamanho 20
```

---

##  Testes

```bash
pip install pytest
python -m pytest tests.py -v
```

---

 Critérios de Avaliação

| Critério               | Pontos |
|------------------------|--------|
| Comprimento 16+        | +30    |
| Comprimento 12–15      | +20    |
| Comprimento 8–11       | +10    |
| Letras minúsculas      | +10    |
| Letras maiúsculas      | +20    |
| Números                | +20    |
| Símbolos especiais     | +20    |
| Entropia alta (60+ bits)| +10   |
| Caracteres repetidos   | -10    |
| Sequências previsíveis | -10    |

 Classificação

| Pontuação | Força         |
|-----------|---------------|
| 80–100    | 🟢 Forte      |
| 60–79     | 🟡 Média      |
| 40–59     | 🟠 Fraca      |
| 0–39      | 🔴 Muito Fraca|
| Lista vazada | ☠️ Péssima |

---

 Conceitos de segurança aplicados

- **Entropia**: Mede a imprevisibilidade da senha. Calculada com `len(senha) × log₂(charset)`. Senhas com 60+ bits são consideradas seguras.
- **Wordlist**: Verificação contra senhas mais comuns do mundo (baseada em listas de vazamentos reais como rockyou.txt).
- **`secrets` module**: Usado para gerar senhas com aleatoriedade criptograficamente segura, diferente do `random` padrão.
- **Análise de padrões**: Regex para detectar sequências de teclado e repetições que facilitam ataques de força bruta.

---

 Estrutura do projeto

```
password-analyzer/
├── analyzer.py       # Script principal
├── tests.py          # Testes unitários
├── requirements.txt  # Dependências
└── README.md         # Documentação
```

---

 Aviso ético

Esta ferramenta foi desenvolvida para fins educacionais e para ajudar usuários a criarem senhas mais seguras. Use apenas para analisar suas próprias senhas ou em ambientes autorizados.

---

 Licença

MIT License — fique à vontade para usar, modificar e distribuir.
