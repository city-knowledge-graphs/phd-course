# Load back with memory-mapping = read-only, shared across processes.
from gensim.models import KeyedVectors


model = KeyedVectors.load("data/pizza.embeddings", mmap='r')
wv = model.wv


vector = wv['pizza']  # Get numpy vector of a word
print(vector)


#cosine similarity
similarity = wv.similarity('pizza', 'http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza')
print(similarity)

similarity = wv.similarity('http://www.co-ode.org/ontologies/pizza/pizza.owl#Margherita', 'margherita')
print(similarity)





#Most similar cosine similarity
result = wv.most_similar(positive=['margherita', 'pizza'])
print(result)

#Most similar entities: cosmul
result = wv.most_similar_cosmul(positive=['margherita'])
print(result)