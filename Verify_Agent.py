import numpy as np
from selfcheckgpt.modeling_selfcheck import SelfCheckMQAG, SelfCheckBERTScore, SelfCheckNgram


class ResponseVerificationModule:

	def __init__(self):
		self.selfcheck_mqag = SelfCheckMQAG()  # set device to 'cuda' if GPU is available
		self.selfcheck_bertscore = SelfCheckBERTScore(rescale_with_baseline=True)
		self.selfcheck_ngram = SelfCheckNgram(n=1)  # n=1 means Unigram, n=2 means Bigram, etc.

	def verify(self, primary_response, sample_responses):
		sentences = [sent.text.strip() for sent in nlp(primary_response).sents]
		sent_scores_mqag = self.selfcheck_mqag.predict(
			sentences=sentences,  # list of sentences
			passage=primary_response,  # passage (before sentence-split)
			sampled_passages=sample_responses,  # list of sampled passages
			num_questions_per_sent=5,  # number of questions to be drawn
			scoring_method='bayes_with_alpha',  # options = 'counting', 'bayes', 'bayes_with_alpha'
			beta1=0.8, beta2=0.8,  # additional params depending on scoring_method
		)
		verification_score = np.mean(sent_scores_mqag)
		return True if verification_score < 0.3 else False
