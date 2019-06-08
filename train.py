import os

from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.embeddings import TokenEmbeddings, WordEmbeddings, CharacterEmbeddings, StackedEmbeddings

from typing import List

# define columns
columns = {0: 'text', 1: 'token_type', 2: 'exact_token_type', 3: 'type_hint'}

# this is the folder in which train, test and dev files reside
ROOT_FOLDER = 'data'

# retrieve corpus using column format, data folder and the names of the train, dev and test files
# 1. create the corpus
corpus: Corpus = ColumnCorpus(ROOT_FOLDER,
                              columns,
                              train_file='train.txt',
                              test_file='test.txt',
                              dev_file='dev.txt')
print(corpus)

# remove empty sentences
# print(type(corpus.train))
# corpus.train = [sentence for sentence in corpus.train if len(sentence) > 0]
# corpus.test = [sentence for sentence in corpus.test if len(sentence) > 0]
# corpus.dev = [sentence for sentence in corpus.dev if len(sentence) > 0]
# print(corpus)

# 2. what tag do we want to predict?
tag_type = 'type_hint'

# 3. make the tag dictionary from the corpus
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
# print(tag_dictionary.idx2item)

# 4. initialize embeddings
embedding_types: List[TokenEmbeddings] = [

    WordEmbeddings('glove'),

    # comment in this line to use character embeddings
    CharacterEmbeddings(tag_dictionary),

    # comment in these lines to use flair embeddings
    # FlairEmbeddings('news-forward'),
    # FlairEmbeddings('news-backward'),
]
embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

# 5. initialize sequence tagger
from flair.models import SequenceTagger

tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                        embeddings=embeddings,
                                        tag_dictionary=tag_dictionary,
                                        tag_type=tag_type,
                                        use_crf=True)

# 6. initialize trainer
from flair.trainers import ModelTrainer

trainer: ModelTrainer = ModelTrainer(tagger, corpus)

# 7. start training
trainer.train('resources/taggers/language_model',
              learning_rate=0.1,
              mini_batch_size=16,
              max_epochs=5)