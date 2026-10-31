"""
Use Jev to screen candidate information sources for Jev technical research and usage collection.
"""

import json
from jev_client import JevClient, Choice, Score, Noul

API_KEY = "apikey_2998e6693e0329444758839b8e9f443cf4e_b83254734358781cd5052308f8a0426736d50140c91fe368289899f68461840e"
client = JevClient(api_key=API_KEY)

# Candidate information sources to screen
candidates = [
    {
        "name": "X (Twitter) - Developers, AI Researchers & Tech Twitter",
        "description": "Real-time discussions from AI researchers (Diogo Almeida, OpenAI alumni, AI engineers), product launches, release reactions, and code snippets.",
        "mandatory": True
    },
    {
        "name": "GitHub (Repos, PRs, Issues, Discussion boards)",
        "description": "Open-source implementations, SDKs, agent frameworks (LangChain, LlamaIndex, Semantic Router) integrating Jev, wrapper libraries, and benchmark code.",
        "mandatory": False
    },
    {
        "name": "arXiv.org & OpenReview (Preprint Papers & Conference Proceedings)",
        "description": "Academic papers on RLCD, non-autoregressive decision models, expected calibration error (ECE), and System One reasoning theory.",
        "mandatory": False
    },
    {
        "name": "Hacker News (Y Combinator)",
        "description": "In-depth engineering discussions, architecture critiques, performance benchmarks, and alternative perspectives on TypeSafe AI launches.",
        "mandatory": False
    },
    {
        "name": "Reddit (r/MachineLearning, r/LocalLLaMA, r/Artificial)",
        "description": "Community tests, hands-on developer experiences, latency comparisons, cost breakdowns, and engineering pain points.",
        "mandatory": False
    },
    {
        "name": "TypeSafe AI Official Documentation, SDK Repos & Discord",
        "description": "First-party API references, schema specs, release notes for jev-1.14.0, official example cookbooks, and core developer support.",
        "mandatory": False
    },
    {
        "name": "Substack & AI Engineering Blogs (Latent Space, Interconnects, Swyx)",
        "description": "Deep-dive technical essays, founder interviews with Diogo Almeida, architectural breakdowns of System One vs System Two.",
        "mandatory": False
    },
    {
        "name": "Towards Data Science & Medium AI Publications",
        "description": "Hands-on implementation tutorials, code walk-throughs, comparative evaluations with BERT/LLM fine-tuning.",
        "mandatory": False
    },
    {
        "name": "AI Engineer World's Fair / Conference Talks & Transcripts",
        "description": "Recorded presentations, slide decks, and transcripts from conference keynotes about production agent runtimes and calibrated decisions.",
        "mandatory": False
    },
    {
        "name": "Lobste.rs (Tech Computing Community)",
        "description": "Systems programming, latency-focused architecture discussions, compiler and ML inference engineering threads.",
        "mandatory": False
    },
    {
        "name": "Product Hunt & Launch Directories",
        "description": "Product launch reviews, user feedback, initial ecosystem toolings and startup integrations.",
        "mandatory": False
    },
    {
        "name": "Stack Overflow & Developer Q&A",
        "description": "Implementation troubleshooting, error handling, JSON schema validation questions.",
        "mandatory": False
    }
]

questions = {
    "value_score": Score(
        instructions="Rate the information density and research value of this source for uncovering cutting-edge Jev applications and technical mechanisms.",
        criteria=[
            "Low value: Sparse or mostly noise/marketing",
            "Moderate value: Good secondary tutorials and general chatter",
            "High value: Direct primary source of technical architecture or active practitioner code"
        ]
    ),
    "primary_category": Choice(
        instructions="What is the primary technical value type provided by this source?",
        criteria={
            "first_party_spec": "Official specs, core docs, API standards",
            "practitioner_usage": "Real-world engineering use cases, production patterns, war stories",
            "academic_theory": "Theoretical models, algorithms, RLCD math, formal benchmarks",
            "realtime_pulse": "Breaking discussions, founder insights, ecosystem velocity"
        }
    ),
    "include_in_top10": Noul(
        instructions="Should this source be included in the top 10 prioritized research sources?"
    )
}

print("Invoking Jev to evaluate and screen information sources...")
evaluated_sources = []

for item in candidates:
    state = f"Source Name: {item['name']}\nDescription: {item['description']}\nMandatory Requirement: {item['mandatory']}"
    res = client.decide(state, questions)
    answers = res["answers"]
    
    score_val = answers["value_score"]["score"]
    category = answers["primary_category"]["choice"]
    include_prob = answers["include_in_top10"]["noul"]
    
    # If mandatory, boost ranking priority
    rank_metric = score_val + (10.0 if item["mandatory"] else 0.0) + include_prob
    
    evaluated_sources.append({
        "name": item["name"],
        "description": item["description"],
        "mandatory": item["mandatory"],
        "score": score_val,
        "category": category,
        "include_prob": include_prob,
        "rank_metric": rank_metric,
        "raw_answers": answers
    })

# Sort by rank_metric descending
evaluated_sources.sort(key=lambda x: x["rank_metric"], reverse=True)
top_10 = evaluated_sources[:10]

print("\n--- JEV Screening Results (Top 10 Selected Sources) ---")
for i, s in enumerate(top_10, 1):
    print(f"{i}. [{s['category']}] {s['name']} (Score: {s['score']:.2f}, Incl Prob: {s['include_prob']:.2f}{', MANDATORY' if s['mandatory'] else ''})")

with open("/Users/happy/Desktop/jev 调研/jev_screened_top10_sources.json", "w", encoding="utf-8") as f:
    json.dump(top_10, f, ensure_ascii=False, indent=2)

print("\nSaved top 10 sources to jev_screened_top10_sources.json")
