from fastapi import FastAPI
from agents.zus_agent import executor
from models.zus_query import ZusQueryInput, ZusQueryOutput
from utils.async_utils import async_retry

app = FastAPI(
    title="Zus Coffee Chatbot",
    description="A chatbot for Zus Coffee that answers questions about outlets and products.",
    version="1.0.0"
)

@async_retry(max_retries=10, delay=1)
async def invoke_agent(query: str):
    """
    Invoke the agent with the provided query and return the response.
    """
    return await executor.ainvoke({"input": query})

@app.get("/")
async def get_status():
    """
    Check the status of the chatbot service.
    """
    return {"status": "running"}

@app.post("/query")
async def query_agent(query: ZusQueryInput) -> ZusQueryOutput:
    """
    Handle a query to the chatbot and return the response.
    """
    res = await invoke_agent(query.text)
    res["intermediate_steps"] = [
        str(s) for s in res["intermediate_steps"]
    ]
    return res