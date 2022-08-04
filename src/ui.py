from service import service

class UI:

    def __init__(self):
        self._service = service

    def run(self):
        print("\n\n\nWelcome to Markov Chain Sentence Generator\n")
        choice = ''
        while choice != 'q':
            print("\nSelect action:\nR: Read input text file\nM: Set Markov chain order (current="+str(service.order)+")\nC: Create trie\nS: Search Trie\nG: Generate text\nQ: Quit")

            choice = input('\nAction: ').lower()

            if choice == 'r':
                print('\nCurrent file read in: ' + service.source_file)
                name = input("\nEnter name of new file or 'C' to cancel: ").lower()
                if name != 'c':
                    print(service.read_source_file(name))

            if choice == 'c':
                print(service.create_trie_and_count_frequencies())

            if choice == 'm':
                order = input("\nSet order of Markov chain: ").lower()
                if order.isnumeric():
                    service.order = order
                    print('\nMARKOV CHAIN SET TO ORDER ' + str(self._service.order) + '\n')
                else:
                    print('\nMUST BE A NUMBER\n')

            if choice == 's':
                words = input("\nEnter search words (e.g. the cat jumped): ").lower().split()
                if len(words) != service.order + 1:
                    print('\nMARKOV CHAIN IS ORDER '+ str(service.order) + '. MUST INPUT ' + str(service.order + 1) + ' WORDS\n')
                else:
                    frequency = service.search_trie(words)
                    if frequency > 0:
                        print('\nWORDS FOUND, FREQUENCY = ' + str(frequency) + '\n')
                    else:
                        print('\nWORDS NOT FOUND. MAYBE TRIE NEEDS TO BE RECREATED AFTER RE-READING NEW INPUT FILE OR CHANGING MARKOV ORDER\n')

            if choice == 'g':
                max_length = input('\n\nSet maximum amount of words in generated text (default = 100): ')
                if not max_length.isnumeric():
                    max_length = '100'

                initial_words = input("\nEnter "+ str(service.order)+ " initial words or start with random words (Enter): ").lower().split()
                if (not initial_words or len(initial_words) == service.order):
                    text = service.generate_text(int(max_length), initial_words)
                    print('\nGENERATED TEXT:\n\n')
                    print(text)
                else:
                    print('\nYOU MUST INPUT ' + str(service.order) + ' WORDS OR NO WORDS!\n')
