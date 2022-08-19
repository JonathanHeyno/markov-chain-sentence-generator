# Week 5
Hours spent: 18

## Work done

- Experimented with different ways to generate more sensible text
- Reverted back to using the original logic for sentence generation

## Issues
After trying a multitude of different ways to generate text, I have come to the conclusion that is best to generate
text as originally intendend, and then create some logic for post-processing the generated text to improve the grammar
and sentence structure:
- Trying to get the chain to follow a specific sentence structure (noun - verb -preposition - ...) is problematic. Even when
the source data is something like Shakespeare, we run into the problem that the sentence
structures are long and very varied, and even though there are hundereds or thousands of pages of text, there are a huge amount
of different meaningful words that are used very rarely. This means we basically always run into a situation where we have e.g. two words, and
need to select the next word based on those. However, there are only a few possible choices, none of which are in the form required
by the sentence structure. So the Markov process stops and we only managed to get a few words.
- Tried storing parts of speech into the trie instead of words, i.e. pronoun + verb + "cats" and have the chain select the next
word based on the previous words' parts of speech. This results in a disjointed mess with words that have no connection to one another.
- Removing all stop words means we are left with meaningful words. The problem again is that even in very long and rich texts,
there are lots of different meaningful words but they are used very rarely, so we end up mostly repeating the source text.
Hence it seems better to determine yourself a very limited set of stop words to remove (like "a", "and" "the", nothing else)
- Using e.g. nltk tokenize does the following: don't --> do n't. The problem here is that if we e.g. use a second order Markov chain,
we have a situation like "word1 + don't" and need to get the next word based on "word1 + don't". If we split don't --> do + n't
the next word will be obtained based on "do + n't". This means that the next word to be selected can be virtually anything and will
have no connection to word1. One way to fix this is to not use nltk tokenize but split the words myself. Another, which might be better,
is to raise the order of the Markov chain to 3, which seems to also improve the sentence quality. With a large amount of text we don't
end up simply repeating it (as long as we don't take out all the stop words).

Because of these problems I am going back to the original idea and implementing some post-processing logic to deal with the gramatical issues.

## Next steps
- Create logic for post processing the generated text
