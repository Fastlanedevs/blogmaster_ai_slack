# tasks.py

from crewai import Task
from textwrap import dedent

class ContentGenerationTasks:
    def scrape_url(self, agent, url):
        return Task(
            description=dedent(f"""
                Scrape the content from the following URL: {url}
                Extract relevant information, including main text, titles, and any important metadata.
                Respect robots.txt rules and website terms of service.
            """),
            agent=agent,
            expected_output="A comprehensive summary of the scraped content from the given URL."
        )

    def summarize_content(self, agent):
        return Task(
            description=dedent("""
                Summarize the scraped content from all provided URLs.
                Create a concise yet comprehensive summary that captures the key points and themes.
                Highlight any common threads or contradictions across the different sources.
            """),
            agent=agent,
            expected_output="A concise summary of the key points and themes from all scraped content."
        )

    def generate_post_ideas(self, agent):
        return Task(
            description=dedent("""
                Based on the summarized content, generate post ideas for different social media channels:
                1. 5 ideas for blog posts
                2. 5 ideas for LinkedIn posts
                3. 5 ideas for Twitter posts
                Ensure each idea is tailored to the specific platform and likely to engage the target audience.
                Format the output as follows:
                Blog Ideas:
                1. [Idea 1]
                2. [Idea 2]
                3. [Idea 3]
                4. [Idea 4]
                5. [Idea 5]

                LinkedIn Ideas:
                1. [Idea 1]
                2. [Idea 2]
                3. [Idea 3]
                4. [Idea 4]
                5. [Idea 5]

                Twitter Ideas:
                1. [Idea 1]
                2. [Idea 2]
                3. [Idea 3]
                4. [Idea 4]
                5. [Idea 5]
            """),
            agent=agent,
            expected_output="A formatted list of 15 post ideas: 5 for blog posts, 5 for LinkedIn, and 5 for Twitter."
        )

    def write_post(self, agent, topic, channel):
        return Task(
            description=dedent(f"""
                Create a {channel} post on the topic: {topic}
                Use the provided topic to craft informative and engaging content.
                Tailor the content to the specific requirements and audience of {channel}.
                For a blog post, aim for 1000-1500 words with proper structure and SEO optimization.
                For LinkedIn, create a professional post of 1300-1700 characters.
                For Twitter, craft an engaging tweet within the 280 character limit.
                Incorporate relevant hashtags and calls-to-action where appropriate.
            """),
            agent=agent,
            expected_output=f"A complete {channel} post on the topic: {topic}"
        )

    def edit_post(self, agent, channel):
        return Task(
            description=dedent(f"""
                Review and edit the {channel} post.
                Ensure the content is clear, concise, and error-free.
                Check for proper structure, flow, and adherence to the platform's best practices.
                Optimize for engagement and readability.
                Provide the final, polished version of the content.
            """),
            agent=agent,
            expected_output=f"A polished and edited version of the {channel} post."
        )

    def create_visual_concept(self, agent, topic, channel):
        return Task(
            description=dedent(f"""
                Create a detailed description for a visual concept to accompany the {channel} post on the topic: {topic}
                The description should be suitable for AI image generation.
                Consider:
                1. The main theme or message of the content
                2. Key elements that should be included
                3. Style and mood that aligns with the content's tone and the {channel} platform
                4. Any specific details that would make the image unique and engaging
                Provide a clear, detailed description that could be used as a prompt for AI image generation.
                Limit the description to 100 words or less.
            """),
            agent=agent,
            expected_output=f"A detailed description (100 words or less) of a visual concept for the {channel} post on {topic}."
        )