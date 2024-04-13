def get_crawler_template():
    system = (
    """You are an AI language model tasked to beat the Wiki Game. 
    Your goal is, from a wikipedia page, to get the next link to click to go to the next page."""
    )
    prompt = """ 
    <instructions>
    The page you are sitting at is <page> {current_page} </page>
    
    Here is a list of the links available. 
    <link_list> {current_links} </link_list>
    
    The goal page is <goal_page> {end_page} </goal_page>
    Here is its content <goal_page_content> {end_page_content} </goal_page_content>
    Select the link that is the most useful to get to the goal page. If you cannot find one that could be related from close to far, output "Random".
    </instructions>
    
    <output_rules>
    You must output two things:
    - Within <reasoning></reasoning> brackets, your reasoning about your link choice.
    - Within <output></output> brackets, your link choice. It should be like "<output>Output</output>". </output_rules>
    """
    return system, prompt

def get_reasoned_crawler_template():
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
    - Within <output></output> brackets, your link choice. It should be like "<output>Output</output>". </output_rules>
    """
    return system, prompt

def get_summarize_template():
    system = (
    """You are an AI language model tasked to summarize the Wikipedia content of the end page of a Wiki Race Game.
    Through this summary, you are supposed to help a crawler agent to get to the end page."""
    )
    prompt = """<instructions> The page content I want you to summarize is the following: 
    <page_content> 
    {page_content} 
    </page_content>
    </instructions>

    This summary should not be longer than 10 sentences. It should simply be enough to grasp an understanding of the Wikipedia page.
    From the page content above, return its summary and only the summary, within <summary> </summary> brackets."""
    return system, prompt

def get_broad_links_template():
    system = (
    """You are an AI language model part of a system tasked to beat the Wiki Game. 
    In order to beat the game, it can be helpful to get broad links that can give a lot of information to move from.
    Your goal is to select 3 links that you think have the highest amount of information in their wikipedia page."""
    )
    prompt = """The links you have to look for are the following: 
    <link_list> {link_list} </link_list>
    
    Select the 3 links that cover the most amount of subjects, and on which you expect to find the highest amount of links to follow through, regarding the objective of reaching the page
    <end_page> {end_page} </end_page>
    
    In order to help, here is a summary of the page's content <page_summary> {end_page_summary} </page_summary>
    
    Now, output the three links. Those three links should be output in the following format:
    <output> link_1, link_2, link_3 </output>. 
    Output them in this format and this format alone."""
    return system, prompt

def get_explain_links_template():
    system = (
    """You are an AI language model part of a system tasked to beat the Wiki Game. 
    In order to beat the game, it can be helpful to get explanations on the most relevant links chosen to beat the game.
    Here are the links you have to explain, that can be helpful to reach the end goal."""
    )
    prompt = """Here are the links that are to be explained, related to the end goal of reaching this page: <end_page> {end_page} </end_page> 
    <link_list> {link_list} </link_list>

    In order to help, here is a summary of the page's content <page_summary> {end_page_summary} </page_summary>
    
    Output an explanation for each of those links on why they could be helpful at winning the Wikipedia Race."""
    return system, prompt