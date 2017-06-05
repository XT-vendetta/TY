def read_file_to_list(file_dir):
    retval = []
    f = open(file_dir, 'rb')
    for line in f.readlines():
        line = line.strip('\n\r')
        retval.append(line)
    return retval