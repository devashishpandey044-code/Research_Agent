from config import llm

response = llm.invoke("Tell me one interesting fact about AI.")

print(response.content)