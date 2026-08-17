"""Verification helpers.

The verifier deliberately does not invent corrections. It flags records for review when
there is missing evidence, low confidence, or contradictory/ambiguous classifications.
"""
import json
from pathlib import Path

def flag_rows(input_path='data/raw_results.json', output_path='data/verification_queue.json', sample_size=15):
    rows=json.loads(Path(input_path).read_text())
    flagged=[]
    for r in rows:
        reasons=[]
        if r.get('confidence',0)<0.8: reasons.append('low confidence')
        if not r.get('evidence'): reasons.append('no evidence')
        if r.get('credential_access')=='unknown': reasons.append('credential access unknown')
        if r.get('existing_mcp')=='unknown': reasons.append('MCP status unknown')
        if reasons: flagged.append({'app':r['app'],'reasons':reasons})
    # deterministic human sample for auditability
    sample=[{'app':r['app'],'reason':'human spot-check sample'} for r in rows[:sample_size]]
    out={'flagged':flagged,'human_sample':sample}
    Path(output_path).parent.mkdir(parents=True,exist_ok=True)
    Path(output_path).write_text(json.dumps(out,indent=2))
    return out
