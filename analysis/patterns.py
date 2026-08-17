import argparse, json
from collections import Counter, defaultdict
from pathlib import Path

p=argparse.ArgumentParser(); p.add_argument('--input',default='data/verified_results.json'); p.add_argument('--output',default='data/patterns.json'); a=p.parse_args()
rows=json.loads(Path(a.input).read_text())
summary={'total':len(rows),'auth_methods':Counter(x for r in rows for x in r.get('auth_methods',[])),'credential_access':Counter(r.get('credential_access','unknown') for r in rows),'buildability':Counter(r.get('buildability','unknown') for r in rows),'mcp':Counter(r.get('existing_mcp','unknown') for r in rows),'categories':defaultdict(lambda:Counter())}
for r in rows:
 c=summary['categories'][r.get('category','Unknown')]; c['total']+=1; c[r.get('credential_access','unknown')]+=1; c[r.get('buildability','unknown')]+=1
summary={k:(dict(v) if isinstance(v,Counter) else {kk:dict(vv) for kk,vv in v.items()} if isinstance(v,defaultdict) else v) for k,v in summary.items()}
Path(a.output).write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
