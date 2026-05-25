import streamlit as st
from utils.api import ask_question


def render_chat():
    st.subheader("💬 Chat with your documents")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # display old messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_input = st.chat_input("Type your question here...")

    if user_input:
        # show user message
        st.chat_message("user").markdown(user_input)

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # ask backend
        response = ask_question(user_input)

        # DEBUG
        print(response)

        # get answer safely
        if response.get("status") == "success":

            # backend returns result
            answer = response.get("result", "No answer returned")

            # if result is dict
            if isinstance(answer, dict):
                final_answer = answer.get("answer", str(answer))
                sources = answer.get("sources", [])
            else:
                final_answer = str(answer)
                sources = []

        else:
            final_answer = response.get("message", "Something went wrong")
            sources = []

        # show assistant message
        st.chat_message("assistant").markdown("### 🧠 Answer\n")

        # If answer contains bullet-style text → format it nicely
        if isinstance(final_answer, str):
            lines = final_answer.split("\n")

            formatted_answer = ""
            for line in lines:
                line = line.strip()

                if line.startswith("-") or line.startswith("•"):
                    formatted_answer += f"• {line.lstrip('-• ')}\n"
                elif line:
                    formatted_answer += f"👉 {line}\n"

            st.markdown(formatted_answer)
        else:
            st.markdown(final_answer)

        # show sources
        if sources:
            st.markdown("📄 **Sources:**")

            with st.expander("📄 View Sources"):
                for src in sources:
                    st.markdown(f"📘 {src}")

        # save assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": final_answer
        })