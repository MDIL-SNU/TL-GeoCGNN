import pandas as pd
import argparse
from tqdm import tqdm
from pymatgen.ext.matproj import MPRester


def get_atomization_energy(entries: list, api_key: str):
    
    at_en_dict = {}

    with MPRester(api_key) as mpr:
        if mpr is None:
            print('Check your API key please.')
            return

        else:
            for mp_id in tqdm(entries):
                try:
                    at_en_dict[mp_id] = mpr.get_cohesive_energy(mp_id, True)
                except:
                    print(f'Warning: Atomization energy invalid for {mp_id}')

    return at_en_dict


def main():
    parser = argparse.ArgumentParser(description="Updating atomization energy")

    parser.add_argument("--id", type=str, default=[], nargs='*',
        help='Materials Project ID for update')
    parser.add_argument("--all", action='store_true',
        help='Update every IDs')
    parser.add_argument("--api_key", type=str, required=True,
        help='API key for Materials Project. Check https://legacy.materialsproject.org/dashboard')

    config = vars(parser.parse_args())

    if len(config['id']) == 0  and not config['all']:
        print('Nothing to be updated')

    else:
        df = pd.read_csv('targets_atomization.csv')

        entries = list(df['id']) if config['all'] else config['id']
        
        at_en_dict = get_atomization_energy(entries, config['api_key'])

        if at_en_dict is not None:
            update_df = pd.DataFrame(list(at_en_dict.items()), columns=['id', 'cohesive'])
            df = pd.merge(df, update_df, on='id', how='left', suffixes=('_existing', '_new'))
            df['cohesive'] = df['cohesive_new'].combine_first(df['cohesive_existing'])
            df = df[['id', 'cohesive']]
            df = pd.concat([df, update_df[~update_df['id'].isin(df['id'])]], ignore_index=True)
            
            df.to_csv('targets_atomization_updated.csv', index=False)

if __name__=="__main__":
    main()
