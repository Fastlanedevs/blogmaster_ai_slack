# agents.py

import os
from textwrap import dedent
from crewai import Agent
from langchain_anthropic import ChatAnthropic
from crewai_tools import SerperDevTool
from langchain.tools import Tool
from langchain.utilities import RequestsWrapper
from langchain_community.llms import Ollama
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")
class ContentGenerationAgents:
    def __init__(self):
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20240620",
            anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
            temperature=0.7
        )
        # self.llm = Ollama(
        #     model="llama3.1",
        #     base_url="http://localhost:11434"
        # )
        self.search_tool = SerperDevTool()
        self.requests_get_tool = Tool(
            name="requests_get",
            description="A tool for making GET requests to websites and fetching their content.",
            func=RequestsWrapper().get
        )

    def web_scraper_agent(self):
        return Agent(
            role="Web Scraper",
            goal="Extract relevant information from provided URLs",
            backstory="You are an expert web scraper, capable of efficiently extracting valuable information from various websites while respecting robots.txt rules and website terms of service.",
            tools=[self.requests_get_tool],
            llm=self.llm,
            verbose=False
        )

    def content_summarizer_agent(self):
        return Agent(
            role="Content Summarizer",
            goal="Synthesize and summarize scraped content into concise, informative summaries",
            backstory="You are a skilled content analyst with a talent for distilling large amounts of information into clear, concise summaries that capture the essence of the original content.",
            tools=[],
            llm=self.llm,
            verbose=False
        )

    def content_idea_generator_agent(self):
        return Agent(
            role="Content Idea Generator",
            goal="Generate creative and engaging post ideas for various social media channels",
            backstory="You are a creative powerhouse, known for generating innovative content ideas that resonate with diverse audiences across different social media platforms.",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=False
        )

    def writer_agent(self):
        return Agent(
            role="Content Writer",
            goal="Create engaging, platform-specific content based on provided topics",
            backstory="You are a versatile writer with a talent for crafting compelling narratives across various platforms. Your writing is known for its clarity, engagement, and ability to convey complex ideas in an accessible manner.",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=False
        )

    def editor_agent(self):
        return Agent(
            role="Content Editor",
            goal="Refine and polish content to ensure quality, coherence, and adherence to style guidelines",
            backstory="You are a meticulous editor with a sharp eye for detail and a deep understanding of language nuances. Your expertise ensures that all content is polished, error-free, and optimized for maximum impact.",
            tools=[],
            llm=self.llm,
            verbose=False
        )

    def visual_concept_creator_agent(self):
        return Agent(
            role="Visual Concept Creator",
            goal="Create compelling visual concepts for content across various platforms",
            backstory="You are a creative visual designer with expertise in conceptualizing images that complement and enhance written content across various platforms. Your skills in describing visual concepts ensure that the content is not only informative but also visually appealing.",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=False
        )