'''
this file contains the parameters to do all the graph based tasks

1) reading teamsvecs pickle data
2) creating graph data
3) loading graph data
4) generating embeddings

'''

settings = {
    'model':{
            'gnn':{},
            'gcn':{},
            'gan':{},
            'gin':{},
            'node2vec':{},
            'metapath2vec':{
                'STE' : {},
                'SE' : {},
                'STE_TL' : {},
                'STEL' : {}
            }
        },
    'data':{
        'domain': {
            'dblp':{
                'toy.dblp.v12.json':{},
            },
            'uspt':{
                'toy.patent.tsv':{},
            },
            'imdb':{
                'toy.title.basics.tsv':{},
            },
        },
    },
    'storage':{
        'base_folder' : {
            '../../data/graph/' : {},
        },
        'output_type': {
            'raw' : {},
            'preprocessed' : {}
        },
    },

}