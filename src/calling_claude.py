import yaml
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)
openai_key = config["openai_key"]
anthropic_key = config["anthropic_key"]

os.environ["ANTHROPIC_API_KEY"] = anthropic_key