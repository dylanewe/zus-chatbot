import dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import (
    create_openai_functions_agent,
    Tool,
    AgentExecutor
)
from langchain import hub
from chains.outlet_chain import outlet_chain
from chains.product_chain import product_chain
from tools.calculator import Calculator

dotenv.load_dotenv()

agent_prompt = hub.pull("hwchase17/openai-functions-agent")

tools = [
    # Tool(
    #     name="Calculator",
    #     func=Calculator(),
    #     description="A simple calculator that can add and multiply numbers."
    # ),
    Tool(
        name="Outlets",
        func=outlet_chain,
        description="Answer questions about Zus Coffee outlets."
    ),
    Tool(
        name="Products",
        func=product_chain,
        description="Answer questions about Zus Coffee products."
    )
]

chatbot = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_openai_functions_agent(
    llm=chatbot,
    prompt=agent_prompt,
    tools=tools,
)

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True
)