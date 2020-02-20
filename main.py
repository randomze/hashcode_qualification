def parse_file(input_file):
    lines = input_file.readlines()

    b, l, d = [int(x) for x in lines[0].split()]

    book_scores = [[int(x), int(x), -1] for x in lines[1].split()]
    libraries = []
    for i in range(2, 2 * (l+1), 2):
        n, t, m = [int(x) for x in lines[i].split()]
        book_ids = set([int(x) for x in lines[i + 1].split()])
        average = sum(book_ids) / n
        to_be_removed = set()
        for j in book_ids:
            if book_scores[j][2] == -1:
                book_scores[j][2] = (i - 2) // 2
                book_scores[j][1] = book_scores[j][0] - average
            elif book_scores[j][1] < book_scores[j][0] - average:
                libraries[book_scores[j][2]][1].remove(j)
                libraries[book_scores[j][2]][2] = sum(libraries[book_scores[j][2]][0])
                book_scores[j][2] = (i - 2) // 2
                book_scores[j][1] = book_scores[j][0] - average
            else:
                to_be_removed.add(j)

        book_ids = book_ids.difference(to_be_removed)
        libraries += [((n, t, m), book_ids, sum(book_ids))]

    return ((b, l, d), book_scores, libraries) 

def weight(library, days_left):
    (n, t, m), book_ids, book_sum = library

    weight = (book_sum / m) / (days_left - t)
    return weight

if __name__=='__main__':
    input_file = open('a_example.txt', 'r')
    data = parse_file(input_file)

    print(data)
