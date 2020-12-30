class jaccard():
    def urut(tokens):
        result = [x.lower().strip(',').strip('.') for x in tokens.split()]
        result.sort()
        return result

    def compute_jaccard_similarity_score(x, y):
        intersection_cardinality = len(set(x).intersection(set(y)))
        union_cardinality = len(set(x).union(set(y)))

        return intersection_cardinality / float(union_cardinality)
