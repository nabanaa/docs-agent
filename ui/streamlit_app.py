import streamlit as st
import httpx
import os

st.set_page_config(page_title="Docs Knowledge Agent", layout="centered")
st.title("Docs Knowledge Agent")

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

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
                response = httpx.post(f"{BASE_URL}/v1/chat", json=payload, timeout=30.0)

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

with st.sidebar:
    st.header("Documents")
    uploaded_file = st.file_uploader("Upload a PDF for RAG", type = "pdf")

    if uploaded_file and st.button("Process Document"):
        with st.spinner("Processing"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            res = httpx.post(f"{BASE_URL}/v1/upload", files=files)
            if res.status_code == 200:
                st.success("Document indexed!")
            else:
                st.error("Upload failed.")
                