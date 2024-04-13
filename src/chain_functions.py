from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from prompt_functions import get_crawler_template, get_summarize_template, get_broad_links_template, get_explain_links_template

def get_crawler_chain(chat:ChatAnthropic):
    crawler_system, crawler_template = get_crawler_template()
    crawler_prompt = ChatPromptTemplate.from_messages([("system", crawler_system), ("human", crawler_template)])
    crawler_chain = crawler_prompt | chat
    return crawler_chain

def get_summarize_chain(chat:ChatAnthropic):
    summarize_system, summarize_template = get_summarize_template() 
    prompt = ChatPromptTemplate.from_messages([("system", summarize_system), ("human", summarize_template)])
    summarize_chain = prompt | chat
    return summarize_chain

def get_broad_links_chain(chat:ChatAnthropic):
    broad_links_system, broad_links_template = get_broad_links_template()
    broad_links_prompt = ChatPromptTemplate.from_messages([("system", broad_links_system), ("human", broad_links_template)])
    broad_links_chain = broad_links_prompt | chat
    return broad_links_chain

def get_explain_links_chain(chat:ChatAnthropic):
    explain_links_system, explain_links_template = get_explain_links_template()
    explain_links_prompt = ChatPromptTemplate.from_messages([("system", explain_links_system), ("human", explain_links_template)])
    explain_links_chain = explain_links_prompt | chat
    return explain_links_chain