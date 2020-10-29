def Log_Word_List(word_list, path):
    with open(path + 'word_list.txt', mode='w') as file:
        for word in word_list:
            file.write(str(word))
        file.close()


def Log_Frame(word, time):
    print('FRAME', word, 'CREATED IN', time, "sec")


def Log_Final(title, time, vid_path):
    print('CREATED VIDEO', title, "IN", time, "sec, OUTPUT", vid_path)
