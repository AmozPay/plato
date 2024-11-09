from plato.dictionary import Dictionary

def main():
    d = Dictionary(author="Amoz Pay", name="My Dict", input_lang="El", output_lang="El")
    d.new_page("a")
    d.add_entry("Amoz", "Jeune homme stylé")
    d.generate()
    print(d)

if __name__ == "__main__":
    main()
