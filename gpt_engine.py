def gpt_reason(row):

    price = float(row.get("price", 0))
    original = float(row.get("original_price", price))
    drop = float(row.get("drop_pct", 0))
    stock = float(row.get("stock_qty", 0))
    velocity = float(row.get("velocity", 0))

    reasoning = []
    confidence = 50

    # =========================
    # PRICE LOGIC
    # =========================
    if drop >= 50:
        reasoning.append("Extreme discount indicates clearance-level pricing.")
        confidence += 25
    elif drop >= 30:
        reasoning.append("Strong discount suggests promotional or clearance event.")
        confidence += 15
    else:
        reasoning.append("Normal discount range, not a deep clearance.")

    # =========================
    # STOCK LOGIC
    # =========================
    if stock <= 5:
        reasoning.append("Very low stock suggests urgency or end-of-cycle inventory.")
        confidence += 20
    elif stock <= 15:
        reasoning.append("Moderate stock pressure detected.")
        confidence += 10
    else:
        reasoning.append("High stock reduces urgency.")

    # =========================
    # DEMAND LOGIC
    # =========================
    if velocity >= 8:
        reasoning.append("High demand signals strong market interest.")
        confidence += 20
    elif velocity >= 5:
        reasoning.append("Moderate demand trend detected.")
        confidence += 10
    else:
        reasoning.append("Low demand reduces urgency of deal.")

    # =========================
    # VALUE LOGIC
    # =========================
    if original > 0 and price < original * 0.6:
        reasoning.append("Price is below 60% of original value — strong value opportunity.")
        confidence += 15

    # =========================
    # FINAL INTELLIGENCE
    # =========================
    confidence = min(confidence, 100)

    if confidence >= 85:
        verdict = "🔥 ELITE DEAL — ACT FAST"
    elif confidence >= 70:
        verdict = "⚡ STRONG DEAL — WORTH BUYING"
    elif confidence >= 55:
        verdict = "📊 MODERATE DEAL — CONSIDER"
    else:
        verdict = "❌ WEAK DEAL — SKIP"

    return {
        "gpt_score": confidence,
        "verdict": verdict,
        "reasoning": reasoning
    }


def enrich_with_gpt(df):

    df = df.copy()

    scores = []
    verdicts = []
    reasons = []

    for _, row in df.iterrows():
        result = gpt_reason(row)

        scores.append(result["gpt_score"])
        verdicts.append(result["verdict"])
        reasons.append(" | ".join(result["reasoning"]))

    df["gpt_score"] = scores
    df["gpt_verdict"] = verdicts
    df["gpt_reasoning"] = reasons

    return df
