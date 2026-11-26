import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")
st.set_page_config(page_title="Citizen AI Assistant", page_icon="🇮🇳", layout="wide")

st.title("🇮🇳 Multilingual Government Citizen Assistant")
st.caption("Ask public-service questions in English, తెలుగు, हिन्दी, தமிழ் or ಕನ್ನಡ.")

with st.sidebar:
    st.header("Language")
    language = st.selectbox("Response language", [
        ("Automatic detection", "auto"), ("English", "en"), ("తెలుగు", "te"),
        ("हिन्दी", "hi"), ("தமிழ்", "ta"), ("ಕನ್ನಡ", "kn")
    ], format_func=lambda x: x[0])[1]
    st.divider()
    st.subheader("Upload government PDF")
    uploaded = st.file_uploader("Choose a searchable PDF", type=["pdf"])
    if st.button("Upload and index", disabled=uploaded is None):
        try:
            response = requests.post(
                f"{API_URL}/documents/upload",
                files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")},
                timeout=90
            )
            response.raise_for_status()
            st.success(response.json()["message"])
        except requests.RequestException as exc:
            st.error(f"Upload failed: {exc}")
    st.divider()
    st.caption("Never enter Aadhaar numbers, OTPs, passwords, bank PINs or other sensitive details.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask about a government service or scheme...")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Understanding your question..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"message": question, "language": language},
                    timeout=90
                )
                response.raise_for_status()
                result = response.json()
                answer = result["answer"]
                st.markdown(answer)
                st.caption(f"Detected language: {result['detected_language']} · Provider: {result['provider']}")
                if result.get("sources"):
                    with st.expander("Retrieved document references"):
                        for source in result["sources"]:
                            st.markdown(f"**{source['title']}**")
                            st.write(source["content"][:700])
                st.session_state.last_question = question
            except requests.RequestException as exc:
                answer = f"Could not connect to the backend. Start FastAPI first. Details: {exc}"
                st.error(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

if st.session_state.get("last_question"):
    st.divider()
    st.subheader("Was this answer helpful?")
    col1, col2 = st.columns([1, 3])
    with col1:
        rating = st.selectbox("Rating", [5, 4, 3, 2, 1], label_visibility="collapsed")
    with col2:
        comment = st.text_input("Optional feedback", label_visibility="collapsed",
                                placeholder="Tell us how to improve")
    if st.button("Submit feedback"):
        try:
            requests.post(f"{API_URL}/feedback", json={
                "question": st.session_state.last_question,
                "rating": rating, "comment": comment
            }, timeout=10).raise_for_status()
            st.success("Thank you for your feedback.")
        except requests.RequestException as exc:
            st.error(f"Feedback could not be saved: {exc}")

st.divider()
st.caption("This is an educational prototype, not an official government service. Always verify scheme details on official portals.")
