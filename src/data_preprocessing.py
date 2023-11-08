import json
import nltk
nltk.download('punkt')
import re
from sklearn.feature_extraction.text import CountVectorizer
from joblib import load
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
# import matplotlib.pyplot as plt


nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))

def tokenize(text):
    wordstoremove = ['Thomas', 'thing', 'quite', 'exist', 'live', 'things', 'you\'re', 'we\'ll', 'really', 'right',
                     'said', 'right', 'refresh', 'realized', 'realize', 'wrong', 'means', 'stuff', 'wants', 'like',
                     'going', 'exactly', 'feel', 'probably', 'likely', 'likes', 'thank', 'oopsie', 'rightfully', 'paul', '23andme', 'didn', 'know', 'just', 'really', 'able', 'actually', 'comes', 'does', 'left']
    tokens = [word for word in nltk.word_tokenize(text) if (len(word) > 3 and len(word.strip('Xx/')) > 2 and len(re.sub('\d+', '', word.strip('Xx/'))) > 3) and word not in wordstoremove ]
    tokens = map(str.lower, tokens)
    return tokens

def lda(input_file):

  with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

  df = pd.DataFrame(columns=["title", "url", "source", "text"])

  dfs_to_concat = []
  for source, articles in data.items():
      for article in articles:
          new_df = pd.DataFrame({
              "title": [article["title"]],
              "url": [article["url"]],
              "source": [source],
              "text": [article["text"]]
          })

          dfs_to_concat.append(new_df)
  df = pd.concat([df] + dfs_to_concat, ignore_index=True)


  vectorizer_count = CountVectorizer(tokenizer=tokenize, stop_words='english', max_df=0.50, max_features=500, lowercase=False, ngram_range=(1,2))
  countidf_vectors = vectorizer_count.fit_transform(df.text)

  feature_names = vectorizer_count.get_feature_names_out()

  lda_model = load('model_weights/best_lda_model.joblib')
  W1 = lda_model.fit_transform(countidf_vectors)
  H1 = lda_model.components_


  num_words=15

  vocab = np.array(feature_names)

  top_words = lambda t: [vocab[i] for i in np.argsort(t)[:-num_words-1:-1]]
  topic_words = ([top_words(t) for t in H1])
  topics = [' '.join(t) for t in topic_words]
  topics_str = '\n\n'.join(topics)

  histo, barchart = visualize(topics, df, W1, H1, lda_model, vectorizer_count)
  print("done")
  return topics_str, histo, barchart

def visualize(topics, df, W1, H1, lda_model, vectorizer):
  #label each document with a topic
  colnames = ["Topic" + str(i+1) for i in range(lda_model.n_components)]
  docnames = df['title']

  df_doc_topic = pd.DataFrame(np.round(W1, 2), columns = colnames, index=docnames)
  significant_topic = np.argmax(df_doc_topic.values, axis=1)

  #histogram of common topics
  df_doc_topic['dominant_topic'] = significant_topic + 1
  histogram_fig, histogram_ax = plt.subplots()
  df_doc_topic['dominant_topic'].hist(bins=7, ax=histogram_ax)
  histogram_ax.set_title('Histogram of Dominant Topics')

  #words of each topic
  fig, axes = plt.subplots(2, 4, figsize=(30, 15), sharex=True)
  axes = axes.flatten()
  for topic_idx, topic in enumerate(lda_model.components_):
    top_features_ind = topic.argsort()[:-10 - 1:-1]
    top_features = [vectorizer.get_feature_names_out()[i] for i in top_features_ind]
    weights = topic[top_features_ind]

    ax = axes[topic_idx]
    ax.barh(top_features, weights, height=0.7)
    ax.set_title(f'Topic {topic_idx +1}')
    ax.invert_yaxis()
  
  return histogram_fig, fig




  # df_doc_topic
  # print("Perplexity: ", lda_model.perplexity(countidf_vectors))




  # sns.heatmap(df_doc_topic.corr())
  # plt.show()


  # fig, axes = plt.subplots(2, 4, figsize=(30, 15), sharex=True)
  # axes = axes.flatten()
  # for topic_idx, topic in enumerate(best_lda_model.components_):
  #     top_features_ind = topic.argsort()[:-10 - 1:-1]
  #     top_features = [vectorizer_count.get_feature_names_out()[i] for i in top_features_ind]
  #     weights = topic[top_features_ind]

  #     ax = axes[topic_idx]
  #     ax.barh(top_features, weights, height=0.7)
  #     ax.set_title(f'Topic {topic_idx +1}')
  #     ax.invert_yaxis()
  # plt.show()
