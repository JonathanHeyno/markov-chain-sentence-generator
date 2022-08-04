# Week 3
Hours spent: 14

## Work done

- Created logic for generating text using Markov chain from either initial words given by user or randomly selecting starting words
- Testing output with various types of input files
- Updated documentation

## Issues

-nltk tokenize package does the following: 'my brother's printer' --> ['my', 'brother', 's', 'printer']. It seems to not handle genitive forms correctly since it splits the word from the apostrophe into two separate words, e.g. brother's --> ['brother' + 's']. Need to maybe use something else instead or write logic for tokenizing myself.

- The generated text is kind of rambling. Increasing the order of the Markov chain might help.

- Poems and other relatively short texts with complex sentences and rarely used words lead to the generated text mostly repeating the source data, typically cutting one line and pasting it after some other one. More interesting text can be generated from large input files, like an entire book.

## Next steps
- Try different ways to make generated text more sensible. E.g. get program to keep words with apostrophes in text, experiment with keeping sentence ending punctuations (.?1) though this will probably require larger input files, like entire books or book collections. Can also try e.g. removing articles (the, a, an, ...) and stemming words, then creating logic to fit them into the generated text in the correct form and see if this generates more sensible text.

- Can also experiment what happens when mixing two or more different source texts together, e.g. two completely different books into the same input file.