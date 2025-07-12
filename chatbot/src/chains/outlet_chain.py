import dotenv
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing_extensions import TypedDict
from langchain.chains import LLMChain

class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

dotenv.load_dotenv()

db = SQLDatabase.from_uri("sqlite:///zus_outlets.db")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

text2sql_template = """
Task:
Generate SQL queries based on the user's question.

Instructions:
Use only the provided database schema to generate the SQL query.
Do not include any additional text or explanations.

Schema:
{schema}

Note:
Do not include any explainations in your response.
Do not respond to any questions that are not related to the database schema.
Do not include any text other than the SQL query.
Do not run any SQL queries that would modify the database.
You are strictly only allowed to read from the database.

Examples:
# What is the address for the Ekocheras outlet?
SELECT location FROM outlets WHERE outlet = 'ekocheras mall';

# How many outlets are there in Kuala Lumpur?
SELECT COUNT(*) FROM outlets;

# Which outlets are located in Petaling Jaya?
SELECT outlet FROM outlets WHERE location LIKE '%Petaling Jaya%';

Question:
{question}
"""

text2sql_prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template=text2sql_template
)

qa_template = """
You are an assistant that takes the results of a SQL query and provides a human-readable response to the user's question.
The query result contains the answer of a SQL query that was generated based on the user's question.
The provided information is authoritative, so do not make up or correct any information that is not in the query result.
Make the answer sound like a response to the user's question.
The query results will be in lowercase, so make sure to format and capitalize the answer according to natural language conventions.

Query Result:
{context}

Question:
{question}

If the provided information is empty, say you don't know the answer.
Else, provide an answer based on the query result.

Answer:
"""

qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=qa_template
)

text2sql_chain = LLMChain(
    llm=llm,
    prompt=text2sql_prompt,
    output_key="query"
)

qa_chain = LLMChain(
    llm=llm,
    prompt=qa_prompt,
    output_key="answer"
)

def outlet_chain(question):
    schema = db.get_table_info()
    sql_query = text2sql_chain.invoke({"schema":schema, "question":question})["query"].strip()
    print("Query: " + sql_query)
    result = db.run(sql_query)
    answer = qa_chain.invoke({"context":result, "question":question})["answer"].strip()
    return answer




