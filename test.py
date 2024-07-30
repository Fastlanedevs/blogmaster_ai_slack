# test.py

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='dotenv')

from pymongo import MongoClient
from bson.objectid import ObjectId
from crewai import Crew
from dotenv import load_dotenv
from agents import ContentGenerationAgents
from tasks import ContentGenerationTasks
from image_generation import generate_image_with_nvidia_nim
import os

load_dotenv()

# MongoDB connection
client = MongoClient(os.environ["MONGO_DB_URI"])
db = client["articles"]
collection = db["tasks"]

def parse_post_ideas(ideas_text):
    ideas = {"blog": [], "linkedin": [], "twitter": []}
    current_platform = None
    for line in ideas_text.split('\n'):
        line = line.strip()
        if line.endswith("Ideas:"):
            current_platform = line.lower().split()[0]
        elif line and current_platform:
            # Remove the number at the beginning of the idea
            idea = line.split('. ', 1)[-1] if '. ' in line else line
            ideas[current_platform].append(idea)
    return ideas

def analyze_urls(urls):
    agents = ContentGenerationAgents()
    tasks = ContentGenerationTasks()

    scraper = agents.web_scraper_agent()
    summarizer = agents.content_summarizer_agent()
    idea_generator = agents.content_idea_generator_agent()

    scrape_tasks = [tasks.scrape_url(scraper, url) for url in urls]
    summarize_task = tasks.summarize_content(summarizer)
    generate_ideas_task = tasks.generate_post_ideas(idea_generator)

    crew = Crew(
        agents=[scraper, summarizer, idea_generator],
        tasks=scrape_tasks + [summarize_task, generate_ideas_task],
        verbose=2
    )

    result = crew.kickoff()

    if isinstance(result, dict):
        summary = result.get('summarize_content', '')
        post_ideas = parse_post_ideas(result.get('generate_post_ideas', ''))
    elif isinstance(result, list):
        summary = result[-2]
        post_ideas = parse_post_ideas(result[-1])
    else:
        # If the result is a string, it likely contains both summary and ideas
        parts = str(result).split("Blog Ideas:", 1)
        summary = parts[0].strip()
        post_ideas = parse_post_ideas("Blog Ideas:" + parts[1] if len(parts) > 1 else "")

    return summary, post_ideas

def create_content(topic, channel):
    agents = ContentGenerationAgents()
    tasks = ContentGenerationTasks()

    writer = agents.writer_agent()
    editor = agents.editor_agent()
    visual_creator = agents.visual_concept_creator_agent()

    write_post_task = tasks.write_post(writer, topic, channel)
    edit_post_task = tasks.edit_post(editor, channel)
    create_visual_task = tasks.create_visual_concept(visual_creator, topic, channel)

    crew = Crew(
        agents=[writer, editor, visual_creator],
        tasks=[write_post_task, edit_post_task, create_visual_task],
        verbose=2
    )

    result = crew.kickoff()

    if isinstance(result, dict):
        edited_post = result.get('edit_post', '')
        visual_concept = result.get('create_visual_concept', '')
    elif isinstance(result, list):
        edited_post = result[-2]
        visual_concept = result[-1]
    else:
        edited_post = str(result)
        visual_concept = str(result)

    image_result = generate_image_with_nvidia_nim(visual_concept)

    return edited_post, visual_concept, image_result

def main():
    urls = input("Enter the URLs to analyze (comma-separated): ").split(',')
    summary, post_ideas = analyze_urls(urls)

    print("\nContent Summary:")
    print(summary)
    print("\nPost Ideas:")
    for platform, ideas in post_ideas.items():
        print(f"\n{platform.capitalize()} Ideas:")
        for i, idea in enumerate(ideas, 1):
            print(f"{i}. {idea}")

    results = {}
    for channel in ['blog', 'linkedin', 'twitter']:
        topic = post_ideas[channel][0] if post_ideas[channel] else f"Default topic for {channel}"
        print(f"\nGenerating content for {channel.capitalize()} - Topic: {topic}")
        content, image_prompt, image_result = create_content(topic, channel)
        results[channel] = {
            'topic': topic,
            'content': content,
            'image_prompt': image_prompt,
            'image_result': image_result
        }
        print(f"Content generated for {channel.capitalize()}")

    # Update database
    data = {
        "_id": ObjectId(),
        "status": "completed",
        "summary": summary,
        "post_ideas": post_ideas,
        "results": results,
        
    }
    collection.insert_one(data)

    print("\nContent generation complete. Results stored in database.")

    # Print generated content for review
    for channel, result in results.items():
        print(f"\n--- {channel.upper()} CONTENT ---")
        print(f"Topic: {result['topic']}")
        print("Content:")
        print(result['content'])
        print("Image Prompt:")
        print(result['image_prompt'])
        print("Image Result:")
        print(result['image_result'])
        print("------------------------")

if __name__ == "__main__":
    main()