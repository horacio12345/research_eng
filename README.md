# Research Automation Tool

A simple, maintainable Python program that periodically searches for high-quality information about generative AI applications in engineering projects.

## Overview

This tool automatically:
- Searches the web using Tavily API
- Filters and ranks results using AI (OpenAI GPT models)
- Generates human-readable Markdown reports and machine-friendly JSON data
- Focuses on recent, relevant content about generative AI in engineering

## Features

✅ **Modular Architecture**: Clean separation into focused modules (50-100 lines each)  
✅ **Externalized Prompts**: AI prompts in dedicated files for easy iteration and version control  
✅ **Interactive Browser UI**: Beautiful, filterable web interface for viewing results  
✅ **AI-Powered Filtering**: Uses LangChain + OpenAI to assess relevance and quality  
✅ **Configurable**: YAML-based configuration for topics, filters, and outputs  
✅ **Triple Output**: Markdown reports + JSON data + Interactive HTML viewer    

## Installation

### 1. Prerequisites

- Python 3.11+
- Virtual environment (`.uvenv` already created)

### 2. Install Dependencies

```bash
# Activate virtual environment
source .uvenv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Configure API Keys

Edit your `.env` file with your API keys:

```bash
# Required for web search
TAVILY_API_KEY=your_tavily_api_key_here

# Required for AI analysis
OPENAI_API_KEY=your_openai_api_key_here
```

**Get API Keys:**
- Tavily: https://tavily.com (sign up for free tier)
- OpenAI: https://platform.openai.com/api-keys

## Configuration

Edit `config.yaml` to customize:

### Topics

```yaml
topics:
  - name: "Your Topic Name"
    keywords:
      - "keyword1"
      - "keyword2"
    search_variations:
      - '"specific query" 2025 pdf'
      - '"another query" 2024 2025'
```

### Search Settings

```yaml
tavily:
  search_depth: "advanced"  # or "basic"
  max_results: 8
  exclude_domains:
    - "youtube.com"
```

### AI Settings

```yaml
ai:
  primary_model: "gpt-4o-mini"  # Fast and cost-effective
  temperature: 0.3
  use_ai_filtering: true
```

### Filtering

```yaml
filtering:
  min_year: 2024
  top_n_per_topic: 15
  required_keywords:
    - "engineering"
    - "management"
```

## Usage

### Run the Tool

```bash
# Activate virtual environment
source .uvenv/bin/activate

# Run the refactored tool (v2.0)
python run_research.py

# Or run as module
python -m src.main
```

### Output

The tool generates **three files** in the `outputs/` directory:

1. **Markdown Report** (`research_report_YYYYMMDD_HHMMSS.md`)
   - Human-readable with clickable links
   - Organized by topic
   - Includes AI-generated summaries
   - **View in any Markdown viewer or browser**

2. **JSON Data** (`research_data_YYYYMMDD_HHMMSS.json`)
   - Machine-friendly structured data
   - Complete metadata for each result
   - Easy to parse and integrate with other tools

3. **Interactive Browser View** (`research_browser_YYYYMMDD_HHMMSS.html`) ✨ **NEW**
   - Beautiful, responsive web interface
   - Real-time search and filtering
   - Sort by relevance, date, or title
   - Filter by topic, minimum relevance score
   - **Just open in your browser - no server needed!**

### Example Output Structure

**Markdown Report:**
```markdown
# Research Report: Generative AI in Engineering

**Generated:** 2025-12-09 11:43:00

## Generative AI in Engineering Project Management

### 1. Title of Article
📅 2025 | 🌐 example.com | ⭐ Relevance: 0.92

