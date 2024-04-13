def get_crawler_template():
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
    - Within <output></output> brackets, your link choice. It should be like "<output>Output</output>".
    """
    return prompt

def get_summarize_template():
    prompt = """<instructions> The page content I want you to summarize is the following: 
    <page_content> 
    {page_content} 
    </page_content>
    </instructions>

    This summary should not be longer than 10 sentences. It should simply be enough to grasp an understanding of the Wikipedia page.
    From the page content above, return its summary and only the summary, within <summary> </summary> brackets."""
    return prompt