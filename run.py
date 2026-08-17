import argparse
from agent.researcher import run
from agent.verifier import flag_rows

if __name__ == '__main__':
    p=argparse.ArgumentParser(description='Run the evidence-first app research pipeline.')
    p.add_argument('--input',default='apps.json')
    p.add_argument('--output',default='data/raw_results.json')
    p.add_argument('--verify',action='store_true',help='Create a verification queue after research')
    args=p.parse_args()
    run(args.input,args.output)
    if args.verify:
        flag_rows(args.output)
