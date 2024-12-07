import streamlit as st
import requests

# No problem this being public.
QUEPASA_TOKEN = "saas_alpaca_2:gmlqz7WiB4fDIwqt5MQ7PyD7gp4MEabcMcpMhBsPH9GGDtui7Wj4hshm54EDIqv4"

st.title("Alpaca Network AI Agent Search Bot")

intro_msg = 'Hi! I am an Alpaca Netowork assistant that finds you an AI agent to perform a task you want. Please describe what you want to do.'

quepasa_prompt = '''You are a search bot created by Alpaca Network.
You will be asked to either complete a task, or to find a proper AI agent to complete the task.
But don't worry — I already know what AI agents are best fit for the task provided.
Use ONLY the information from the sources below!

When answering the question, use the following rules:
- always answer in {{LANGUAGE}} language;
- output ONLY the list of agents with their brief description in a numbered list. Do not add anything except the list of agents, therefore your output MUST begin with '1.'
- if there is no information on the question in the sources: say that you can't find a matching AI assistant, and say that you hope a one appears in the future!

Here's the ranked list of agents or tools that fit the job:

{{SOURCES}}'''

def get_quepasa_response(q):
    payload = {
        "question": q,
        "domain": "default",
        "llm": "anthropic:claude-3-5-sonnet-20240620",
        "prompt": quepasa_prompt,
        # "answer_prompt_size": 900,
        # "prompt_total_size": 8110,
        "document_relevance_weights": {
            "text": 0.2,
            "semantic": 0.8
        },
        "chunk_relevance_weights": {
            "text": 0.2,
            "semantic": 0.8
        },
    }

    req_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {QUEPASA_TOKEN}"
    }

    response = requests.post("https://api.quepasa.ai/api/v1/retrieve/answer", json=payload, headers=req_headers)
    return response.json()['data']['answer']


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": intro_msg}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display assistant response in chat message container
    thinking_msg = "Thinking..."
    with st.chat_message("assistant"):
        st.markdown(thinking_msg)
    st.session_state.messages.append({"role": "assistant", "content": thinking_msg})
    
    answer = get_quepasa_response(prompt)
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
