import re

def answer_summarize(summarize_chain, end_page:str) -> str:
    end_summary = summarize_chain.invoke(
        {
            "end_page": end_page
        }
    )
    model_output = end_summary.content
    pattern = r'<summary>(.*?)</summary>'
    matches = re.findall(pattern, model_output)
    end_page_content = matches[0]
    return end_page_content

def answer_broad_links(broad_links_chain, current_links:list[str], end_page:str, end_page_content:str) -> list[str]:
    broad_links = broad_links_chain.invoke({
        "current_links": current_links,
        "end_page": end_page,
        "end_page_content": end_page_content
    })
    model_output = broad_links.content
    pattern = r'<output>(.*?)</output>'
    matches = re.findall(pattern, model_output)
    broad_links = [link.strip() for link in matches[0].split(",")]
    return broad_links

def answer_explain_links(explain_links_chain, current_links:list[str], end_page:str, end_page_content:str) -> str:
    explain_links = explain_links_chain.invoke({
        "current_links": current_links,
        "end_page": end_page,
        "end_page_content": end_page_content
    })
    reasonings = explain_links.content
    return reasonings

def answer_crawler(crawler_chain, current_page:str, current_links:list[str], reasonings:str, end_page:str, end_page_content:str):
    crawler_text = crawler_chain.invoke(
        {
            "current_page": current_page,
            "current_links": current_links,
            "reasonings": reasonings,
            "end_page": end_page,
            "end_page_content": end_page_content
        }
    )
    model_output = crawler_text.content
    print(model_output)
    pattern = r'<output>(.*?)</output>'
    matches = re.findall(pattern, model_output)
    current_page = matches[0]
    return current_page