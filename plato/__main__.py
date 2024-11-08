from plato.epub import Epub

def main():
    epub = Epub()
    epub.generate()
    epub.write()

if __name__ == "__main__":
    main()
