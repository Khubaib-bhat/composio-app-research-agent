import argparse
from agent.researcher import run

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',default='apps.json')
    p.add_argument('--output',default='data/raw_results.json')
    args=p.parse_args()
    run(args.input,args.output)
