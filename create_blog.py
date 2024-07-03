#warning control
import warnings
warnings.filterwarnings("ignore")
from pymongo import MongoClient
from bson.objectid import ObjectId
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
from tools import pexels_image_search
from crewai_tools import tool
from dotenv import load_dotenv
load_dotenv()


import os
from langchain_community.llms import Ollama

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

#create a connection to the mongodb
client = MongoClient(os.environ["MONGO_DB_URI"])
db = client["articles"]
collection = db["tasks"]

llm = Ollama(
    model = "llama3",
    base_url = "http://localhost:11434")



#   Initialize the tools for internet searching capabilities
@tool('search_tool')
def search(search_query: str):
    """Search the web for information on a given topic"""
    response = SerperDevTool().run(search_query)
    return response

serper_search = search

# Planning Agent
planner = Agent(
    role="Content Strategist and Researcher",
    goal="Research and develop a comprehensive, SEO-optimized content plan for a blog article on {topic}",
    backstory="You are an experienced content strategist and researcher with a keen understanding of SEO and audience engagement. Your expertise lies in conducting thorough research and crafting content plans that not only inform but also captivate readers, ensuring high engagement and search engine visibility.",
    tools=[serper_search],
    allow_delegation=False,
    verbose=False,
    llm=llm
)

# Writing Agent
writer = Agent(
    role="Expert Content Creator",
    goal="Craft an insightful, engaging, and SEO-friendly {content_type} on {topic}, based on the provided content plan and user-specified parameters",
    backstory="As a skilled content creator, you excel at transforming outlines into compelling narratives. Your writing is known for its clarity, engagement, and ability to balance factual information with thoughtful insights. You have a talent for seamlessly incorporating SEO elements without compromising readability.",
    tools=[],
    allow_delegation=False,
    verbose=False,
    llm=llm
)
# Editing Agent
editor = Agent(
    role="Senior Content Editor",
    goal="Refine and polish the blog post to ensure it meets the highest standards of quality, accuracy, and brand alignment",
    backstory="With years of experience in digital publishing, you have a sharp eye for detail and a deep understanding of content best practices. Your expertise ensures that every piece of content not only resonates with the target audience but also adheres to the brand's voice and editorial guidelines.",
    tools=[],
    allow_delegation=False,
    verbose=False,
    llm=llm
)

# Define the tasks for the crew agents
plan = Task(
    description="""
    1. Use the SerperDevTool to conduct thorough research on {topic}.Strictly use the top 5 search results only and Focus on:
       a. Latest news and developments
       b. Statistical data and expert opinions
    2. Analyze the search results and identify the most relevant and credible information.
    3. Based on your research, identify the primary target audience, including their demographics, interests, pain points, and information needs.
    4. Develop a detailed content outline with the following components:
       a. An attention-grabbing introduction
       b. 3-5 main sections, each addressing a key aspect of {topic}, supported by your research findings
       c. A compelling conclusion with a clear call-to-action
    5. Incorporate the following elements into your plan:
       a. A list of 5-7 relevant SEO keywords or phrases identified from your research
       b. Specific data points, statistics, or expert quotes from your research to enhance credibility
       c. Ideas for visual elements (e.g., infographics, charts) based on the data you've found
    6. Provide guidance on the overall tone and style that would best resonate with the target audience, considering the nature of the topic and your research findings.

    Your output should be a structured content plan document that serves as a comprehensive roadmap for the content creator, heavily informed by your research.
    """,
    expected_output="A detailed content strategy document including research findings, audience analysis, SEO keywords, content structure, and specific resource suggestions based on the conducted research.",
    agent=planner
)

write = Task(
    description="""
    Using the provided content plan, craft a compelling and informative {content_type} on {topic}. Your task includes:

    1. Writing an engaging introduction that hooks the reader and clearly states the {content_type}'s purpose.
    2. Developing each main section with depth and insight, ensuring a logical flow of ideas.
    3. Naturally incorporating the provided SEO keywords throughout the content.
    4. Using transitions to maintain coherence between sections.
    5. Crafting a conclusion that summarizes key points and includes a clear call-to-action.
    6. Incorporating relevant data, statistics, or expert quotes as suggested in the content plan.
    7. Suggesting placements for visual elements to enhance the content's impact.
    8. Ensuring the {content_type} aligns with the specified tone and style guidelines.

    Additional parameters to consider:
    - Tonality: {tonality}
    - Content Goal: {content_goal}

    Adjust your writing style and approach based on these parameters:
    - For tonality, ensure that the overall voice and language used in the {content_type} matches the specified {tonality} tone.
    - For the content goal of {content_goal}, structure your content to primarily achieve this objective while still providing value to the reader.

    Format your {content_type} in markdown, with proper headings, subheadings, and paragraph breaks. Adjust the length based on the specific content type, but aim for a comprehensive piece that thoroughly covers the topic.

    Remember to tailor your approach based on the specific content type:
    - For a how-to guide, focus on clear, step-by-step instructions.
    - For a listicle, use numbered or bulleted lists to organize information.
    - For a news article, prioritize the most important information first and maintain an objective tone.
    - For an opinion piece, clearly state your position and support it with strong arguments and evidence.
    - For a product review, provide a balanced assessment of pros and cons, and include specific details about the product.

    Throughout the writing process, keep the {tonality} tone and the goal to {content_goal} at the forefront of your mind, ensuring that every section contributes to these objectives.
    """,
    expected_output="A well-structured, SEO-optimized {content_type} in markdown format, tailored to the specified tonality and content goal, ready for editorial review.",
    agent=writer
)

edit = Task(
    description="""
    Thoroughly review and refine the provided blog post to ensure it meets the highest standards of quality and aligns with the brand's guidelines. Your editing process should include:

    1. Checking for grammatical errors, typos, and punctuation issues.
    2. Ensuring consistent tone and style throughout the piece, aligned with the brand voice.
    3. Verifying the logical flow and coherence of ideas across sections.
    4. Confirming that SEO keywords are naturally integrated and not overused.
    5. Evaluating the effectiveness of the introduction and conclusion.
    6. Assessing the appropriateness and impact of any data, statistics, or quotes used.
    7. Suggesting improvements for clarity, conciseness, and engagement where necessary.
    8. Verifying that the content provides balanced viewpoints and avoids unsubstantiated claims.
    9. Ensuring compliance with ethical guidelines and avoiding controversial statements.
    10. Optimizing headings and subheadings for both SEO and readability.
    11. Strictly provide blog article of 1000-1500 words, with each main section containing 2-3 well-developed paragraphs.

    Provide your edits and suggestions directly in the document, using track changes or comments where appropriate. If major revisions are needed, clearly explain your reasoning and provide guidance for improvements.
    """,
    expected_output="A polished, publication-ready blog post with tracked changes and editorial comments where necessary.",
    agent=editor
)

# Create the Crew with the defined agents and tasks
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)
# function to create a blog article and update the database 
def create_blog(id, topic,content_type, tonality, content_goal):
   
    result = crew.kickoff(inputs={"topic": topic,"content_type":content_type,"tonality":tonality,"content_goal":content_goal })
    data = {
        "_id": id,
        "status": "completed",
        "article": result,
        "updated_at": str(ObjectId.generation_time)
    }
    collection.update_one(
        {
            "_id": id
        },
        {
            "$set": data
        }
    )
    pass 

