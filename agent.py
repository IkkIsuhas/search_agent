from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_classic.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from datetime import datetime
import requests

import os
from dotenv import load_dotenv
load_dotenv()

api = os.getenv("OPENROUTER_API_KEY")
search_tool = TavilySearchResults(
          api_key = os.getenv("TAVILY_API_KEY")
     )

@tool
def get_current_date(query : str) -> str:
     """get current time"""
     return datetime.now().strftime("%d-%m-%y, %H:%M:%S" )

@tool
def get_calculator(expression: str) -> str:
     """safely eveluate mathmatical expression"""
     try:
          result = eval(expression)
          return result
     except Exception as e:
          return f"Error calculating: {e}"

@tool
def web_search(question: str) -> str:
     """Search the web for current information."""
     result = search_tool.invoke(question)
     return result

@tool
def text_parser(text:str)->str:
    """count character and words in the text"""
    char_count = len(text)
    word_count = len(text.split())

    return f"Characturs: {char_count} Words: {word_count}"

llm = ChatOpenAI(
     api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-oss-120b:free"
)

agent = create_agent(
     model=llm,
     tools=[get_current_date,get_calculator,web_search,text_parser]
     )

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_classic.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from datetime import datetime
import requests

import os
from dotenv import load_dotenv
load_dotenv()

api = os.getenv("OPENROUTER_API_KEY")
search_tool = TavilySearchResults(
          api_key = "TAVILY_API_KEY"
     )

@tool
def get_current_date(query : str) -> str:
     """get current time"""
     return datetime.now().strftime("%d-%m-%y, %H:%M:%S" )

@tool
def get_calculator(expression: str) -> str:
     """safely eveluate mathmatical expression"""
     try:
          result = eval(expression)
          return str(result)
     except Exception as e:
          return f"Error calculating: {e}"

@tool
def web_search(question: str) -> str:
     """Search the web for current information."""
     result = search_tool.invoke(question)
     return result

@tool
def text_parser(text:str)->str:
    """count character and words in the text"""
    char_count = len(text)
    word_count = len(text.split())

    return f"Characturs: {char_count} Words: {word_count}"

prompt_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""

prompt = PromptTemplate(
     template=prompt_template,
     input_variables=["input", "agent_scratchpad"] 
)

llm = ChatOpenAI(
     api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-oss-120b:free"
)

agent = create_agent(
     model=llm,
     tools=[get_current_date,get_calculator,web_search,text_parser]
     )

user_input = input("Enter your query: ")
response = agent.invoke({
    "messages": [
        {"role": "user", "content": user_input}
    ]
})

final_answer = response['messages'][-1].content
print(final_answer)