from Bio import Entrez
import xmltodict
import numpy as np
import re

def download_pubmed_articles(api_key, email, pmid_list):
    Entrez.api_key = api_key
    Entrez.email = email

    pmid_list = set([str(_) for _ in pmid_list if _.isdigit()])
    pmid_search_string = ",".join(list(pmid_list))

    print('No of unique pubmed ids:', len(pmid_list))

    search_results = Entrez.read(Entrez.epost("pubmed", id=pmid_search_string, usehistory="y"))
    webenv=search_results["WebEnv"]
    query_key=search_results["QueryKey"]

    print('Downloading from pubmed db...')
    fetch_handle = Entrez.efetch(db="pubmed", retmode="xml", webenv=search_results["WebEnv"], query_key=search_results["QueryKey"])
    res = fetch_handle.read()
    fetch_handle.close()

    print('Decoding downloaded data...')
    res = res.decode('utf-8')
    res = re.sub('\n', '', res)
    res = re.sub('\t', '', res)

    print('Parsing to a dict...')
    pubmed_data = xmltodict.parse(res)

    print(len(pubmed_data['PubmedArticleSet']['PubmedArticle']), 'pubmed matches found out of', len(pmid_list),'pubmed articles.')

    pubmed_articles = [i['MedlineCitation'] for i in pubmed_data['PubmedArticleSet']['PubmedArticle']]
    print('Extracting abstracts and titles...')
    pubmed_data_res = []


    for j, i in enumerate(pubmed_articles):
        if isinstance(i['PMID'], dict):
            pmid =  i['PMID']['#text']
        else:
            pmid = i['PMID']
        if 'ArticleTitle' in i['Article'].keys():
            if isinstance(i['Article']['ArticleTitle'], dict):
                title = i['Article']['ArticleTitle']['#text']
            else:
                title = i['Article']['ArticleTitle']
        else:
            title = np.nan
        if 'Abstract' in i['Article'].keys():
            if isinstance(i['Article']['Abstract']['AbstractText'], list):
                _ = []
                for k in i['Article']['Abstract']['AbstractText']:
                    if isinstance(k, dict):
                        if '#text' in k.keys():
                            _.append(k['#text'])    
                    else:    
                        _.append(k)
                abstract = ' '.join(_)
            elif isinstance(i['Article']['Abstract']['AbstractText'], dict):
                abstract = i['Article']['Abstract']['AbstractText']['#text']
            else:
                abstract = i['Article']['Abstract']['AbstractText']
        else:
            abstract = np.nan
        d = {'pubmed': pmid, 'title': title, 'abstract': abstract}
        pubmed_data_res.append(d)
    print('Done!')
    return(pubmed_data_res)

def search_gene_id(api_key, email, gene_list):
    Entrez.api_key = api_key
    Entrez.email = email
    gene_list = set(gene_list)
    print(len(gene_list), 'unique gene names...')
    print('Searching...')
    genes = []
    for j, name in enumerate(gene_list):
        handle = Entrez.esearch(db="gene", retmax=10, term=str(name), sort = 'relevance')
        record = Entrez.read(handle)
        if len(record['IdList']) > 0:
            d = {'gene': name, 'id':record['IdList'][0]}
            genes.append(d)
        else:
            #d = {'gene': name, 'id':np.nan}
            pass
        print(f'{len(genes)} found out of {j+1} genes...', end = '\r')    
    return(genes)

def search_chem_id(api_key, email, chem_list):
    Entrez.api_key = api_key
    Entrez.email = email
    chem_list = list(set(chem_list))
    print(f'{len(chem_list)} unique chemical names.')
    chems = []
    print('Searching...')
    for i, chem in enumerate(chem_list):
        handle = Entrez.esearch(db="pccompound", retmax=10, term=str(chem), sort = 'relevance')
        record = Entrez.read(handle)
        if len(record['IdList']) > 0:
            d = {'chem': chem, 'id':record['IdList'][0]}
            chems.append(d)
        else:
            pass
        print(f'{len(chems)} chemicals found out of {i+1}', end = '\r')
    return chems

def download_chem_names(api_key, email, chem_ids):
    Entrez.email = email
    Entrez.api_key = api_key
    
    chem_ids = set([str(_) for _ in chem_ids if _.isdigit()])
    
    print('No of unique gene ids:', len(chem_ids))
    chem_search_string = ",".join(list(chem_ids))

    search_results = Entrez.read(Entrez.epost("pccompound", id=chem_search_string, usehistory="y"))
    webenv=search_results["WebEnv"]
    query_key=search_results["QueryKey"]
    
    print('Downloading from gene db...')
    fetch_handle = Entrez.esummary(db="pccompound", retmode="txt", webenv=search_results["WebEnv"], query_key=search_results["QueryKey"])
    data = fetch_handle.read()
    fetch_handle.close()
    
    print('Decoding downloaded data...')
    data = data.decode('utf-8')
    sub_data = re.sub('\n', '', data)
    sub_data = re.sub('\t', '', sub_data)

    print('Parsing to a dict')
    chem_data = xmltodict.parse(sub_data)
    chem_data = chem_data['eSummaryResult']['DocSum']
    
    chem_dict = []
    for i in chem_data:
        if i['Item'][5]['@Name'] == 'SynonymList' and 'Item' in i['Item'][5].keys():
            if isinstance(i['Item'][5]['Item'], list):
                synonyms = [j['#text'] for j in i['Item'][5]['Item']]
            else:
                synonyms = i['Item'][5]['Item']['#text']
                chem_name = np.nan
            for n in synonyms:
                regexp = re.compile('\W')
                if not regexp.search(n):
                    chem_name = n
                    break
            d = {'chem': chem_name.lower(), 'id':i['Id'], 'syn': synonyms}
            chem_dict.append(d)
        else:
            pass
    print(f'{len(chem_dict)} found.')
    return(chem_dict)

def download_gene_names(api_key, email, gene_ids):
    Entrez.email = email
    Entrez.api_key = api_key
    
    gene_ids = set([str(_) for _ in gene_ids if _.isdigit()])
    gene_search_string = ",".join(list(gene_ids))

    print('No of unique gene ids:', len(gene_ids))

    search_results = Entrez.read(Entrez.epost("gene", id=gene_search_string, usehistory="y"))
    webenv=search_results["WebEnv"]
    query_key=search_results["QueryKey"]
    
    print('Downloading from gene db...')
    fetch_handle = Entrez.esummary(db="gene", retmode="txt", webenv=search_results["WebEnv"], query_key=search_results["QueryKey"])
    data = fetch_handle.read()
    fetch_handle.close()
    
    print('Decoding downloaded data...')
    data = data.decode('utf-8')
    sub_data = re.sub('\n', '', data)
    sub_data = re.sub('\t', '', sub_data)

    print('Parsing to a dict')
    gene_data = xmltodict.parse(sub_data)
    gene_data = gene_data['eSummaryResult']['DocumentSummarySet']['DocumentSummary']
    
    gene_dict = []
    for j, i in enumerate(gene_data):
        oa = i['OtherAliases'].split(', ') if i['OtherAliases'] else []
        od = i['OtherDesignations'].split('|') if i['OtherDesignations'] else []
        aliases = oa + od
        aliases = [i for i in aliases if len(i)>2]
        if len(aliases) > 0:
            d = {'gene':i['Name'].lower(), 'id':i['@uid'], 'aliases':aliases}
            gene_dict.append(d)

    print(f'{len(gene_dict)} found.')
    return(gene_dict)