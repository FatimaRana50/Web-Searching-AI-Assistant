import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool
from firecrawl import FirecrawlApp   

# Loading API keys
load_dotenv()

# ---- Web Searching Tool ----
def firecrawl_search(query: str) -> str:
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
    results = app.search(query)

    simplified = []
    if results.web:  
        for r in results.web:
            title = getattr(r, "title", "No title")
            url = getattr(r, "url", "")
            desc = getattr(r, "description", "")
            simplified.append(f"- {title}: {url}\n  {desc}")

    if not simplified:
        return "No search results found."
    return "\n".join(simplified)




# Register tool
tools = [
    Tool(
        name="Web Search",
        func=firecrawl_search,
        description="Use this to look up real-time or current information on the internet."
    )
]

# ---- LLM ----
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",   
    temperature=0
)

# ---- Agent ----
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# ---- Run ----
if __name__ == "__main__":
    q1 = "Who won the  T-20 World Cup in 2022?"
    q2 = "What is the Pythagorean theorem?"
    q3 = "What is the capital of Norway, and what are the headlines there today?"

    #print("\n--- Q1 ---")
    #print(agent.run(q1))

    #print("\n--- Q2 ---")
    #print(agent.run(q2))

    print("\n--- Q3 ---")
    print(agent.run(q3))
