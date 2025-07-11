import dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)

dotenv.load_dotenv()

chatbot = ChatOpenAI(model="gpt-4o-mini", temperature=0)