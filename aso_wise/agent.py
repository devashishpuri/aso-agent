"""
ASO_Wise: Multi-Agent App Store Optimization System

A simplified multi-agent system that automates App Store Optimization using:
- Keyword Research Agent (uses Google Search)
- Competitor Analysis Agent (uses Google Search)
- Content Writer Agent (creates optimized listings)
"""

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.adk.tools import google_search
from google.genai import types
import json

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 502, 503, 504],
)


# ============================================================================
# CUSTOM TOOL: App Store Guidelines Validator
# ============================================================================

def validate_app_store_content(title: str, description: str, store: str = "both") -> str:
    """
    Validates app store listing content against platform guidelines.
    
    Args:
        title: App title to validate
        description: App description to validate  
        store: Target store ('ios', 'android', or 'both')
    
    Returns:
        JSON with validation results, issues, and recommendations
    """
    issues = []
    warnings = []
    
    # Title length validation
    if store in ["ios", "both"] and len(title) > 30:
        issues.append(f"iOS title too long: {len(title)} chars (max 30)")
    if store in ["android", "both"] and len(title) > 50:
        warnings.append(f"Android title long: {len(title)} chars (recommended max 30)")
    
    # Check for keyword stuffing
    words = title.lower().split()
    if len(words) != len(set(words)):
        warnings.append("Title has repeated words (possible keyword stuffing)")
    
    # Prohibited terms
    prohibited = ["#1", "best", "top rated", "free download"]
    for term in prohibited:
        if term in title.lower():
            warnings.append(f"Discouraged term in title: '{term}'")
    
    # Description validation
    if len(description) < 200:
        warnings.append(f"Description short: {len(description)} chars (recommended 500+)")
    if len(description) > 4000:
        issues.append(f"Description too long: {len(description)} chars (max 4000)")
    
    return json.dumps({
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "title_length": len(title),
        "description_length": len(description),
        "recommendations": [
            "Use natural language",
            "Focus on user benefits",
            "Include clear call-to-action",
            "Use bullet points for readability"
        ]
    }, indent=2)


# ============================================================================
# SPECIALIZED AGENTS
# ============================================================================

# 1. Keyword Research Agent (uses Google Search for real data)
keyword_research_agent = Agent(
    name="keyword_researcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are an ASO keyword researcher. Your task:

1. Analyze the app description and category
2. Generate 15-20 relevant keyword ideas
3. Use google_search to research each keyword:
   - Search for "keyword app" to see competition
   - Search for "keyword app store" to see existing apps
   - Analyze search results to gauge popularity and competition

4. Categorize keywords:
   - Primary (5-7): High relevance, good search presence
   - Secondary (5-8): Medium relevance, moderate competition  
   - Long-tail (5-8): Specific phrases, lower competition

Return a structured analysis with keyword recommendations.""",
    tools=[google_search],
    output_key="keyword_research",
)

# 2. Competitor Analysis Agent (uses Google Search)
competitor_analysis_agent = Agent(
    name="competitor_analyst",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a competitive analysis expert for app stores. Your task:

1. Use google_search to find top competitor apps:
   - Search "best [category] apps"
   - Search "top [category] apps ios/android"
   - Search for specific app types mentioned in the description

2. Analyze search results to identify:
   - Common keywords in top app titles
   - Popular features mentioned in descriptions
   - Patterns in successful apps
   - Gaps and opportunities

3. Provide insights:
   - What works in this category
   - How to differentiate
   - Unique positioning opportunities

Return a competitive analysis with actionable recommendations.""",
    tools=[google_search],
    output_key="competitor_analysis",
)

# 3. Content Writer Agent
content_writer_agent = Agent(
    name="content_writer",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are an ASO copywriter. Your task:

1. Review keyword research and competitive analysis from previous agents
2. Create 3 variants of:
   - Title (max 30 chars for iOS, 50 for Android)
   - Subtitle (short value proposition)
   - Description (500-1000 words, keyword-optimized)
   - Backend keywords (comma-separated)

3. Writing principles:
   - Lead with benefits, not features
   - Natural keyword integration
   - Clear call-to-action
   - Scannable format (bullets, short paragraphs)

4. Use validate_app_store_content to check each variant

Return 3 complete variants with strategy explanations.

**Keyword Research:**
{keyword_research}

**Competitor Analysis:**
{competitor_analysis}""",
    tools=[validate_app_store_content],
    output_key="content_variants",
)


# 4. Final Aggregator Agent (synthesizes everything)
aggregator_agent = Agent(
    name="aso_aggregator",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are the ASO_Wise final advisor. Review all the research and content variants to provide a comprehensive recommendation.

**Keyword Research:**
{keyword_research}

**Competitor Analysis:**
{competitor_analysis}

**Content Variants:**
{content_variants}

Your task:
1. Analyze all 3 content variants
2. Evaluate each variant based on:
   - Keyword optimization
   - Competitive positioning
   - App store guideline compliance
   - User appeal and clarity

3. Provide a clear recommendation:
   - Which variant is best and why
   - Key strengths of the recommended variant
   - Any final tweaks or suggestions
   - Summary of the overall ASO strategy

4. Present the final recommended listing in a clean, ready-to-use format

Be conversational and explain your reasoning. Help the user understand why this approach will work.""",
)


# ============================================================================
# ROOT AGENT (Orchestrator)
# ============================================================================

from google.adk.agents import SequentialAgent

root_agent = SequentialAgent(
    name="aso_wise",
    sub_agents=[
        keyword_research_agent,
        competitor_analysis_agent,
        content_writer_agent,
        aggregator_agent,
    ],
)