🔗 [View Article](https://example.com/article)

**Summary:** AI-generated 1-2 sentence summary of key insights...
```

**JSON Data:**
```json
{
  "generated_at": "2025-12-09T11:43:00",
  "topics": {
    "Topic Name": [
      {
        "title": "Article Title",
        "url": "https://...",
        "snippet": "...",
        "published_date": "2025",
        "domain": "example.com",
        "relevance_score": 0.92,
        "ai_summary": "..."
      }
    ]
  }
}
```

## Scheduling with Cron

To run automatically (e.g., weekly):

```bash
# Edit crontab
crontab -e

# Add this line (runs every Monday at 9 AM)
0 9 * * 1 cd /Users/horacio/AI/research_eng && source .uvenv/bin/activate && python src/main.py >> logs/cron.log 2>&1
```

## Architecture (v2.0)

### Design Principles

- **Modular Design**: Each module has single responsibility (50-100 lines)
- **Externalized Configuration**: Prompts in separate files for easy iteration 
- **Type-safe**: Full type hints on all functions
- **Well-tested**: Importable modules for easy unit testing
- **Clear Separation**: Core, Search, AI, Filters, Output, UI layers

### New Modular Structure

```
research_eng/
├── run_research.py          # Main launcher script
├── config.yaml              # Configuration
├── src/
│   ├── core/                # Data models & config
│   │   ├── models.py        #   Result, Topic, SearchConfig
│   │   └── config.py        #   load_config()
│   ├── search/              # Search functionality
│   │   ├── query_builder.py #   build_queries_for_topic()
│   │   └── tavily_client.py #   tavily_search()
│   ├── ai/                  # AI analysis
│   │   ├── prompts/         #   ✨ Externalized prompts
│   │   │   ├── relevance_analysis.txt
│   │   │   └── summary_generation.txt
│   │   ├── prompt_loader.py #   load_prompt()
│   │   └── analyzer.py      #   AI analysis logic
│   ├── filters/             # Filtering & ranking
│   │   ├── date_filter.py
│   │   ├── deduplicator.py
│   │   ├── keyword_filter.py
│   │   └── ranking.py       #   Orchestrates all filters
│   ├── output/              # Output generation
│   │   ├── markdown_generator.py
│   │   └── json_generator.py
│   ├── ui/                  # ✨ NEW: Browser UI
│   │   ├── browser_view.py
│   │   └── templates/
│   │       └── results.html #   Interactive viewer
│   └── main.py              # Orchestration (111 lines!)
└── outputs/                 # Generated files
```

### Benefits of v2.0 Refactoring

✅ **Maintainability**: 692 lines → 10 focused modules  
✅ **Prompt Management**: Easy to edit and version AI prompts  
✅ **Testability**: Each module can be tested independently  
✅ **Extensibility**: Add new filters, outputs without touching core  
✅ **Browser UI**: Interactive results viewer with filtering  

## Customization

### Edit AI Prompts ✨ NEW

The v2.0 refactoring makes prompts easy to customize! Just edit the text files:

**Relevance Analysis Prompt:**
```bash
nano src/ai/prompts/relevance_analysis.txt
```

**Summary Generation Prompt:**
```bash
nano src/ai/prompts/summary_generation.txt
```

Changes take effect immediately on the next run. Great for:
- Experimenting with different prompt styles
- Adding domain-specific instructions
- A/B testing prompt effectiveness
- Version controlling prompt iterations

### Swap Search Provider

The search layer is abstracted. To use a different provider:

1. Implement a new function matching the signature:
   ```python
   def new_search(query: str, max_results: int, ...) -> List[Result]:
       # Your implementation
       pass
   ```

2. Replace `tavily_search()` calls in `main()`

### Adjust AI Models

In `config.yaml`:
```yaml
ai:
  primary_model: "gpt-4"  # More powerful but slower/costlier
  # or
  primary_model: "gpt-3.5-turbo"  # Faster and cheaper
```

### Disable AI Filtering

For faster, cheaper runs without AI analysis:

```yaml
ai:
  use_ai_filtering: false
```

Results will be sorted by date only.

## Troubleshooting

### Missing API Keys

```
ValueError: Missing required API keys: TAVILY_API_KEY
```
→ Check your `.env` file has the correct API keys

### Tavily API Errors

```
Tavily API request failed: 401 Unauthorized
```
→ Verify your `TAVILY_API_KEY` is valid

### No Results Found

- Check your `min_year` isn't too restrictive
- Try broader search queries
- Reduce `required_keywords` constraints
- Set `search_depth: "advanced"` for better results

## Cost Optimization

### Reduce API Costs

1. **Use fewer queries per topic**: Remove search variations
2. **Lower max_results**: Set `max_results: 5`
3. **Disable AI filtering**: Set `use_ai_filtering: false`
4. **Use cheaper model**: Set `primary_model: "gpt-3.5-turbo"`

### Estimated Costs (per run)

- Tavily: ~$0.005 per search (advanced), $0.001 (basic)
- OpenAI GPT-4o-mini: ~$0.01-0.05 per run
- **Total: ~$0.05-0.15 per full run** (4 topics, AI enabled)

## Project Structure

```
research_eng/
├── .env                    # API keys (gitignored)
├── .uvenv/                 # Virtual environment
├── config.yaml             # Configuration file
├── requirements.txt        # Python dependencies
├── src/
│   └── main.py            # Main application
└── outputs/               # Generated reports (created automatically)
    ├── research_report_*.md
    └── research_data_*.json
```

## License

This tool is provided as-is for research and automation purposes.

## Support

For issues or questions:
1. Check the logs (set `logging.DEBUG` in code)
2. Verify API keys are correctly set
3. Review the configuration file syntax
4. Test with a minimal config first

---

**Built with:** Python 3.11 | LangChain | Tavily | OpenAI
