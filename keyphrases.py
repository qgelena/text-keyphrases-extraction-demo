#!/usr/bin/env python3
import RAKE
import operator
import gensim

test_text = "AI Platform Pipelines has two major parts: (1) the infrastructure \
for deploying and running structured AI workflows that are integrated with Google \
Cloud Platform services and (2) the pipeline tools for building, debugging, and sharing \
pipelines and components. The service runs on a Google Kubernetes cluster that’s \
automatically created as a part of the installation process, and it’s accessible via \
the Cloud AI Platform dashboard. With AI Platform Pipelines, developers specify a \
pipeline using the Kubeflow Pipelines software development kit (SDK), or by customizing \
the TensorFlow Extended (TFX) Pipeline template with the TFX SDK. This SDK compiles \
the pipeline and submits it to the Pipelines REST API server, which stores and schedules \
the pipeline for execution."

class KeywordsExtractor:
    STOPWORDS_PATH = 'SmartStoplist.txt'

    def __init__(self):
        self.rake_extractor = RAKE.Rake(self.STOPWORDS_PATH)

    def get_keywords(self, text, sortby=None, count=None):
        """ Тут буде документація """
        tokens = preprocess(text)
        text = ' '.join(tokens)
        keywords = self.rake_extractor.run(text)
        if sortby == 'relevance':
            keywords.sort(key=lambda v: v[1], reverse=True)
        if count:
            keywords = keywords[:count]
        return keywords

def preprocess(text):
    '''Remove stopwords and remove words with 2 or less characters'''
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if len(token) > 2:
            result.append(token)
            
    return result

if __name__ == '__main__':
    extractor = KeywordsExtractor()
    keywords = extractor.get_keywords(test_text, count=5, sortby='relevance')
    print('keywords: ', *keywords, sep='\n')