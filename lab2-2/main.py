import sys
from lexer import Lexer

def main():
    if len(sys.argv) <= 1:
        print("usage: {0} <filename>".format(sys.argv[0]))
        return

    filename = sys.argv[1]
    with open(filename) as f:
        source = f.read()

    lexer = Lexer()
    st, pif, errors = lexer.Start(source)
    if len(errors) != 0:
        for error in errors:
            print(error)
    else:
        print(st)
        print(pif)

if __name__ == '__main__':
    main()
