import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(page_title="Bac Bo Inteligente", layout="centered")
st.title("🤖 Bot Inteligente para Bac Bo")

st.markdown("Adicione os valores dos dados e o bot irá prever o próximo resultado com base lógica avançada.")

# Inicializa o histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Entradas de dados
col1, col2 = st.columns(2)
with col1:
    banker = st.number_input("🎲 Valor dos dados do Banker", min_value=2, max_value=12, step=1)
with col2:
    player = st.number_input("🎲 Valor dos dados do Player", min_value=2, max_value=12, step=1)

if st.button("Adicionar Resultado"):
    if banker > player:
        resultado = "Banker"
    elif player > banker:
        resultado = "Player"
    else:
        resultado = "Empate"
    st.session_state.historico.append(resultado)
    st.success(f"Resultado adicionado: {resultado}")

# Exibe histórico
if st.session_state.historico:
    st.subheader("📜 Histórico de Resultados")
    st.write(st.session_state.historico[::-1])

    # Filtros avançados
    st.subheader("⚙️ Filtros Avançados")
    num_rodadas = st.slider("Quantas rodadas recentes considerar?", min_value=5, max_value=100, value=10)
    considerar_empates = st.checkbox("Incluir empates na análise", value=True)

    # Processamento dos dados
    ultimos = st.session_state.historico[-num_rodadas:]
    if not considerar_empates:
        ultimos = [r for r in ultimos if r != "Empate"]

    contagem = Counter(ultimos)
    total = sum(contagem.values())

    # Probabilidades
    prob_banker = contagem.get("Banker", 0) / total if total else 0
    prob_player = contagem.get("Player", 0) / total if total else 0
    prob_empate = contagem.get("Empate", 0) / total if total else 0

    st.subheader("📊 Probabilidades Detectadas")
    st.markdown(f"**Banker:** {prob_banker:.0%} | **Player:** {prob_player:.0%} | **Empate:** {prob_empate:.0%}")

    # Inteligência lógica
    sugestao = ""
    if len(ultimos) >= 4:
        padrao = ultimos[-4:]
        if padrao.count("Banker") >= 3:
            sugestao = "Tendência forte de Banker, possível virada para Player."
            recomendacao = "Player"
        elif padrao.count("Player") >= 3:
            sugestao = "Tendência forte de Player, possível virada para Banker."
            recomendacao = "Banker"
        elif ultimos[-1] == "Banker" and ultimos[-2] == "Player" and ultimos[-3] == "Banker":
            sugestao = "Padrão alternado detectado."
            recomendacao = "Player"
        elif contagem.get("Empate", 0) < max(1, total // 12):
            sugestao = "Empate raro detectado. Pode estar próximo."
            recomendacao = "Empate"
        else:
            recomendacao = max(contagem, key=contagem.get)
            sugestao = "Recomendação baseada na frequência dominante."
    else:
        recomendacao = max(contagem, key=contagem.get)
        sugestao = "Análise baseada na frequência dos últimos resultados."

    st.subheader("🧠 Sugestão Inteligente")
    st.markdown(f"**{sugestao}**")
    st.markdown(f"🎯 **Recomenda apostar em:** `{recomendacao}`")

else:
    st.info("Adicione pelo menos um resultado para iniciar a análise.")
