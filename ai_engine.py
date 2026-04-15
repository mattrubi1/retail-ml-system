import pandas as pd


def analyze_deal(row):

    score = 0
    reasons = []

    # -------------------------
    # DISCOUNT SIGNAL
    # -------------------------
    if row.get("drop_pct", 0) >= 40:
        score += 40
        reasons.append("🔥 Heavy discount (40%+)")
    elif row.get("drop_pct", 0) >= 25:
        score += 25
        reasons.append("📉 Strong discount")

    # -------------------------
    # STOCK PRESSURE
    # -------------------------
    if row.get("stock_qty", 0) <= 5:
        score += 30
        reasons.append("⚠️ Very low stock (scarcity)")
    elif row.get("stock_qty", 0) <= 15:
        score += 15
        reasons.append("📦 Moderate stock pressure")

    # -------------------------
    # DEMAND SIGNAL
    # -------------------------
    if row.get("velocity", 0) >= 8:
        score += 25
        reasons.append("🚀 High demand item")
    elif row.get("velocity", 0) >= 5:
        score += 15
        reasons.append("📊 Moderate demand")

    # -------------------------
    # VALUE SIGNAL
    # -------------------------
    price = row.get("price", 0)
    original = row.get("original_price", price)

    if original > 0 and price < original * 0.6:
        score += 25
        reasons.append("💰 Below 60% of original price")

    return {
        "ai_score": min(score, 100),
        "reasons": reasons
    }


def enrich_dataframe(df):

    df = df.copy()

    ai_scores = []
    ai_reasons = []

    for _, row in df.iterrows():
        result = analyze_deal(row)
        ai_scores.append(result["ai_score"])
        ai_reasons.append(" | ".join(result["reasons"]))

    df["ai_score"] = ai_scores
    df["ai_reasons"] = ai_reasons

    return df
