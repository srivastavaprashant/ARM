import pandas as pd
import numpy as np
import re

def generate_word_list(df):
    if_match = lambda x, y: True if x.lower() in y.lower() else False
    df['list_of_words'] = df.sentence.apply(lambda x: [i for i in x.split(' ') if len(i) > 0])
    df['n_words'] = list(df.list_of_words.apply(lambda x: len(x)))
    return(df)


def vocab_generator(list_of_words, lowered = True, VOCAB = {}):
    if lowered == True:
        for word in list_of_words:
            if word.lower() in VOCAB.keys():
                pass
            else: 
                VOCAB[word.lower()] = len(VOCAB)
    else:
        for word in list_of_words:
            if word in VOCAB.keys():
                pass
            else: 
                VOCAB[word] = len(VOCAB)
    print('VOCAB size =', len(VOCAB))
    return(VOCAB)

def generate_typed_encodings(df, maxl, VOCAB, interaction_dict):
    
    def match_ent_in_list(word_list, match_list):        
        if_match = lambda x, y: True if x in y else False
        indexes = []
        for string in match_list:
            for idx, word in enumerate(word_list):
                if if_match(string.lower(), word.lower()):                
                    indexes.append(idx)
                else:
                    pass
        return set(indexes)
    
    def match_int_in_list(word_list, match_list):        
        if_match = lambda x, y: True if x in y else False
        indexes = []
        d = dict.fromkeys([j for i in interaction_dict.values() for j in i], [])
        for string in match_list:
            for idx, word in enumerate(word_list):
                if if_match(string.lower(), word.lower()):
                    d[string] = d[string] + [idx]                    
                else:
                    pass
        return d
    
    df = df[df.n_words < maxl]
    df['tokens'] = df.list_of_words.apply(lambda x: [VOCAB[i.lower()] for i in x])
    df['int_words'] = df.apply(lambda x: match_int_in_list(x.list_of_words, [j for i in interaction_dict.values() for j in i]), axis = 1)
    df['source_words'] = df.apply(lambda x: match_ent_in_list(x.list_of_words, [x.source]), axis = 1)
    df['target_words'] = df.apply(lambda x: match_ent_in_list(x.list_of_words, [x.target]), axis = 1)
    
    def f_int_embd(interaction_dict, interaction, int_words, n_words):
        if interaction in interaction_dict.keys():
            int_keys = interaction_dict[interaction]
            int_key_pos = [int_words[i] for i in int_keys]
            int_key_pos = [j for i in int_key_pos for j in i]
            if sum(int_key_pos) > 0:
                e = [1 if idx in int_key_pos else 0 for idx in range(n_words)]
            else:
                e = [0 for idx in range(n_words)]
        return(e)
    
    df['int_embd'] = df.apply(lambda x: f_int_embd(interaction_dict, x.interaction, x.int_words, x.n_words), axis = 1)    
    df['source_embd'] = df.apply(lambda x: [1 if idx in x.source_words else 0 for idx in range(x.n_words)], axis = 1)
    df['target_embd'] = df.apply(lambda x: [1 if idx in x.target_words else 0 for idx in range(x.n_words)], axis = 1)
    
    df['n_int'] = df.int_embd.apply(lambda x: sum(x))
    df['n_source'] = df.source_embd.apply(lambda x: sum(x))
    df['n_target'] = df.target_embd.apply(lambda x: sum(x))
    df['sing_rel'] = ((df.n_int == 1) & (df.n_source == 1) & (df.n_target == 1))*1
    df['tokens'] = df.apply(lambda x: list(np.pad(x['tokens'], (0, (maxl - x['n_words'])))), axis = 1)
    df['int_embd'] = df.apply(lambda x: list(np.pad(x['int_embd'], (0, (maxl - x['n_words'])))), axis = 1)
    df['source_embd'] = df.apply(lambda x: list(np.pad(x['source_embd'], (0, (maxl - x['n_words'])))), axis = 1)
    df['target_embd'] = df.apply(lambda x: list(np.pad(x['target_embd'], (0, (maxl - x['n_words'])))), axis = 1)
    
    return(df)

def generate_untyped_encodings(df, maxl, VOCAB):
    
    def match_ent_in_list(word_list, match_list):        
        if_match = lambda x, y: True if x in y else False
        indexes = []
        for string in match_list:
            for idx, word in enumerate(word_list):
                if if_match(string.lower(), word.lower()):                
                    indexes.append(idx)
                else:
                    pass
        return set(indexes)
    
    df['tokens'] = df.list_of_words.apply(lambda x: [VOCAB[i.lower()] for i in x])
    df['source_words'] = df.apply(lambda x: match_ent_in_list(x.list_of_words, [x.source]), axis = 1)
    df['target_words'] = df.apply(lambda x: match_ent_in_list(x.list_of_words, [x.target]), axis = 1)
    
    df['source_embd'] = df.apply(lambda x: [1 if idx in x.source_words else 0 for idx in range(x.n_words)], axis = 1)
    df['target_embd'] = df.apply(lambda x: [1 if idx in x.target_words else 0 for idx in range(x.n_words)], axis = 1)
    
    df['n_source'] = df.source_embd.apply(lambda x: sum(x))
    df['n_target'] = df.target_embd.apply(lambda x: sum(x))
    df['sing_rel'] = ((df.n_source == 1) & (df.n_target == 1))*1
    
    df['tokens'] = df.apply(lambda x: list(np.pad(x['tokens'], (0, (maxl - x['n_words'])))), axis = 1)
    df['source_embd'] = df.apply(lambda x: list(np.pad(x['source_embd'], (0, (maxl - x['n_words'])))), axis = 1)
    df['target_embd'] = df.apply(lambda x: list(np.pad(x['target_embd'], (0, (maxl - x['n_words'])))), axis = 1)
    
    return(df)