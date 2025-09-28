# Projeto BotCity – Automação de Alteração de SLA no SeSuite

## 1. Descrição do Projeto
Este projeto tem como objetivo automatizar o processo de **alteração de SLA em chamados** no sistema SeSuite. O robô faz login, pesquisa os chamados indicados, altera a data do SLA e registra a execução no Orquestrador Maestro.

O fluxo simula um **cenário corporativo real**, onde mudanças repetitivas e críticas em sistemas internos podem ser automatizadas, aumentando a produtividade e reduzindo erros manuais.

---

## 2. Funcionalidades
- Login automático no SeSuite usando credenciais seguras.
- Navegação e pesquisa de chamados via ID.
- Alteração da data do SLA e preenchimento de justificativa.
- Geração de log em Excel (`resultado_execucao.xlsx`) com status de cada chamado.
- Integração completa com **BotCity Maestro** para reportar execução e upload do artefato.

---

## 3. Tecnologias Utilizadas
- Python 3.10+
- [BotCity WebBot](https://botcity.dev/)
- Selenium (via BotCity)
- pandas (manipulação de planilhas Excel)
- python-dotenv (armazenamento seguro de credenciais)
- BotCity Maestro SDK (integração com Orquestrador)

---

## 4. Estrutura do Projeto
botcity-alterar-sla/
├─ robot.py # Script principal do WebBot
├─ chamados.xlsx # Planilha de entrada com IDs, datas e justificativas
├─ requirements.txt # Dependências Python
├─ .env.example # Exemplo de variáveis de ambiente (usuário, senha, URL)
├─ outputs/ # Pasta para logs e relatórios gerados
└─ README.md # Este arquivo

---

## 5. Pré-requisitos
1. Python 3.10 ou superior.
2. Edge WebDriver instalado e compatível com sua versão do Edge.
3. Credenciais de acesso ao SeSuite.
4. Conta no BotCity Maestro com permissões para reportar execução e enviar artefatos.
5. Bibliotecas Python listadas em `requirements.txt`.

---

## 6. Configuração do Ambiente
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/botcity-alterar-sla.git
cd botcity-alterar-sla
