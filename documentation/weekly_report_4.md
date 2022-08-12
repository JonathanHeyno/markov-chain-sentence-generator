# Week 4
Hours spent: 18

## Work done

- Improved cleaning up input file and breaking input text into separate sentences
- Implemented part of speech tagging
- Storing also sentence structures (e.g. "Personal pronoun" - "Past tense verb" - "Preposition" - ...)
- Creating sentences according to sentence structures, i.e. select next word based on previous words and required part of speech
- Updated documentation

## Issues
- Code is somewhat messy, needs to be refactored
- Not sure sentence structure requirement has improved generated text quality, possibly even made it worse.
- Run into problems if previous words do not have any word that follows in the required form (e.g. word1 + word2 + adverb -- BUT word1 + word2 are not followed by an adverb anywhere in the text).

## Next steps
- Try different ways to use part of speech tagging:
	- For instance now the program stores the sentence structures in the text and selects one to follow, could maybe instead store parts of speech into a trie like the words and have the program generate the sentence structure instead of simply copying one fro the source text
	- Instead of storing word1 + word2 + next_word, could try part_of_speech + part_of_speech + next_word. E.g. store into the trie: noun + adjective + next_word
