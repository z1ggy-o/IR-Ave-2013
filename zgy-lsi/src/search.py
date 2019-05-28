import lsi
import signal
import sys


def search(k=None):
    my_lsi = lsi.LSI(k)
    my_lsi.create_matrix()  # Create term-document matrix
    my_lsi.svd()  # Do SVD on term-doc matrix

    while True:
        query = input('Please entry your query (use Ctrl-C to exit): ')
        my_lsi.search(query)


def start():
    k = input('Please input dimension of LSI space. (Push entry to use default rank): ')
    print('Need sometime to initial the system. Please wait few seconds.\n')
    if len(k) == 0:
        search()
    elif k.isdigit():
        search(int(k))
    else:
        print('Please input a integer.\n')
        start()

if __name__ == '__main__':
    def handler(signal, frame):
        print('\nBye bye~')
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)

    start()
