# Given a database of tweets in json format, performs statistics/machine learning operations to analyze them
# Should have collected tweets, and run fix_json_db.py on the database

import tweet_processing
import NLP
import json

folder = "data"
db_number = 1
file_string_new = folder + '/stream_' + ("database"+str(db_number)+"_fixed") + '.json'

with open(file_string_new, 'r') as f:

    myTokenizer = tweet_processing.TweetTokenizer()
    myNLP = NLP.NLProcessor()
    myPol = tweet_processing.TweetPolitics()

    amlo_count = 0
    ricky_count = 0
    meade_count = 0
    bronco_count = 0

    for line in f:
        tweet = json.loads(line)

        # Uncomment to filter tweets that are replies to other users
        #if tweet['in_reply_to_status_id'] is not None:
        #   continue

        # Get tweet based on if it was retweeted, or if it has an extended field, or both
        if 'retweeted_status' in tweet:
            continue  # Currently ignores retweets
            # if 'extended_tweet' in tweet['retweeted_status']:
            #     tokens = myTokenizer.tokenize(tweet['retweeted_status']['extended_tweet']['full_text'], True)
            # else:
            #     tokens = myTokenizer.tokenize(tweet['retweeted_status']['text'], True)
        elif 'extended_tweet' in tweet:
            tokens = myTokenizer.tokenize(tweet['extended_tweet']['full_text'], True)
        else:
            tokens = myTokenizer.tokenize(tweet['text'], True)

        # Remove stopwords
        tokens_no_stopw = myNLP.rem_stop_words(tokens)

        # Keep tweets that mention only one candidate
        temp_cand = myPol.only_one_candidate(tokens_no_stopw)
        if temp_cand == '':
            continue

        # Determine if tweet mentions something about winning
        if not myPol.did_he_win(tokens_no_stopw):
            continue

        # If mention the debate
        if not myPol.mention_debate(tokens_no_stopw):
            continue

        # Add 1 to corresponding candidate
        if temp_cand == "amlo":
            amlo_count += 1
        elif temp_cand == "ricky":
            ricky_count += 1
        elif temp_cand == "meade":
            meade_count += 1
        elif temp_cand == "bronco":
            bronco_count += 1

        # Debugging code, print one tweet at a time with the candidate it got assigned
        # try:
        #     print(tweet['extended_tweet']['full_text'])
        # except:
        #     print(tweet['text'])
        # input(temp_cand)

# Print final count
print("amlove: {}\n".format(amlo_count))
print("ricky: {}\n".format(ricky_count))
print("meade: {}\n".format(meade_count))
print("bronco: {}".format(bronco_count))

