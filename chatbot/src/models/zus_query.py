from pydantic import BaseModel

class ZusQueryInput(BaseModel):
    text: str

class ZusQueryOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: list[str]