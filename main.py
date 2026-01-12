import streamlit as st

# ЧАТ-БОТ

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
)

# заголовок
st.title("ITStep chat bot")

# завантаження апі ключа за допомогою streamlit
api_key = st.secrets.get("GEMINI_API_KEY")

# Якщо API ключ не налаштований, показати повідомлення і зупинити виконання
if not api_key:
    st.error(
        "API ключ GEMINI_API_KEY не знайдено в st.secrets.\n"
        "Додайте його у файл .streamlit/secrets.toml перед запуском застосунку."
    )
    st.stop()

# створити llm
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    api_key=api_key,
)

# Ініціалізація історії повідомлень один раз на сесію
if "history" not in st.session_state:
    # перше повідомлення з основними інструкціями (системний промпт)
    st.session_state["history"] = [
        SystemMessage(
            """
            Ти — ввічливий чат-бот. Твоя задача — давати короткі та
            чіткі відповіді на питання.
            """
        )
    ]

# поле для введення повідомлення користувача
user_query = st.chat_input("Ваше повідомлення")

# якщо повідомлення введено, то дати відповідь від моделі
if user_query:
    # перетворюємо повідомлення в HumanMessage
    human_message = HumanMessage(user_query)

    # додаємо до історії повідомлень
    st.session_state["history"].append(human_message)

    # запускаємо модель з усією історією
    response = llm.invoke(st.session_state["history"])

    # response — AIMessage; додаємо до історії повідомлень
    st.session_state["history"].append(response)

    # вивести відповідь
    st.markdown(f"**AI:** {response.content}")
