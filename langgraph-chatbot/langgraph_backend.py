from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatopenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_message

from dotenv import load_dotenv
load_dotenv()
llm = ChatopenAI()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_message]

def chat_node(state: ChatState):
    response = llm.invoke(state['messages'])
    return {'messages': [response]}

#checkpointer
checkpointer = InMemorySaver()

#graph
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)