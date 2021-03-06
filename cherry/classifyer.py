# -*- coding: utf-8 -*-

"""
cherry.classify
~~~~~~~~~~~~
This module implements the cherry classify.
:copyright: (c) 2018-2019 by Windson Yang :license: MIT License, see LICENSE for more details.
"""


import os
import numpy as np
from sklearn.exceptions import NotFittedError
from .base import load_cache
from .exceptions import TokenNotFoundError


class Classify:
    def __init__(self, model, **kwargs):
        text = kwargs['text']
        self._load_cache(model)
        self.probability, self.word_list = self._classify(text)

    @property
    def get_word_list(self):
        return self.word_list

    @property
    def get_probability(self):
        return self.probability

    def _load_cache(self, model):
        '''
        Load cache from pre-trained model
        '''
        self.trained_model = load_cache(model, 'clf.pkz')
        self.vector = load_cache(model, 've.pkz')

    def _classify(self, text):
        '''
        1. Build vector using pre-trained cache
        2. Transform the input text into text vector
        3. return the probability and word_list
        '''
        if isinstance(text, str):
            text = [text]
        try:
            text_vector = self.vector.transform(text)
        except NotFittedError:
            error = 'Some of the tokens in text never appear in training data'
            raise TokenNotFoundError(error)
        word_list = []
        for tv in text_vector.toarray():
            feature_names = np.asarray(self.vector.get_feature_names())
            word_list.append(sorted([word for word in list(zip(tv, feature_names)) if word[0] != 0.0], reverse=True))
        probability = self.trained_model.predict_proba(text_vector)
        return probability, np.asarray(word_list)
