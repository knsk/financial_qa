# financial_qa
Financial Q&A with LLM inspired by Grok's question answering capability on recent event.

ref.

https://twitter.com/knsk_exa/status/1785332389847449985

<img width="560" alt="Screenshot 2024-05-01 at 0 41 32" src="https://github.com/knsk/financial_qa/assets/1192029/c5f316f0-05c1-4a54-a555-8d2db848288f">

# Current capability
1) Can summarize and analyze financial results
2) Build strategy based on recent financial results
3) Can speak management policy as CEO based on recent financial results and company's mission statement

# Background
 - **World knowledge is not growing as fast as AI growth**
   - [Will we run out of data? An analysis of the limits of scaling datasets in Machine Learning](https://arxiv.org/abs/2211.04325) [![arXiv](https://img.shields.io/badge/arXiv-2211.04325-a6dba0.svg)](https://arxiv.org/abs/2211.04325)
   - [Annual growth rate for the English Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Size_of_Wikipedia#Annual_growth_rate_for_the_English_Wikipedia)
   - [Number Of Books Published Per Year](https://wordsrated.com/number-of-books-published-per-year-2021/)
 - **LLM's context length is growing with Transformer based architecture improvement and challenges in keeping performance with longer context length**
   - [GPT-4 Turbo and GPT-4 support 128K tokens](https://platform.openai.com/docs/models/gpt-4-turbo-and-gpt-4)
   - [Grok 1.5 supports 128K tokens](https://x.ai/blog/grok-1.5)
   - [Claude 3 supports 200K tokens](https://www.anthropic.com/news/claude-3-family)
   - [Gemni 1.5 Pro support 10M tokens](https://blog.google/technology/ai/google-gemini-next-generation-model-february-2024/#context-window)
   - [Advancing Transformer Architecture in Long-Context Large Language Models: A Comprehensive Survey](https://arxiv.org/abs/2311.12351)  [![arXiv](https://img.shields.io/badge/arXiv-2311.12351-a6dba0.svg)](https://arxiv.org/abs/2311.12351)
   - [RULER: What’s the Real Context Size of Your Long-Context Language Models?](https://arxiv.org/abs/2404.06654) [![arXiv](https://img.shields.io/badge/arXiv-2404.06654-a6dba0.svg)](https://arxiv.org/abs/2404.06654)

# Installation
1) Create venv
```zsh
pyenv exec python -m venv venv
```

2) Source venv
```zsh
source venv/bin/activate
```

3) pip install
```zsh
pip3 install -r requirements.txt
```

4) Install Postgres
```zsh
brew install postgresql
```

5) Start Postgres
```zsh
brew services start postgresql # or pg_ctl stop
```

6) Connect to Postgres
```zsh
psql postgres
```

7) Create User
```sql
CREATE USER kanpo WITH PASSWORD 'kanpo';
```

8) Load data
```zsh
psql -U kanpo -d kanpo_development < data/kanpo_20240501.dump
```

# Data
About the last 10 years (until the end of April 2024) of financial results data posted in [官報](https://kanpou.npb.go.jp/).
 - pg_dump of only articles table 
   - data/kanpo_articles_20240501.dump.xz (1.3MB)
 - pg_dump of all tables including images
   - kanpo_dump_20240501.dump.xz (2.7GB) (to be uploaded somewhere)

# Execution with OpenAI
 - Set API key
```zsh
expprt OPENAI_API_KEY='sk-xxx'
```

1) Overview mode
```zsh
python ask_openai.py --name [company name] --overview
```

2) Analyze mode
```zsh
python ask_openai.py --name [company name] --analyze
```

3) CEO mode
```zsh
python ask_openai.py --name [company name] --ceo --url [company's mission web page url]
```

* Tested with GPT-4 and GPT-4 Turbo
