"""

CS5010: Final Project
Names: Aditi Rajagopal, Bradley Katcher, Charlie Putnam
Computing-ID: ar5vt, bk5pu, cmp2cz
Content: Unit Test Suite for final_project_praw.py
Notes: Comment out code in final_project_praw.py that generates the word cloud etc before running
TO DO: Move word cloud, df generated code from final_project_praw.py to different file, add more tests?
"""

from final_project_praw import RedditPostParse
import unittest

#inherits from unittest class
class TestRedditPostParse(unittest.TestCase): 

    def test_num_posts(self):
      redditComments = RedditPostParse("https://www.reddit.com/r/CFB/comments/cejgo2/jim_harbaugh_is_fine_urban_meyer_isnt_going_to/", 'michigan', 'ohiostate')
      redditComments.getComments()
      self.assertEqual(len(redditComments.postDetails), 18)      

    def test_sentiment_score_type(self):
      redditComments = RedditPostParse("https://www.reddit.com/r/CFB/comments/cejgo2/jim_harbaugh_is_fine_urban_meyer_isnt_going_to/", 'michigan', 'ohiostate')
      redditComments.getComments()
      self.assertIsInstance(type(redditComments.postDetails[0]['sentimentScore']), dict.__class__)

    def test_comment_type(self):
      redditComments = RedditPostParse("https://www.reddit.com/r/CFB/comments/cejgo2/jim_harbaugh_is_fine_urban_meyer_isnt_going_to/", 'michigan', 'ohiostate')
      redditComments.getComments()
      self.assertIsInstance(type(redditComments.postDetails[0]['comment']), str.__class__)

    def test_df_size(self):
      redditComments = RedditPostParse("https://www.reddit.com/r/CFB/comments/cejgo2/jim_harbaugh_is_fine_urban_meyer_isnt_going_to/", 'michigan', 'ohiostate')
      redditComments.getComments()
      commentDF = redditComments.getDataFrame()
      self.assertEqual(commentDF.shape, (18, 11))

    def test_df_cols(self):
      redditComments = RedditPostParse("https://www.reddit.com/r/CFB/comments/cejgo2/jim_harbaugh_is_fine_urban_meyer_isnt_going_to/", 'michigan', 'ohiostate')
      redditComments.getComments()
      commentDF = redditComments.getDataFrame()
      self.assertEqual(list(commentDF.columns), ['author', 'flair', 'comment', 'timeStamp', 'textblobScore', 'votes', 'flair_clean', 'neg', 'neu', 'pos', 'compound'])

    def test_timestamp_type(self):
      redditComments = RedditPostParse("https://www.reddit.com/r/CFB/comments/cejgo2/jim_harbaugh_is_fine_urban_meyer_isnt_going_to/", 'michigan', 'ohiostate')
      redditComments.getComments()
      self.assertIsInstance(type(redditComments.postDetails[0]['timeStamp']), str.__class__)

    def test_df_scoreType(self):
      redditComments = RedditPostParse("https://www.reddit.com/r/CFB/comments/cejgo2/jim_harbaugh_is_fine_urban_meyer_isnt_going_to/", 'michigan', 'ohiostate')
      redditComments.getComments()
      commentDF = redditComments.getDataFrame()
      self.assertIsInstance(type(commentDF[:]['neg']), float.__class__)
      self.assertIsInstance(type(commentDF[:]['pos']), float.__class__)
      self.assertIsInstance(type(commentDF[:]['neu']), float.__class__)
      self.assertIsInstance(type(commentDF[:]['compound']), float.__class__)

if __name__ == '__main__':
    unittest.main()