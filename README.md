# ASO_Wise: Multi-Agent App Store Optimization System

## Overview

ASO_Wise is an intelligent multi-agent system that automates App Store Optimization (ASO) for mobile app developers. It uses specialized AI agents and Google Search to generate professional-quality app store listings in minutes.

## The Problem

- Most of the apps never get discovered in app stores
- ASO requires specialized expertise most developers lack
- Developers need keyword research, competitive analysis, and expert copywriting

## The Solution

ASO_Wise automates the entire ASO workflow using **4 specialized AI agents**:

1. **Keyword Research Agent** - Uses Google Search to find optimal keywords
2. **Competitor Analysis Agent** - Analyzes top apps using Google Search  
3. **Content Writer Agent** - Creates 3 optimized listing variants
4. **Aggregator Agent** - Synthesizes all findings and recommends the best variant


## Architecture

```
User Input (App Description)
         ↓
Sequential Agent (Root)
         ↓
    Keyword Research Agent
    (Google Search)
         ↓
    Competitor Analysis Agent
    (Google Search)
         ↓
    Content Writer Agent
    (Validator Tool)
         ↓
    Aggregator Agent
    (Final Recommendation)
         ↓
Best Variant + Strategy
```

## Features

### Multi-Agent System
- 4 specialized agents working in sequence
- Sequential orchestration ensures proper data flow
- Each agent builds on previous agent's output
- Final aggregator provides cohesive recommendation

### Tools
- **Google Search** (built-in tool) for keyword and competitor research
- **Custom Validator Tool** for guideline compliance

### Output
- 3 complete app store listing variants
- Keyword strategy with primary/secondary/long-tail keywords
- Competitive analysis and positioning insights
- Guideline validation (iOS/Android)

## Installation

```bash
# Install ADK
pip install google-adk

# Configure API key
echo "GOOGLE_API_KEY=your_key_here" > .env
```

## Usage

### Run the Agent

```bash
adk run aso_wise
```

or to use ADK web run,

```bash
adk web
```

and choose aso_wise from the agents' list

### Example Interaction

**You:**
```
I have a meditation app for busy professionals with 10-minute 
guided sessions and sleep stories. Category: Health & Fitness.
```

**ASO_Wise will:**
1. Research keywords using Google Search
2. Analyze competitor apps using Google Search
3. Generate 3 optimized listing variants with validation
4. Synthesize findings and recommend the best variant with strategic reasoning

**Note about Tool Execution:**
- Google Search is a real API call and takes time to complete
- The agent will show "Thinking..." or similar status while tools execute
- Responses stream back as they're generated
- Total process typically takes 1-3 minutes for complete optimization

**Output includes:**
- Keyword research with primary/secondary/long-tail categories
- Competitive analysis with positioning insights
- 3 complete listing variants (title, subtitle, description, keywords)
- Validation results for each variant
- Final recommendation with the best variant
- Strategic reasoning and implementation guidance


### Execution Time

- **Keyword Research**: 10-30 seconds (multiple Google searches)
- **Competitor Analysis**: 10-30 seconds (multiple Google searches)
- **Content Writing**: 20-40 seconds (generating 3 variants + validation)
- **Final Aggregation**: 10-20 seconds (analyzing and recommending)
- **Total**: 1-3 minutes for complete optimization with final recommendation

### Tips

- Be patient - real API calls take time
- Watch for status updates in the terminal
- The agent explains what it's doing at each step
- If it seems stuck, wait 30 seconds - tools may still be executing

### Key Components

**1. Keyword Research Agent**
- Uses `google_search` tool
- Searches for "{keyword} app" and "{keyword} app store"
- Analyzes search results for competition and popularity
- Categorizes into primary/secondary/long-tail keywords

**2. Competitor Analysis Agent**
- Uses `google_search` tool
- Searches for "best {category} apps"
- Identifies patterns in successful apps
- Finds gaps and opportunities

**3. Content Writer Agent**
- Uses custom `validate_app_store_content` tool
- Creates 3 variants with different optimization strategies
- Validates against iOS/Android guidelines
- Ensures proper keyword integration

**4. Aggregator Agent**
- Reviews all research and content variants
- Evaluates each variant based on multiple criteria
- Recommends the best variant with clear reasoning
- Provides final polished listing ready to use

**Root Agent (Sequential Orchestrator)**
- Runs agents in sequence: keyword → competitor → content → aggregator
- Passes outputs between agents via session state
- Ensures each agent has context from previous steps

### Custom Tool: validate_app_store_content

Validates app store listings against platform guidelines:
- Title length (iOS: 30 chars, Android: 50 chars)
- Keyword stuffing detection
- Prohibited terms check
- Description length validation
- Returns issues, warnings, and recommendations

## Example Output

### Input
"Fitness tracking app with AI-powered workout recommendations. Category: Health & Fitness"

### Output Structure
```
📊 KEYWORD RESEARCH
Primary Keywords:
- fitness tracker
- workout app
- AI fitness

📈 COMPETITIVE ANALYSIS
Top Competitors:
- FitPro (4.5★, 500K+ downloads)
- WorkoutMaster (4.3★, 300K+ downloads)

✍️ CONTENT VARIANTS
Variant A (SEO-Optimized):
Title: "AI Fitness Tracker - Smart Workouts"
[Full listing...]

Variant B (User-Focused):
Title: "FitGenius: Your AI Workout Coach"
[Full listing...]

Variant C (Balanced):
Title: "AI Fitness & Workout Tracker"
[Full listing...]

🏆 RECOMMENDATION: Variant C (Best balance)
```
