""" script to read the predictions of bertsumextract and create the data for matchsum"""

import json
import argparse
import pathlib
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', help='')
    parser.add_argument('--prefix', default='_step3000')
    parser.add_argument('--original-dir')
    parser.add_argument('--output', help='')
    parser.add_argument('--sent_ids_file', help='')
    parser.add_argument('--max_sents', default=7, type=int)
    args = parser.parse_args()

    pathlib.Path(args.output).mkdir(parents=True, exist_ok=True)


    for ds in ['test']:
        fpath = args.input_dir + f'/{ds}{args.prefix}'
        ids_file = fpath + '.ids'
        cand_file = fpath + '.candidate'
        score_file = fpath + '.scores'
        gold_file = fpath + '.gold'

        orig_file = f'{args.original_dir}/{ds}-multitarget.jsonl' if ds != 'train' else f'{args.original_dir}/train.jsonl'
        with open(orig_file) as fin:
            orig = [json.loads(e) for e in fin]

        output_file = args.output + f'/{ds}-raw.jsonl'
        output_ids_file = args.output + f'/{ds}-ids.jsonl'

        with open(ids_file) as f1, open(cand_file) as f2, open(score_file) as f3, open(gold_file) as f4, open(output_file, 'w') as f5, open(output_ids_file, 'w') as f6:
            ids = [e.strip() for e in f1]
            cands_raw = [e.strip() for e in f2]
            cands = [e.split('<q>') for e in cands_raw]
            scores = [json.loads(line) for line in f3]
            gold = [line.strip() for line in f4]
            all_data = {}
            all_sent_ids = {}
            for _id, _cand, _score, _gold in zip(ids, cands, scores, gold):
                obj = {
                    'text': _cand,
                    'summary': [_gold],
                    'summary_id': _id,
                }
                idx = np.argsort(_score)[::-1].tolist()[:args.max_sents]
                if len(_score) != len(_cand):
                    import ipdb; ipdb.set_trace()
                all_data[_id] = obj
                all_sent_ids[_id] = {"sent_id": [e for e in idx]}

            for e in orig:
                try:
                    obj = all_data[e['paper_id']]
                except KeyError:
                    import ipdb; ipdb.set_trace()
                assert all_data[e['paper_id']]['summary_id'] == e['paper_id']
                # if len(obj['text']) != len(e['source']):
                #     import ipdb; ipdb.set_trace()
                # obj['text'] = e['source']
                sent_ids = all_sent_ids[e['paper_id']]
                f5.write(f"{json.dumps(obj)}\n")
                f6.write(f"{json.dumps(sent_ids)}\n")
            
        

if __name__ == '__main__':
    main()
