from langchain.agents import create_agent

from config import llm
from tools import tools
from prompts import system_prompt


agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)