import re

def normalize_genes(gene_dict, source_gene_list, target_gene_list, abstracts):
    print(f'{len(abstracts)} abstracts to be normalized...')
    for i in range(len(abstracts)):
        source_gene = source_gene_list[i]
        target_gene = target_gene_list[i]
        
        gene_dict_case = list(filter(lambda gene: gene['gene'] == source_gene.lower(), gene_dict))
        if len(gene_dict_case) > 0:
            for s in gene_dict_case[0]['aliases']:
                abstracts[i] = re.sub(re.escape(s), gene_dict_case[0]['gene'], abstracts[i], flags=re.IGNORECASE)
        
        gene_dict_case = list(filter(lambda gene: gene['gene'] == target_gene.lower(), gene_dict))
        if len(gene_dict_case) > 0:
            for s in gene_dict_case[0]['aliases']:
                abstracts[i] = re.sub(re.escape(s), gene_dict_case[0]['gene'], abstracts[i], flags=re.IGNORECASE)
        print(f'{i+1} abstracts normalized...', end = '\r')
    print('\nDone!')
    return(abstracts)

def normalize_dis_genes(gene_dict, dis_dict, source_gene_list, target_dis_list, abstracts):
    print(f'{len(abstracts)} abstracts to be normalized...')
    for i in range(len(abstracts)):
        source_gene = source_gene_list[i]
        target_dis = target_dis_list[i]
        
        gene_dict_case = list(filter(lambda gene: gene['gene'].lower() == source_gene.lower(), gene_dict))
        if len(gene_dict_case) > 0 and isinstance(gene_dict_case[0]['aliases'], list):
            for s in gene_dict_case[0]['aliases']:
                abstracts[i] = re.sub(re.escape(s), gene_dict_case[0]['gene'], abstracts[i], flags=re.IGNORECASE)
        
        dis_dict_case = list(filter(lambda dis: dis['dis'].lower() == target_dis.lower(), dis_dict))
        if len(dis_dict_case) > 0:
            abstracts[i] = re.sub(re.escape(dis_dict_case[0]['dis']), dis_dict_case[0]['aliases'], abstracts[i], flags=re.IGNORECASE)
        print(f'{i+1} abstracts normalized...', end = '\r')
    print('\nDone!')
    return(abstracts)

def normalize_chems_genes(chem_dict, gene_dict, source_chem_list, target_gene_list, abstracts):
    print(f'{len(abstracts)} abstracts to be normalized...')
    for i in range(len(abstracts)):
        source_chem = source_chem_list[i]
        target_gene = target_gene_list[i]
        chem_dict_case = list(filter(lambda chem: chem['chem'].lower() == source_chem.lower(), chem_dict))
        gene_dict_case = list(filter(lambda gene: gene['gene'].lower() == target_gene.lower(), gene_dict))
        if len(chem_dict_case) > 0:
            s = chem_dict_case[0]['syn']
            abstracts[i] = re.sub(re.escape(chem_dict_case[0]['chem']), s, abstracts[i], flags=re.IGNORECASE)
        if len(gene_dict_case) > 0:
            s = gene_dict_case[0]['aliases']
            abstracts[i] = re.sub(re.escape(gene_dict_case[0]['gene']), s, abstracts[i], flags=re.IGNORECASE)
        print(f'{i+1} abstracts normalized...', end = '\r')
    print('\nDone!')
    return(abstracts)