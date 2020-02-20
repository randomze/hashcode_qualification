def parse_file(input_file):
    lines = input_file.readlines()

    b, l, d = [int(x) for x in lines[0].split()]

    book_scores = [int(x) for x in lines[1].split()]
    libraries = []
    for i in range(2, 2 * (l+1), 2):
        print(i)
        n, t, m = [int(x) for x in lines[i].split()]
        book_ids = [int(x) for x in lines[i + 1].split()]
        libraries += [((n, t,m), book_ids)]

    return ((b, l, d), book_scores, libraries) 

if __name__=='__main__':
    input_file = open('a_example.txt', 'r')
    data = parse_file(input_file)

    print(data)
