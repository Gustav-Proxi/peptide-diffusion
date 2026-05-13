"""
Fix the InstaNovo scoring bug: rs.decode() returns a list, which str() turns into
"['G','F','E',...]". The _clean() function's [..] stripper then wipes it to "".

Fix: parse the list repr with ast.literal_eval, join to plain string, then clean.
"""

import ast
import json
import re

import pandas as pd

df = pd.read_csv("eval/instanovo_472_split.csv")


def clean(seq: str) -> str:
    s = str(seq)
    try:
        parsed = ast.literal_eval(s)
        if isinstance(parsed, list):
            s = "".join(str(x) for x in parsed)
    except (ValueError, SyntaxError):
        pass
    s = re.sub(r"\[.*?\]|\(.*?\)", "", s)
    return re.sub(r"[^A-Z]", "", s.upper())


def aa_recall(pred: str, true: str) -> float:
    if not true:
        return 0.0
    return sum(p == t for p, t in zip(pred, true)) / max(len(true), 1)


df["true_clean"] = df["true_sequence"].apply(clean)
df["pred_clean"] = df["predicted_sequence"].apply(clean)
df["aa_recall"] = df.apply(
    lambda r: aa_recall(r["pred_clean"], r["true_clean"]), axis=1
)
df["pep_correct"] = (df["pred_clean"] == df["true_clean"]).astype(int)

aa = df["aa_recall"].mean() * 100
pep = df["pep_correct"].mean() * 100

print(f"InstaNovo v1.2.0  |  472-spectrum E. coli EV test split")
print(f"  AA Recall  : {aa:.2f}%")
print(f"  Pep Acc    : {pep:.2f}%")
print(f"  n spectra  : {len(df)}")

# Sample comparison
print("\nSample predictions (first 5):")
for _, row in df.head(5).iterrows():
    match = "✓" if row["pep_correct"] else "✗"
    print(
        f"  {match} true={row['true_clean']:25s}  pred={row['pred_clean']:25s}  aa={row['aa_recall']:.2f}"
    )

df.to_csv("eval/instanovo_472_split.csv", index=False)

summary = {
    "model": "instanovo-v1.2.0",
    "test_set": "ecoli_ev_472",
    "n_spectra": len(df),
    "aa_recall_pct": round(aa, 2),
    "pep_acc_pct": round(pep, 2),
}
with open("eval/instanovo_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\nSaved → eval/instanovo_472_split.csv")
print(f"Saved → eval/instanovo_summary.json")
