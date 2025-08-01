import streamlit as st
from groq import Groq

# Configuration de la page
st.set_page_config(page_title="Chat avec Grok", layout="wide")
st.markdown(
    """
    <style>
    .stApp {background-color: #2E2E2E;}
    .header {background-color: #1C1C1C; color: #FFD700; padding: 10px; text-align: center;}
    .card {background-color: #3A3A3A; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.3); margin: 10px 0; color: #E0E0E0;}
    .footer {text-align: center; padding: 10px; background-color: #2E2E2E; color: #B0B0B0; font-size: 12px;}
    </style>
    """,
    unsafe_allow_html=True
)

# En-tête
st.markdown('<div class="header"><h2>Chat avec Grok</h2></div>', unsafe_allow_html=True)

# Initialisation du client Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Initialisation de l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Interface de chat
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Posez vos questions à Grok")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tapez votre message ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # Modèle rapide de Groq
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            temperature=0.7,
            max_tokens=500
        )
        reply = response.choices[0].message.content
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
st.markdown('</div>', unsafe_allow_html=True)

# Pied de page
st.markdown('<div class="footer">Développé par [Ton Nom] - Mise à jour: 01/08/2025</div>', unsafe_allow_html=True)