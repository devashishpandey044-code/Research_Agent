# test_agent_rag.py

from agent import agent

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is gradient descent?"
            }
        ]
    }
)

print(response["messages"][-1].content)