# Composio App Research Agent

Research and verification pipeline for the Composio AI Product Ops Intern take-home assignment.

## What it does

The pipeline researches the 100-app set and produces structured evidence for:

- category and one-line description
- authentication methods
- self-serve vs gated credential access
- API type and breadth
- MCP availability
- agent-toolkit buildability and blocker
- official evidence URLs
- evidence snippets and confidence

It then runs a separate verification pass that looks for missing evidence, contradictions, low-confidence classifications, and claims that should be checked against official documentation. The final report is designed to make first-pass vs verified accuracy auditable rather than hiding mistakes.

## Architecture

```text
apps.json
   |
   v
Research Agent -> official-doc discovery -> structured extraction
   |                         |
   +---- evidence + confidence
                             |
                             v
                       Verification Agent
                             |
                    +--------+--------+
                    |                 |
                 auto-check       human sample
                    |                 |
                    +--------+--------+
                             v
                    verified_results.json
                             |
                             v
                      pattern analysis
                             |
                             v
                     case-study/index.html
```

## Setup

Python 3.11+ is recommended.

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\\Scripts\\activate

pip install -r requirements.txt
cp .env.example .env
```

Set the API credentials required by your chosen model/search providers. Composio credentials are optional for the baseline research path but the project is structured so Composio tools/MCP can be plugged into the research session.

## Run

```bash
python run.py --input apps.json --output data/raw_results.json
python run.py --input apps.json --output data/raw_results.json --verify
python analysis/patterns.py --input data/verified_results.json --output data/patterns.json
```

The HTML case study is a self-contained static page under `case-study/index.html`.

## Evidence policy

The agent is instructed to prefer official developer documentation, pricing/developer-access pages, and official MCP documentation/repositories. Search snippets are discovery aids, not final evidence. A result should be marked uncertain when the evidence does not support the classification.

## Verification policy

The verifier checks a sample and all low-confidence/contradictory records. Human review is required for ambiguous pricing gates, conflicting authentication documentation, unclear MCP provenance, and apps without a clear public developer path. The case study should report the actual sample size, errors and corrected rows after running the pipeline.

## Important honesty rule

Do not replace unknown values with guesses and do not claim an accuracy percentage until the research and verification runs have actually completed. The supplied case-study template deliberately leaves those figures data-driven.
