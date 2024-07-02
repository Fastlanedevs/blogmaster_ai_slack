#warning control
import warnings
warnings.filterwarnings("ignore")
from pymongo import MongoClient
from bson.objectid import ObjectId
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

import os
from langchain_community.llms import Ollama
os.environ["OPENAI_API_KEY"] = "NA"
#create a connection to the mongodb
client = MongoClient(os.environ["MONGO_DB_URI"])
db = client["articles"]
collection = db["tasks"]

llm = Ollama(
    model = "gemma2",
    base_url = "http://localhost:11434")

planner = Agent(
    role="Content Strategist",
    goal="Develop a comprehensive, SEO-optimized content plan for a blog article on {topic}",
    backstory="You are an experienced content strategist and copywriter with a keen understanding of SEO and audience engagement. Your expertise lies in crafting content plans that not only inform but also captivate readers, ensuring high engagement and search engine visibility.",
    tools=[],
    allow_delegation=False,
    verbose=False,
    llm=llm
)

writer = Agent(
    role="Expert Content Creator",
    goal="Craft an insightful, engaging, and SEO-friendly blog post on {topic}, based on the provided content plan",
    backstory="As a skilled content creator, you excel at transforming outlines into compelling narratives. Your writing is known for its clarity, engagement, and ability to balance factual information with thoughtful insights. You have a talent for seamlessly incorporating SEO elements without compromising readability.",
    tools=[],
    allow_delegation=False,
    verbose=False,
    llm=llm
)

editor = Agent(
    role="Senior Content Editor",
    goal="Refine and polish the blog post to ensure it meets the highest standards of quality, accuracy, and brand alignment",
    backstory="With years of experience in digital publishing, you have a sharp eye for detail and a deep understanding of content best practices. Your expertise ensures that every piece of content not only resonates with the target audience but also adheres to the brand's voice and editorial guidelines.",
    tools=[],
    allow_delegation=False,
    verbose=False,
    llm=llm
)

plan = Task(
    description="""
    1. Conduct a thorough analysis of the latest trends, key players, and noteworthy developments related to {topic}.
    2. Identify the primary target audience, including their demographics, interests, pain points, and information needs.
    3. Develop a detailed content outline with the following components:
       a. An attention-grabbing introduction
       b. 3-5 main sections, each addressing a key aspect of {topic}
       c. A compelling conclusion with a clear call-to-action
    4. Incorporate the following elements into your plan:
       a. A list of 5-7 relevant SEO keywords or phrases to be naturally integrated
       b. Suggestions for data points, statistics, or expert quotes to enhance credibility
       c. Ideas for visual elements (e.g., infographics, charts) to support the content
    5. Provide guidance on the overall tone and style that would best resonate with the target audience.

    Your output should be a structured content plan document that serves as a comprehensive roadmap for the content creator.
    """,
    expected_output="A detailed content strategy document including audience analysis, SEO keywords, content structure, and resource suggestions.",
    agent=planner
)

write = Task(
    description="""
    Using the provided content plan, craft a compelling and informative blog post on {topic}. Your task includes:

    1. Writing an engaging introduction that hooks the reader and clearly states the post's purpose.
    2. Developing each main section with depth and insight, ensuring a logical flow of ideas.
    3. Naturally incorporating the provided SEO keywords throughout the content.
    4. Using transitions to maintain coherence between sections.
    5. Crafting a conclusion that summarizes key points and includes a clear call-to-action.
    6. Incorporating relevant data, statistics, or expert quotes as suggested in the content plan.
    7. Suggesting placements for visual elements to enhance the content's impact.
    8. Ensuring the post aligns with the specified tone and style guidelines.

    Format your post in markdown, with proper headings, subheadings, and paragraph breaks. Aim for a length of 1000-1500 words, with each main section containing 2-3 well-developed paragraphs.
    """,
    expected_output="A well-structured, SEO-optimized blog post in markdown format, ready for editorial review.",
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

    Provide your edits and suggestions directly in the document, using track changes or comments where appropriate. If major revisions are needed, clearly explain your reasoning and provide guidance for improvements.
    """,
    expected_output="A polished, publication-ready blog post with tracked changes and editorial comments where necessary.",
    agent=editor
)

crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)
# result = crew.kickoff(inputs={"topic": "Artificial Intelligence"})
# print(result)
def create_blog(id, topic):
   
    result = crew.kickoff(inputs={"topic": topic})
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

