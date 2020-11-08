# def format_time(time):
#     if(time > 60):
#         new_time = round(time / 60)
#         if(new_time > 60):
#             new_time = round(new_time / 60)
#             return str(new_time) + " hours"
#         return str(new_time) + " minutes"
#     else:
#         return str(round(time)) + " seconds"


# def Log_Transcript(transcript, path):
#     with open('transcript.txt', mode='w') as file:
#         file.write(str(transcript))
#         file.close()

# # TODO: better text formatting for words


# def Log_Word_List(word_list, path):
#     with open(path + '_word_list.txt', mode='w') as file:
#         for word in word_list:
#             file.write(str(word) + '\n')
#         file.close()


# def Log_Frame(word, time):
#     new_time = format_time(time)
#     print('FRAME', word, 'CREATED IN', new_time)


# def Log_Final(title, time, vid_path):
#     new_time = format_time(time)
#     print('CREATED VIDEO', title, "IN", new_time, "OUTPUT", vid_path)

def format_time(time):
    if(time > 60):
        new_time = round(time / 60)
        if(new_time > 60):
            new_time = round(new_time / 60)
            return str(new_time) + " hours"
        return str(new_time) + " minutes"
    else:
        return str(round(time)) + " seconds"


def Log_Frame(logger, word, time):
    self.logger = logger
    new_time = format_time(time)
    logger.info('FRAME', word, 'CREATED IN', new_time)


def Log_Final(logger, title, time, vid_path):
    new_time = format_time(time)
    logger.info('CREATED VIDEO', title, "IN", new_time, "OUTPUT", vid_path)


def Log_Word_List(logger, word_list):
    logger.info('LOGGED WORDS')
