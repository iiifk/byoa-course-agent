# BYOA Course Agent

Single-purpose course report assistant for the software product practice course.

## Features

- Extracts text from `.docx`, `.pptx`, and `.pdf` course files.
- Reads public GitHub profile, repository, and pull request pages.
- Generates structured experiment-report drafts from real local context.
- Marks unverifiable links as pending instead of inventing data.

## Tools / Skills

- `document_reader`: parses local Word, PowerPoint, and PDF files.
- `github_reader`: fetches public GitHub page or API metadata.
- `report_writer`: writes generated content back into a report template.

## Core Prompt

See [prompts/core_prompt.md](prompts/core_prompt.md).

## Run

```bash
python agent.py --workspace "D:\codex po\8"
```

