# Does it really need a description?

import twitter_stream
import os
from datetime import datetime, time, date, timedelta

# determine database number according to latest database found
folder = "data"
db_number = 1
for file in os.listdir(folder):
    if "database" in file:
        db_number += 1

# Words to track in twitter stream
query = r"""amlo,andrés manuel lópez obrador,andrés manuel,ricardo anaya,anaya,josé antonio meade,meade,
        jose antonio meade,jaime rodriguez,jaime rodríguez,jaime rodriguez calderon,jaime rodríguez calderón,
        bronco,@lopezobrador_,@RicardoAnayaC,@JoseAMeadeK,@JaimeRdzNL,#debateine,#debateINE,#DebateINE
        """
tweet_limit = 15 # Used only if time_flag = false
startdate = date(2018, 6, 12) # Used only if time_flag = true
starttime = time(hour=21, minute=45, second=0)
datetime_start = datetime.combine(startdate, starttime)
duration = timedelta(hours=2, minutes=15)
datetime_end = datetime_start + duration

# Get tweets
twitter_stream.collect_tweets(folder, query, tweet_limit, datetime_start, datetime_end, db_number, time_flag=True)