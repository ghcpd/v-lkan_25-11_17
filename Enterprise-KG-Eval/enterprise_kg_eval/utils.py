def summarize_counts(entities, relations):
    return {
        'entities': sum(len(d['entities']) for d in entities),
        'relations': sum(len(d['relations']) for d in relations),
    }
