from psaw import PushshiftAPI
import datetime as dt
import json
# import pickle

api = PushshiftAPI()
subreddit = "depression"
#subreddit = "SuicideWatch"
start_epoch=int(dt.datetime(2017, 1, 1).timestamp())

info = ['selftext']

# get posts
# dictionary format with the filter attributes as keys
sub_results = [post.d_ for post in list(api.search_submissions(
                            after = start_epoch,
                            subreddit = subreddit,
                            filter = ['title','selftext', 'id'],
                            limit = 1000))]
#print(sub_results)

# map posts to comments
post_to_comment_dict = dict()

for post in sub_results:
    sub_id = post['id']
    # fetch comment ids
    comment_id_results = list(api._get_submission_comment_ids(sub_id))
    #print("sub_id: ", sub_id, " comments: ", comment_id_results)
    post_to_comment_dict[sub_id] = comment_id_results

# fetch comment data
for comment_list in post_to_comment_dict.values():
    # parent ids: t3 is original submission, t1 is another comment
    # is_submitter = true means that it is a reply from OP
    comment_results = [comment.d_ for comment in list(api.search_comments(
                            ids = comment_list,
                            filter = ['id', 'body', 'is_submitter', 'score']
                            ))]
    #print(comment_results)