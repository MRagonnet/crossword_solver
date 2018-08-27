import gensim
import os

model_path = os.path.join("model","GoogleNews-vectors-negative300.bin")
# Load Google's pre-trained Word2Vec model.
model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)  