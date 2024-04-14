"""Functions related to getting both system and human prompts"""

def get_crawler_template() -> tuple[str]:
    """
    Gets system and human prompts for the crawling agent.
    
    Args: None
    
    Returns:
        system (str): system prompt for the crawling agent.
        prompt (str): human prompt for the crawling agent.
    """
    system = (
    """You are an AI language model tasked to beat the Wiki Game. 
    Your goal is, from a wikipedia page, to get the next link to click to go to the next page.
    You will be given reasoning for each link to click on, and select your link accordingly."""
    )
    prompt = """ 
    <instructions>
    The page you are sitting at is <page> {current_page} </page>
    
    Here is a list of the links available, with associated reasonings of why they would be good to pick. 
    <link_list> {current_links} </link_list>
    <reasonings> {reasonings} </reasonings>
    
    The goal page is <goal_page> {end_page} </goal_page>
    Here is its content <goal_page_content> {end_page_content} </goal_page_content>
    Select the link that is the most useful to get to the goal page. You MUST output a link, even if you are uncertain any link is helpful.
    </instructions>
    
    <output_rules>
    You must output two things:
    - Within <reasoning></reasoning> brackets, your reasoning about your link choice.
    - Within <output></output> brackets, your link choice. It should be like "<output>Output</output>".
    You MUST answer a link from the link list. Any other link is unreceivable. </output_rules>
    """
    return system, prompt

def get_summarize_template():
    """
    Gets system and human prompts for the summarizing agent.
    
    Args: None
    
    Returns:
        system (str): system prompt for the summarizing agent.
        prompt (str): human prompt for the summarizing agent.
    """
    system = (
    """You are an AI language model tasked to summarize the Wikipedia content of the end page of a Wiki Race Game.
    Through this summary, you are supposed to help a crawler agent to get to the end page."""
    )
    prompt = """<instructions> The end page's content that I want you to summarize is the following: 
    <end_page_full_content> 
    {end_page_full_content} 
    </end_page_full_content>
    </instructions>

    This summary should not be longer than 10 sentences. It should simply be enough to grasp an understanding of the Wikipedia page.
    From the page content above, return its summary and only the summary. Your summary MUST be formatted like this:
    <summary>summary</summary>"""
    return system, prompt

def get_broad_links_template():
    """
    Gets system and human prompts for the agent tasked to get broad links from the links available.
    
    Args: None
    
    Returns:
        system (str): system prompt for the agent tasked to get broad links from the links available.
        prompt (str): human prompt for the agent tasked to get broad links from the links available.
    """
    system = (
    """You are an AI language model part of a system tasked to beat the Wiki Game. 
    In order to beat the game, it can be helpful to get broad links that can give a lot of information to move from.
    Your goal is to select 3 links that you think have the highest amount of information in their wikipedia page."""
    )
    prompt = """The links you have to look for are the following: 
    <link_list> {current_links} </link_list>
    
    Select the 3 links that cover the most amount of subjects, and on which you expect to find the highest amount of links to follow through, regarding the objective of reaching the page
    <end_page> {end_page} </end_page>
    
    In order to help, here is a summary of the page's content <page_summary> {end_page_content} </page_summary>
    
    <output_rules> Now, output the three links. Those three links should be output in the following format:
    <output> link_1, link_2, link_3 </output>. 
    Output them in this format and this format alone. You MUST answer links from the link_list. Any other link is unreceivable. </output_rules>"""
    return system, prompt

def get_explain_links_template():
    """
    Gets system and human prompts for the agent tasked tasked to explain the links' usefulness related to the objective.
    
    Args: None
    
    Returns:
        system (str): system prompt for the agent tasked tasked to explain the links' usefulness related to the objective.
        prompt (str): human prompt for the agent tasked tasked to explain the links' usefulness related to the objective.
    """
    system = (
    """You are an AI language model part of a system tasked to beat the Wiki Game. 
    In order to beat the game, it can be helpful to get explanations on the most relevant links chosen to beat the game.
    Here are the links you have to explain, that can be helpful to reach the end goal."""
    )
    prompt = """Here are the links that are to be explained, related to the end goal of reaching this page: <end_page> {end_page} </end_page> 
    <link_list> {current_links} </link_list>

    In order to help, here is a summary of the page's content <page_summary> {end_page_content} </page_summary>
    
    <output_rules> Output an explanation for each of those links on why they could be helpful at winning the Wikipedia Race.
    Output AT MOST 3 sentences per link. Do not output anything else but the explanations. </output_rules>"""
    return system, prompt