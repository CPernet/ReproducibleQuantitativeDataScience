def top_doc(df, doc_col, score_col, m):
    """
    Get top m most relevant docs 
    based on some relevance scores.
    
    Args:
        df = pandas.DataFrame object that contains the documents and their respective relevance scores
        doc_col (str) = Name of DataFrame column that contains text
        score_col (str) = Name of DataFrame column that contains score
        m (int) = Number of top docs to get. To retrieve all, put m=-1
    
    Returns:
        top_docs: returns top m documents with the highest relevance scores
    """
    #Sort score
    sorted_score = df[score_col].sort_values(ascending=False)

    #Get top m scores
    top_sorted_score = sorted_score.head(m)

    #Get index of top m scores
    doc_idx = top_sorted_score.index

    #Get top m documents based on the scores
    top_docs = df.loc[doc_idx, doc_col]
    
    #Return top m documents based on relevance scores
    return top_docs

#source: https://github.com/theresiavr/Query-Expansion/blob/master/prf.py
