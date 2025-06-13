import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import Agent, Runner, WebSearchTool, ModelSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("OPENAI_API_KEY not found in environment variables", file=sys.stderr)
    raise ValueError("OPENAI_API_KEY must be set")

# Define request schemas
class TopicsRequest(BaseModel):
    topics: list[str]

class FormatRequest(BaseModel):
    raw_content: str
    topics: list[str]

# Initialize FastAPI app with root path for Vercel
app = FastAPI(title="AI Newsletter Agents", root_path="/api/agents")

@app.get("/ping")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "openai_api_key_set": bool(OPENAI_API_KEY),
        "vercel_url": os.getenv("VERCEL_URL", "not set"),
        "python_version": sys.version,
        "agents_imported": "agents" in sys.modules,
    }

# Research Agent: Searches web and generates newsletter content
research_agent = Agent(
    name="Research Agent",
    model="gpt-4.1",
    instructions=(
        "You are an AI assistant that creates insightful, well-connected newsletters on a set of given topics.\n\n"
        "Your process:\n"
        "1. Search the web comprehensively for the latest news and information on each one of the given topics individually:\n"
        "   - Perform multiple searches with different query variations to ensure broad coverage\n"
        "   - Look for recent articles (prioritize content from the last 7-30 days)\n"
        "   - Search for both general news and specific expert analysis\n"
        "   - If initial results are insufficient, refine your search queries and search again\n"
        "2. Repeat the same approach to search for the other topics given\n"
        "3. For each topic, analyze the articles to identify connections, patterns, and relationships between them.\n"
        "4. Create a cohesive narrative that explains how these articles relate to each other.\n\n"
        "Your output structure:\n"
        "**[Create a compelling title that captures the essence of how all topics connect]**\n\n"
        "*[Write one impactful sentence that summarizes the key relationship or theme connecting all the topics]*\n\n"
        "**Executive Summary**\n"
        "Start with a compelling 2-3 paragraph summary that:\n"
        "- Identifies the main themes across all articles\n"
        "- Explains the connections and relationships between different pieces of information\n"
        "- Highlights why these connections matter\n"
        "- Provides context for how these topics intersect\n\n"
        "**Key Insights**\n"
        "- List 3-5 major insights that emerge from analyzing these articles together\n"
        "- Explain how different sources complement or contradict each other\n\n"
        "**Detailed Analysis**\n"
        "For each major theme or connection:\n"
        "- Provide specific examples from the articles\n"
        "- Include relevant facts, figures, and quotes\n"
        "- Cite sources properly\n\n"
        "**Conclusion**\n"
        "Synthesize everything into a forward-looking paragraph about implications and trends.\n\n"
        "Use clear, engaging language throughout.\n"
        "Focus on creating a narrative that shows how these topics interconnect rather than just listing summaries."
    ),
    tools=[ WebSearchTool() ]
)

# Formatting Agent: Transforms content into polished markdown
formatting_agent = Agent(
    name="Formatting Agent", 
    model="o3",
    instructions=(
        "You are an expert editor and markdown formatter who transforms research content into beautiful, readable newsletters.\n\n"
        "Your task:\n"
        "1. Take the provided research content and transform it into a polished newsletter\n"
        "2. Apply professional markdown formatting:\n"
        "   - Use **bold** for the main title\n"
        "   - Use *italics* for the one-sentence summary\n"
        "   - Structure content with clear hierarchical headers (##, ###)\n"
        "   - Create visually appealing lists with bullet points or numbers\n"
        "   - Add pull quotes using > blockquote syntax for key insights\n"
        "   - Use horizontal rules (---) to separate major sections\n"
        "   - Format links properly: [text](url)\n"
        "   - Add emphasis with **bold** and *italic* text strategically\n"
        "3. Enhance readability:\n"
        "   - Break up long paragraphs\n"
        "   - Add spacing between sections\n"
        "   - Create clear visual hierarchy\n"
        "   - Ensure smooth flow between sections\n"
        "4. Maintain all the original content and insights\n"
        "5. The output should be publication-ready markdown that looks professional when rendered\n\n"
        "Transform the content into an engaging, visually appealing newsletter while preserving all information."
    ),
    tools=[]
)

@app.post("/research")
async def generate_research(request: TopicsRequest):
    topics = request.topics
    if not topics:
        return {"error": "No topics provided."}
    
    # Get current date and yesterday for fresh news focus
    from datetime import datetime, timedelta
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    today_str = today.strftime("%B %d, %Y")
    yesterday_str = yesterday.strftime("%B %d, %Y")
    
    # Compose a prompt by joining the topics
    topics_list = ", ".join(topics)
    user_prompt = (
        f"Today is {today_str}. I need you to research and analyze these topics comprehensively: {topics_list}. "
        f"IMPORTANT: Focus specifically on news and events from the last 24 hours (since {yesterday_str}). "
        f"When searching, please include date filters like 'today', 'yesterday', 'last 24 hours', or specific dates like '{today_str}' and '{yesterday_str}' in your search queries. "
        f"Find the most recent developments, breaking news, and current events related to these topics. "
        f"Look for connections between them and create a detailed report emphasizing what's happening RIGHT NOW."
    )
    
    # Run the research agent
    result = await Runner.run(research_agent, user_prompt)
    raw_content = result.final_output
    
    return {"content": raw_content}

@app.post("/format")
async def format_newsletter(request: FormatRequest):
    raw_content = request.raw_content
    topics = request.topics
    
    if not raw_content:
        return {"error": "No content provided."}
    
    # Create formatting prompt
    topics_list = ", ".join(topics)
    user_prompt = f"Transform this research content into a beautifully formatted newsletter about {topics_list}. Apply professional markdown formatting:\n\n{raw_content}"
    
    # Run the formatting agent
    result = await Runner.run(formatting_agent, user_prompt)
    formatted_content = result.final_output
    
    return {"content": formatted_content}

# IMPORTANT: Handler for Vercel serverless functions
# Vercel's Python runtime will automatically handle FastAPI apps
# No additional configuration needed - just export the 'app' variable
