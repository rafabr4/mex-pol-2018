# For removing blank lines and errors stored in database due to limits in the twitter streaming API

folder = "data"
db_number = 1
file_string = folder + '/stream_' + ("database"+str(db_number)) + '.json'
file_string_new = folder + '/stream_' + ("database"+str(db_number)+"_fixed") + '.json'

with open(file_string_new, 'a') as f_new:
    with open(file_string, 'r') as f:
        for line in f:
            if line == "\n":
                continue
            if line.startswith('{"limit"'):
                continue
            f_new.write(line)