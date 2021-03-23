from scipy.cluster.hierarchy import linkage, dendrogram


def hClust_euclidean(genome_df):
    linkage_matrix = linkage(genome_df, method='average', metric='euclidean')
    names = genome_df.index.tolist()
    clust = dendrogram(linkage_matrix, no_plot=True, labels=names, get_leaves=True)
    return genome_df.reindex(list(clust['ivl']))
