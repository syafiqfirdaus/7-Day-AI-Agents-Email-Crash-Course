# Evaluation Guide

## Quick Start

### Option 1: Evaluate Existing User Interactions

If you already have user interaction logs, you can evaluate them directly:

1. Open `evaluations.ipynb`
2. Make sure `source_filter = 'user'` (this is the default now)
3. Run all cells

This will evaluate your existing user logs.

### Option 2: Generate AI Test Data First

If you want to generate synthetic test data:

1. First run `data-gen.ipynb` to generate test questions and log AI responses
2. Then run `evaluations.ipynb` with `source_filter = 'ai-generated'`

## Troubleshooting

### "Loaded 0 log files for evaluation"

This happens when the filter criteria don't match your logs. Check:

1. **Agent Name**: The `agent_name` variable must match your log filenames
   - Look at your log files: `ls logs/*.json`
   - If files are named `gh_agent_*.json`, use `agent_name = 'gh_agent'`
   - If files are named `faq_agent_v2_*.json`, use `agent_name = 'faq_agent_v2'`

2. **Source Filter**: Must match the `source` field in your logs
   - User interactions: `source_filter = 'user'`
   - AI-generated test data: `source_filter = 'ai-generated'`
   - Evaluate all logs: `source_filter = None`

3. **Check your logs**:
   ```bash
   # See what's in your logs
   cat logs/gh_agent_*.json | jq '{agent_name, source}'
   ```

## Current Log Status

Your current logs have:
- **Agent name**: `gh_agent`
- **Source**: `user` (from actual user interactions)
- **Count**: ~10 log files

To evaluate these, use:
```python
agent_name = 'gh_agent'
source_filter = 'user'
```

## Understanding the Evaluation

The evaluation system uses an LLM as a judge to assess:
- **instructions_follow**: Did the agent follow instructions?
- **instructions_avoid**: Did it avoid prohibited actions?
- **answer_relevant**: Is the answer relevant to the question?
- **answer_clear**: Is the answer clear and correct?
- **answer_citations**: Are proper citations included?
- **completeness**: Does it cover all aspects?
- **tool_call_search**: Was the search tool used?

Results are saved to `logs/evaluation_results.csv`.
