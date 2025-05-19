import streamlit as st
from src.agent import ReActAgent

st.title("Deep Origin")
st.header("ReAct Agent with Gemini")
st.subheader("Ask a question and watch the agent think step by step.", divider=True)

if st.button("Reset App (Clear Chat and Memory)"):
    st.cache_resource.clear()
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

if "history" not in st.session_state:
    st.session_state.history = []

if "agent" not in st.session_state:
    st.session_state.agent = ReActAgent()

with st.form(key="qa_form", clear_on_submit=True):
    user_input = st.text_input("Your question:")
    submit = st.form_submit_button("Submit")

if submit and user_input:
    with st.spinner("Thinking..."):
        answer, updated_history, thinking = st.session_state.agent.run(
            question=user_input,
            history=st.session_state.history
        )
        st.session_state.history = updated_history

    st.success(f"**Answer:** {answer}")
    with st.expander("Agent Thinking - Steps and Tool Use", expanded=True):
        st.code(thinking, language="markdown")

if st.session_state.history:
    st.markdown("### Conversation History")
    for qa in reversed(st.session_state.history):
        st.markdown(f"**You:** {qa['question']}")
        st.markdown(f"**Agent:** {qa['answer']}")
        st.markdown("---")
