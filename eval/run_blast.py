"""
Fix 3: BLASTp the 6 wastewater FDR peptides against NCBI nr.

Produces eval/blast_results.csv with columns:
  sequence, top_hit_accession, top_hit_description, top_hit_organism,
  identity_pct, e_value, bit_score, query_coverage_pct

Usage:
  cd peptide-diffusion
  python eval/run_blast.py
"""

import json
import os
import time
from io import StringIO

import pandas as pd

try:
    from Bio import SeqIO
    from Bio.Blast import NCBIWWW, NCBIXML
except ImportError:
    raise ImportError("Install biopython: pip install biopython")

# 6 sequences from Table 4 of the report (wastewater 5% FDR peptides)
WASTEWATER_SEQS = [
    "FNDVIPMGEQAINTNEGAYR",
    "NNGNAIGVDLAAIPFVAGDR",
    "GSNYNEVVTLADVTIVQGIR",
    "DLDVEFTALDGASVQVIAYR",
    "ALDNAIDGGQYSFLEVAINR",
    "QLDNNCVYLGATAGVPIAK",
]

out_csv = os.path.join(os.path.dirname(__file__), "blast_results.csv")
cache_dir = os.path.join(os.path.dirname(__file__), "blast_cache")
os.makedirs(cache_dir, exist_ok=True)


def blast_sequence(seq: str) -> dict:
    cache_path = os.path.join(cache_dir, f"{seq}.xml")

    if os.path.exists(cache_path):
        print(f"  [cache] {seq}")
        with open(cache_path) as fh:
            xml_str = fh.read()
    else:
        print(f"  [BLAST] {seq} — querying NCBI (this takes ~30-90s per sequence)...")
        result_handle = NCBIWWW.qblast(
            "blastp",
            "nr",
            seq,
            hitlist_size=5,
            expect=10,
            matrix_name="BLOSUM62",
        )
        xml_str = result_handle.read()
        result_handle.close()
        with open(cache_path, "w") as fh:
            fh.write(xml_str)
        time.sleep(3)  # be polite to NCBI

    blast_records = list(NCBIXML.parse(StringIO(xml_str)))
    if not blast_records or not blast_records[0].alignments:
        return {
            "sequence": seq,
            "top_hit_accession": "NO HIT",
            "top_hit_description": "",
            "top_hit_organism": "",
            "identity_pct": 0.0,
            "e_value": 999.0,
            "bit_score": 0.0,
            "query_coverage_pct": 0.0,
        }

    record = blast_records[0]
    aln = record.alignments[0]
    hsp = aln.hsps[0]

    identity_pct = 100.0 * hsp.identities / hsp.align_length
    query_cov = 100.0 * (hsp.query_end - hsp.query_start + 1) / len(seq)

    # Extract organism from title (format: "description [Organism name]")
    title = aln.title
    import re

    org_match = re.search(r"\[([^\[\]]+)\]\s*$", title)
    organism = org_match.group(1) if org_match else ""
    # Strip organism from description
    description = re.sub(r"\s*\[[^\[\]]+\]\s*$", "", title).strip()
    # Trim very long descriptions
    if len(description) > 100:
        description = description[:97] + "..."

    return {
        "sequence": seq,
        "top_hit_accession": aln.accession,
        "top_hit_description": description,
        "top_hit_organism": organism,
        "identity_pct": round(identity_pct, 1),
        "e_value": hsp.expect,
        "bit_score": round(hsp.bits, 1),
        "query_coverage_pct": round(query_cov, 1),
    }


print("Running BLASTp for 6 wastewater peptides against NCBI nr...\n")
rows = []
for seq in WASTEWATER_SEQS:
    row = blast_sequence(seq)
    rows.append(row)
    print(
        f"    {seq[:20]:22s} → {row['top_hit_organism'][:35]:37s} "
        f"id={row['identity_pct']:.0f}% e={row['e_value']:.2e}"
    )

df = pd.DataFrame(rows)
df.to_csv(out_csv, index=False)
print(f"\nSaved → {out_csv}")
print(
    df[["sequence", "top_hit_organism", "identity_pct", "e_value"]].to_string(
        index=False
    )
)
