# Week 1
Hours spent: 18

## Work done

- Reading through course material
- Determining project subject
- Reading material on Markov chains, trie structures, hidden Markov models, part of speech recognition, Viterbi algorithm
- Studied midi files and Python mido library to try to see if I could make the program compose music.
- Outlined logic of the program and wrote documentation

## Issues
Decided to have the program read and generate text instead of music, because I want the program to be able to generate an output in a similar style to the input. The problem I ran into with midi files is that there are several different ways in which they can be made, so determining when a note starts and ends might have to follow a different logic depending on who made the midi file. Additionally, some files have several tracks, meta messages and control shifts to different tracks among the notes which are necessary for the music to sound right but make a ridiculous outcome if randomly placed somewhere by a Markov chain. This could work better if I made the midi files myself, which I don't want to do since then only files made the way I make them would generate any sensible outcome.


## Next steps
- Create a logic for reading a text file and creating a trie structure.
- Start building automated testing and test coverage
