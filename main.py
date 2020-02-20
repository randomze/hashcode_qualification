import sys

def parse_file(input_file):
    lines = input_file.readlines()

    b, l, d = [int(x) for x in lines[0].split()]

    book_scores = [[int(x), int(x), -1] for x in lines[1].split()]
    libraries = []
    for i in range(2, 2 * (l+1), 2):
        n, t, m = [int(x) for x in lines[i].split()]
        book_ids = set([int(x) for x in lines[i + 1].split()])
        average = sum(book_ids) * m / n
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
        libraries += [[(n, t, m, (i - 2) // 2), book_ids, sum(book_ids)]]

    return ((b, l, d), book_scores, libraries) 

def weight(library):
    (n, t, m, id_number), book_ids, book_sum = library

    weight = (book_sum * m) / (t)
    return weight

if __name__=='__main__':
    for files in sys.argv[1:]:
        input_file = open(files, 'r')
        output_file = open(files + '.out' , 'w+')
        (b, l, d), book_scores, libraries = parse_file(input_file)
        libraries = sorted(libraries, key=lambda library: weight(library), reverse=True)
        time_remaining = d
        number_of_libraries = 0 
        libraries_output = []
        for library in libraries:
            (n, t, m, id_number), book_ids, book_sum = library
            time_remaining -= t
            if time_remaining > 0:
                number_of_libraries += 1
                book_ids = list(book_ids)
                book_ids = sorted(book_ids, key=lambda book: book_scores[book][0], reverse=True)
                to_be_sent = []
                for i in range(time_remaining, 0, -1):
                    if not book_ids:
                        break
                    to_be_sent.extend(book_ids[0:m])
                    book_ids = book_ids[m:]

                libraries_output += [(id_number, to_be_sent)]
            
        if number_of_libraries > 0:
            output_file.write('{}\n'.format(number_of_libraries))
            for library in libraries_output:
                id_number, book_list = library
                if len(book_list) > 0:
                    output_file.write('{} {}\n'.format(id_number, len(book_list)))
                    for i in range(len(book_list)):
                        if i + 1 != len(book_list):
                            output_file.write('{} '.format(book_list[i]))
                        else:
                            output_file.write('{}\n'.format(book_list[i]))
        input_file.close()
        output_file.close()
