from service import service

class UI:

    def __init__(self):
        self._service = service

    def run(self):
        print("\n\n\nWelcome to Markov Chain Sentence Generator\n")
        choice = ''
        while choice != 'q':
            print("\nSelect action:\nM: Set Markov chain order (current="+str(service.order)+")\nR: Read input text file\nG: Generate text\nQ: Quit")

            choice = input('\nAction: ').lower()

            if choice == 'r':
                print('\nCurrent file read in: ' + service.source_file)
                name = input("\nEnter name of new file (e.g. text_for_pytest.txt) or 'C' to cancel: ").lower()
                if name != 'c':
                    print(service.read_source_file(name))
                    print('Creating trie...')
                    print(service.create_trie_and_count_frequencies())

            if choice == 'm':
                order = input("\nSet order of Markov chain: ").lower()
                if order.isnumeric():
                    service.order = order
                    print('\nMARKOV CHAIN SET TO ORDER ' + str(self._service.order))
                    if self._service.source_file:
                        print('Creating trie...')
                        print(service.create_trie_and_count_frequencies())
                else:
                    print('\nMUST BE A NUMBER\n')

            if choice == 'g':
                max_length = input('\n\nSet maximum amount of words in generated text (default = 100): ')
                if not max_length.isnumeric():
                    max_length = '100'

                text = service.generate_text(int(max_length))
                print('\nGENERATED TEXT:\n\n')
                print(text)
