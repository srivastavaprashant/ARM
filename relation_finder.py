import pandas as pd
import re

def find_sentences(df):
    if_match = lambda x, y: True if x.lower() in y.lower() else False
    no_of_ints = df.shape[0]
    print(f'{len(df)} abstracts...')
    df['list_of_lines'] = df.abstract.str.split('.')
    df['n_lines'] = df['list_of_lines'].apply(lambda x: len(str(x)))
    df = df.explode('list_of_lines')
    df = df.rename(columns = {'list_of_lines':'sentence'})
    df = df[df.sentence != ''].dropna()
    print(f'{len(df)} sentences found...')
    df.sentence = df.sentence.apply(lambda x: re.sub("'", '', re.sub("`", '', re.sub('-', '', re.sub('\(', '', re.sub('\)', '', re.sub('/', ' ', re.sub(',', '', re.sub(';', '', re.sub(':', ' ', str(x)))))))))))
    df.source = df.source.apply(lambda x: re.sub("'", '', re.sub("`", '', re.sub('-', '', re.sub('\(', '', re.sub('\)', '', re.sub('/', ' ', re.sub(',', '', re.sub(';', '', re.sub(':', ' ', str(x)))))))))))
    df.target = df.target.apply(lambda x: re.sub("'", '', re.sub("`", '', re.sub('-', '', re.sub('\(', '', re.sub('\)', '', re.sub('/', ' ', re.sub(',', '', re.sub(';', '', re.sub(':', ' ', str(x)))))))))))
    df['match'] = df.apply(lambda x: if_match(x['source'], x['sentence'])*if_match(x['target'], x['sentence']), axis = 1)
    df = df.drop_duplicates(subset = ['source', 'target', 'sentence'])    
    print(f'{df.match.sum()} sentences have a relation information.')
    return(df)