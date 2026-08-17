import json, os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from .schema import AppResearch

load_dotenv()
SYSTEM = '''You are an evidence-first product research agent. Research one software app for integration readiness. Prefer official developer docs, official pricing/developer-access pages, and official MCP documentation. Do not infer a credential gate without evidence. If evidence is insufficient, use unknown. Every material claim must have at least one evidence URL. Return JSON matching the schema.'''

def research_app(app: dict) -> dict:
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    prompt = f'''Research this app for an AI-agent toolkit assessment. App: {app['app']}. Category: {app['category']}.

Determine category/one-line description, auth methods, self-serve vs gated credential access, API type and breadth, existing MCP, buildability, blocker, confidence, and evidence URLs. Use web-capable tools available to the configured model if present. Never fabricate URLs or claims. If evidence is missing, say unknown.'''
    r = client.responses.parse(model=os.getenv('MODEL','gpt-5.2'), input=[{'role':'system','content':SYSTEM},{'role':'user','content':prompt}], text_format=AppResearch)
    return r.output_parsed.model_dump()

def run(input_path='apps.json', output_path='data/raw_results.json'):
    apps=json.loads(Path(input_path).read_text())
    results=[]
    for i,app in enumerate(apps,1):
        print(f'[{i}/{len(apps)}] {app["app"]}')
        try: results.append(research_app(app))
        except Exception as e:
            results.append({'app':app['app'],'category':app['category'],'description':'','auth_methods':[],'credential_access':'unknown','api_type':[],'api_breadth':'unknown','existing_mcp':'unknown','buildability':'unknown','blocker':f'research error: {e}','confidence':0,'evidence':[],'notes':'Needs retry'})
    Path(output_path).parent.mkdir(parents=True,exist_ok=True)
    Path(output_path).write_text(json.dumps(results,indent=2))
