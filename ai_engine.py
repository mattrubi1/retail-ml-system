import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_deal(row):

    prompt = f"""
You are a retail deal intelligence system.

Return ONLY valid JSON.

Product:
- Name: {row.get('item_name')}
- Price: {row.get('price')}
- Original Price: {row.get('original_price')}
- Discount %: {row.get('drop_pct')}
- Stock: {row.get('stock_qty')}
- Velocity: {row.get('velocity')}
- Store: {row.get('store_name')}

JSON format:
{{
  "score": 0-100,
  "verdict": "ELITE | STRONG | MODERATE | WEAK | SKIP",
  "reasoning": "short explanation",
  "tags": ["clearance", "overstock", "high_demand", "low_stock"]
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You return only JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        return {
            "score": 0,
            "verdict": "ERROR",
            "reasoning": str(e),
            "tags": []
        }


def enrich_with_gpt(df):

    df = df.copy()

    scores = []
    verdicts = []
    reasons = []
    tags = []

    for _, row in df.iterrows():
        result = analyze_deal(row)

        scores.append(result.get("score", 0))
        verdicts.append(result.get("verdict", "UNKNOWN"))
        reasons.append(result.get("reasoning", ""))
        tags.append(",".join(result.get("tags", [])))

    df["gpt_score"] = scores
    df["gpt_verdict"] = verdicts
    df["gpt_reasoning"] = reasons
    df["gpt_tags"] = tags

    return df
