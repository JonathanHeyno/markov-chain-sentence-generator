# Week 6
Hours spent: 8

## Work done

- Created post processing logic for generated text (fixes some grammar and adds punctuations (.,?!) and stop words ('a', 'an', 'the'))
- Created custom method for tokenization to be used instead of nltk tokenize

## Results
The quality of the generated text has improved immensily with the latest changes. Punctuations and stop words are not recorded into
the trie, but each node keeps track if these occured before or after the word. The post processing logic uses this information to
determine if these should be placed between two words in the generated text.

Nltk tokenize has been replaced with a custom made method. Instead of minutes the tokenization now takes seconds.

## Next steps
- Finalize documentation