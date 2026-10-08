<sub>[← all labs](../../README.md)</sub>

# Auditing robots.txt for AI crawlers

> robots.txt is a request, not a lock. You can still check whether it asks what you think it asks.

`Python` · `urllib.robotparser`

**Companion to:**
- [Age of AI Scrapers - Robots.txt](https://www.linkedin.com/pulse/age-ai-scrapers-robotstxt-tony-honesto-m1h4c/)

## What it shows

- Parses real-world robots.txt files with the standard library's `urllib.robotparser`.
- Checks a page against the published user-agent tokens of AI crawlers (training, search and user-triggered fetchers).
- Flags crawlers that are only allowed because nobody named them (the `*` group).
- Catches common mistakes: blocking a retired token, or blocking search engines along with AI crawlers.

## Run it

```bash
bash labs/robots-txt-audit/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
docs-site  AI crawlers allowed  0/11   search: Googlebot no, Bingbot no
           - blocks 'anthropic-ai', a retired token; ClaudeBot is not named
           - search crawlers are blocked from this path too, so it drops out of search results
news-site  AI crawlers allowed  7/11   search: Googlebot yes, Bingbot yes
           - 7 AI crawlers allowed only by default ('*'): OAI-SearchBot, ChatGPT-User, Claude-User, Claude-SearchBot...
           - blocks training (GPTBot, ClaudeBot, CCBot, Google-Extended) while keeping search open
team-site  AI crawlers allowed 11/11   search: Googlebot yes, Bingbot yes
           - 11 AI crawlers allowed only by default ('*'): GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot...
```

## What's in here

| File | Purpose |
|---|---|
| `audit.py` | Crawler list, audit and findings |
| `samples/` | Three example robots.txt files |
| `demo.py` | Audits every sample |
| `tests/` | Allow/block, implicit and retired-token tests |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Sample files | `https://<site>/robots.txt` fetched on a schedule |
| Fixed crawler list | A maintained list of AI user agents (they change often) |
| robots.txt only | Also WAF rules or bot management, since robots.txt is voluntary |
