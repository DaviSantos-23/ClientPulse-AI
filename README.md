# 🚀 ClientPulse-AI

Sistema inteligente de análise de feedbacks para consultorias utilizando IA Generativa, automação e dashboards em tempo real.

---

## 📌 Problema

Consultorias recebem dezenas de avaliações de clientes, mas normalmente a análise é manual, lenta e sujeita a erros.

O objetivo deste projeto é automatizar todo o processo de coleta, tratamento, análise e geração de insights.

---

## 🎯 Solução

O sistema:

- Coleta respostas de formulários automaticamente
- Atualiza planilhas em tempo real
- Limpa e trata os dados recebidos
- Calcula score de satisfação automaticamente
- Identifica riscos e oportunidades
- Gera feedbacks personalizados com IA
- Envia relatórios por e-mail
- Atualiza dashboards automaticamente

---

## 🏗 Arquitetura

Formulário
↓
Google Sheets
↓
n8n Workflow
↓
Tratamento de Dados
↓
IA Generativa
↓
Relatório Inteligente
↓
Dashboard Streamlit
↓
Email Automático

---

## Fluxograma

                 Google Forms
                       │
                       ▼
               Google Sheets
                       │
                       ▼
                n8n Workflow
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 Limpeza dos      Tratamento      Cálculo
    Dados          dos Dados      de Score
        │
        ▼
   IA Generativa
(Gemini/OpenAI)
        │
        ▼
 Feedback Inteligente
        │
        ▼
 Atualização da Planilha
        │
        ▼
 Dashboard em Tempo Real
 (Python + Streamlit)
        │
        ▼
 E-mail Automático

 ---
 
## 🛠 Tecnologias Utilizadas

- Python
- Streamlit
- n8n
- Google Sheets API
- Gemini
- OpenAI
- Pandas
- Gmail API

--- 

## 📊 Funcionalidades

### Dashboard Inteligente

- Ranking automático de consultores
- Média de satisfação
- Filtros por consultor
- Atualização automática
- Gráficos interativos

### IA Generativa

- Feedback personalizado
- Identificação de riscos
- Recomendações automáticas

### Automação

- Atualização da planilha
- Geração de relatórios
- Envio automático de e-mails

---

## 📸 Screenshots

### Dashboard

(Adicionar imagem aqui)

### Workflow n8n

(Adicionar imagem aqui)

---

## 📈 Resultados

- Redução do trabalho manual
- Análise automática de feedbacks
- Identificação rápida de problemas
- Melhor acompanhamento de consultores

---

## 🚀 Como Executar

```bash
git clone https://github.com/DaviSantos-23/ClientPulse-AI.git
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Executar:

```bash
streamlit run app.py
```

---

## 👨‍💻 Autor

Davi Santos

Ciência da Computação - UFS

Python | IA Generativa | Automação | Ciência de Dados
