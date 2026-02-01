import streamlit as st
import httpx
import asyncio

st.set_page_config(page_title="Docs Knowledge Agent", layout="centered")
st.title("Docs Knowledge Agent")

BACKEND_URL = "http://backend:8000/v1/chat"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



if prompt := st.chat_input("Zadaj pytanie dotyczące dokumentacji..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            try:
                payload = {
                    "message" : prompt,
                    "session_id": "streamlit-session-1"
                }
                response = httpx.post(BACKEND_URL, json=payload, timeout=30.0)

                if response.status_code == 200:
                    data = response.json()
                    ai_response = data["response"]
                    sources = data.get("sources", [])

                    st.markdown(ai_response)

                    if sources:
                        with st.expander("See sources"):
                            for s in sources:
                                st.write(f"- {s}")
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                else:
                    st.error(f"Backend error: {response.status_code}")
            except Exception as e:
                st.error(f"Failed to connect with API: {e}")