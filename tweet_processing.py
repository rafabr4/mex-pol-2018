# Used to tokenize tweets and/or process them in terms of politics

import re


class TweetTokenizer:
    # Tokenizes tweets

    def __init__(self):

        # Setup re object for finding emojis
        emoji_str = r"""
                (?:
                    [>}]? # Eyebrows (optional)
                    [:=;8xX] # Eyes
                    [']? # Tears
                    [oO\-^]? # Nose (optional)
                    [D\)\]\(\[/\\oO0pPbB<>*3$sSL] # Mouth
                )|(?:
                    [D\)\]\(\[/\\oO0pPbB<>*3$sSL] # Mouth
                    [oO\-^]? # Nose (optional)
                    [']? # Tears
                    [:=;8xX] # Eyes
                    [<{]? # Eyebrows (optional)
                )"""

        # Setup re object for finding different entities
        regex_str = [
            emoji_str,
            r'<[^>]+>',  # HTML tags
            r'(?:@[\w_]+)',  # @-mentions
            r"(?:\#+[\w_\u00C0-\u00FF]+[\w\'_\-]*[\w_\u00C0-\u024F]+)",  # hashtags
            r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
            r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
            r"(?:[a-z\u00C0-\u00FF][a-z\u00C0-\u00FF'\-_]+[a-z\u00C0-\u00FF])",  # words with - and '
            r'(?:[\w_\u00C0-\u00FF]+)',  # other words
            r'(?:\S)'  # anything else
        ]

        self.tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
        self.emoticon_re = re.compile(r'^' + emoji_str + '$', re.VERBOSE | re.IGNORECASE)

    def tokenize(self, s, lowercase=False):
        # Converts tweets to tokens, lowercases them if flag true, keeps emojis

        tokens = self.tokens_re.findall(s)
        if lowercase:
            tokens = [token if self.emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens


class TweetPolitics:
    # Functions to process tweets and find info about politics

    def __init__(self):
        # Setup sets with keywords related to candidates, winning, losing, debate
        self.set_amlove = {r"amlo", r"andrés manuel lópez obrador", r"andrés manuel", r"@lopezobrador_", r"#amlo",
                           r"peje", r"morena", r"#morena"}
        self.set_ricky = {r"ricardo anaya", r"anaya", r"@ricardoanayac", r"#anaya", r"pan", r"#pan"}
        self.set_meade = {r"josé antonio meade", r"jose antonio meade", r"meade", r"@joseameadek", r"#meade"
                          r"pri", r"#pri"}
        self.set_bronco = {r"jaime rodriguez", r"jaime rodríguez", r"jaime rodriguez calderon",
                           r"jaime rodríguez calderón", r"@jaimerdznl", r"bronco", r"#bronco"}
        self.set_win = {r"ganó", r"gano", r"gana", r"ganar", r"victorioso", r"victoria", r"conquista", r"conquistó",
                        r"conquisto", r"triunfa", r"triunfó", "triunfo", r"vence", r"venció", r"vencio", r"domina",
                        r"dominó", r"domino"}
        self.set_lose = {r"pierde", r"perdió", r"perdio", r"perder", r"fracasa", r"fracasó", r"fracaso"}
        self.set_debate = {r"debate", r"#debate", r"#debateine", r"#debatepresidencial", r"#tercerdebate",
                           r"#tercerdebatepresidencial"}
        
    def only_one_candidate(self, t):
        # This function filters tweets that mention more than one candidate

        # XOR of candidates
        c1 = self.mentions_cand(t, 1)
        c2 = self.mentions_cand(t, 2)
        c3 = self.mentions_cand(t, 3)
        c4 = self.mentions_cand(t, 4)
        if c1 + c2 + c3 + c4 == 1:
            return c1*"amlo" + c2*"ricky" + c3*"meade" + c4*"bronco"
        else:
            return ''

    def mentions_cand(self, t, c):
        # Check if tweet mentions something about candidate c

        if c == 1:
            temp_set = self.set_amlove
        elif c == 2:
            temp_set = self.set_ricky
        elif c == 3:
            temp_set = self.set_meade
        elif c == 4:
            temp_set = self.set_bronco
        else:
            temp_set = ""

        for token in t:
            if token in temp_set:
                return 1

        # Return 0 otherwise
        return 0

    def did_he_win(self, t):
        # Check if tweet mentions something about winning the debate

        win = False
        for token in t:
            if token in self.set_win:
                win = True
            if token in self.set_lose:
                return False

        return win

    def did_he_lose(self, t):
        # Check if tweet mentions something about losing the debate

        lose = False
        for token in t:
            if token in self.set_lose:
                lose = True
            if token in self.set_win:
                return False

        return lose

    def mention_debate(self, t):
        # Check if tweet mentions something about the debate

        for token in t:
            if token in self.set_debate:
                return True

        return False
