import streamlit as st
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph_backend_streaming import chatbot

# Page configuration
st.set_page_config(page_title="LangGraph Chatbot", layout="wide")
st.title("💬 LangGraph Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "1"

# Sidebar for thread management
with st.sidebar:
    st.header("⚙️ Settings")
    thread_id = st.text_input("Thread ID:", value=st.session_state.thread_id, key="thread_input")
    st.session_state.thread_id = thread_id
    
    if st.button("🔄 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.subheader("📋 Conversation History")
    if st.session_state.messages:
        st.write(f"Total messages: {len(st.session_state.messages)}")
    else:
        st.write("No messages yet")

# Display chat messages
container = st.container()
with container:
    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to history
    user_message = HumanMessage(content=user_input)
    st.session_state.messages.append(user_message)
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get AI response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Stream from chatbot
            for message_chunk, metadata in chatbot.stream(
                {"messages": st.session_state.messages},
                config={"configurable": {"thread_id": st.session_state.thread_id}},
                stream_mode="messages"
            ):
                if message_chunk.content:
                    full_response += message_chunk.content
                    message_placeholder.write(full_response)
            
            # Add AI response to history
            if full_response:
                ai_message = AIMessage(content=full_response)
                st.session_state.messages.append(ai_message)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
