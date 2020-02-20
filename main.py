import math
import sys

def parse_file(input_file):
    lines = input_file.readlines()

    b, l, d = [int(x) for x in lines[0].split()]

    book_scores = [[int(x), int(x), -1] for x in lines[1].split()]
    libraries = []
    for i in range(2, 2 * (l+1), 2):
        n, t, m = [int(x) for x in lines[i].split()]
        book_ids = set([int(x) for x in lines[i + 1].split()])
        library = [(n, t, m, (i - 2) // 2), book_ids, sum(book_ids)]
        average = weight(library, d) * (library[2] * m / n)
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

        library[1] = book_ids.difference(to_be_removed)
        libraries += [library]

    return ((b, l, d), book_scores, libraries) 

def weight(library, days):
    (n, t, m, id_number), book_ids, book_sum = library

    weight = -1
    if days - t != 0:
        weight = (book_sum ) / (m * (days - t))
    return weight

if __name__=='__main__':
    score_file = open('scores', 'w+')
    for files in sys.argv[1:]:
        input_file = open(files, 'r')
        output_file = open(files + '.out' , 'w+')
        (b, l, d), book_scores, libraries = parse_file(input_file)
        time_remaining = d
        libraries = sorted(libraries, key=lambda library: weight(library, time_remaining), reverse=False)
        number_of_libraries = 0 
        libraries_output = []
        time_elapsed = 0

        for i in range(len(libraries)):
            library = libraries[i]
            (n, t, m, id_number), book_ids, book_sum = library
            time_remaining -= t
            time_elapsed += t
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
                    time_elapsed += 1

                if to_be_sent:
                    libraries_output += [(id_number, to_be_sent)]
                else:
                    number_of_libraries -= 1

                if time_elapsed / d > 0.025:
                    time_elapsed = 0
                    libraries[i:] = sorted(libraries[i:], key=lambda library: weight(library, time_remaining), reverse=False)

            
        if number_of_libraries > 0:
            score = 0
            output_file.write('{}\n'.format(number_of_libraries))
            for library in libraries_output:
                id_number, book_list = library
                if len(book_list) > 0:
                    temp = sum([book_scores[x][0] for x in book_list])
                    score += temp
                    output_file.write('{} {}\n'.format(id_number, len(book_list)))
                    for i in range(len(book_list)):
                        if i + 1 != len(book_list):
                            output_file.write('{} '.format(book_list[i]))
                        else:
                            output_file.write('{}\n'.format(book_list[i]))


        score_file.write('{} got {} points\n'.format(files, score))
        input_file.close()
        output_file.close()
    score_file.close()
