def get_crawler_template(page_title:str, link_list:list[str], goal_page_title:str):
    prompt = f"""<system> You are an AI language model tasked to beat the Wiki Game. 
    Your goal is, from a wikipedia page, to get the next link to click to go to the next page. </system>
    
    <instructions>
    The page you are sitting at is <page> {page_title} </page>
    
    Here is a list of the links available. 
    <link_list> {link_list} </link_list>
    
    The goal page is <goal_page> {goal_page_title} </goal_page>
    Select the link that is the most useful to get to the goal page. 
    </instructions>
    
    <output_rules>
    You must output two things:
    - Within <reasoning></reasoning> brackets, your reasoning about your link choice.
    - Within <output></output> brackets, your link choice.
    """
    return prompt