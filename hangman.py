# main goal: create functioning game loop for basic "hangman" game.
# user has a limited number of guesses to complete a word pulled at random from a word list
# stored in a text file. implement option to play again upon game completion (win or loss).
# basic functionality ideas: print # of guesses left. restrict user input to one letter at a time. support multi-word answers.
# additional functionality ideas: ascii art or similar indicator of number of guesses left. support multiple themed word lists (chosen at start/restart)

import random

#list of valid guesses to be compared against user input (standard English alphabet only). non-capitalized guesses are converted into capitals before comparison.
alpha = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")

def wordblank(word):
    """Takes the secret word and replaces each non-whitespace character with an underscore ('blank'). Forms the initial 'word board.'"""
    blanked = ""
    for char in word:
        if char == " ":
            blanked += (" ")
            continue
        blanked += ("_")
    return blanked

def spacy(wordboard): #note to self: find a more concise way to do this with built-in methods/formatting, possibly using split/join
    """Spaces out the underscores in the word board for better readability when printing."""
    spaced = ""
    for char in wordboard:
        if char == " ":
            spaced += ("  ")
            continue
        else:
            spaced += char + " "
    return spaced

def wordfill(wordboard, word, correctguess):
    """When the player guesses a letter correctly, this function checks to see which "blanks" on the word board need
    to be filled with the letter, then returns an updated word board. The Vanna White function."""
    new_wordboard = ""
    for i in range(len(word)):
        if word[i] == correctguess:
            new_wordboard += correctguess
        else:
            new_wordboard += wordboard[i]
    return new_wordboard

def main():
    global alpha

    # open word list (and throw exception if not found):
    try:
        hanglist = open("hanglist.txt") #A file containing multiple words, all caps, one on each line. Current theme: Mammals
        wordlist = hanglist.readlines()

    except FileNotFoundError:
        print("ERROR: Hangman word list not found!")
        raise

    # create list of guessable words from text file

    gameloop = True

    while gameloop == True:
        #draw new word before initiating game:
        word = random.choice(wordlist).rstrip("\n") #no longer length-dependent!!
        unspacedword = word.replace(" ", "") #removes spaces between two words for use in anything that requires a total letter count (mainly wordfill())
        wordboard = wordblank(word)

        chances = 6 #I can make a fancy visual thing later. maybe make difficulty level adjustable by changing this number

        guessfails = [] #incorrect guesses

        #game intro

        print("Let's play Hangman! Try to guess the word letter by letter. You can only make 6 mistakes!")
        print(f"This word has {len(unspacedword)} letters.")
        if "  " in wordboard:
            print ("This time, it's made of two words.")

        while wordboard.replace(" ","") != unspacedword:
            #round intro
            print(spacy(wordboard))
            if guessfails:
                print("PREVIOUS GUESSES: ", guessfails) #make this prettier later I guess
            print("\n")

            #guess prompt:
            if chances == 1:
                guess = input("Try guessing another letter. You can't make any more mistakes now! ")
            elif chances == 6:
                guess = input("Try guessing a letter. The game will end if you make 6 incorrect guesses. ")
            elif chances <= 0:
                print(f"GAME OVER! The word was {word}. Better luck next time!")
                print("\n")
                break
            else:
                guess = input(f"Try guessing another letter. The game will end if you make {chances} more incorrect guesses. ")

            guess = guess.upper()

            #guess evaluation

            if guess not in alpha or len(guess) != 1:
                continue
            elif guess in guessfails or guess in wordboard:
                print("You tried that one already.")
                continue
            elif guess in word:
                print("Got one!")
                wordboard = wordfill(wordboard, word, guess)
            else:
                print(f"Nope! No {guess}s in this word!")
                chances -=1
                guessfails += guess

        else:
            print("Congratulations! You found the word!")
            print("\n")

        #reset check

        quit = False

        while True:
            reset = input("Do you want to play again? (Y/N) ")
            if reset.lower() == "y" or reset.lower == "yes":
                print("\n")
                break
            elif reset.lower() == "n" or reset.lower == "no":
                print("\n")
                print("Thanks for playing!")
                quit = True
                break
            else:
                print("\n")
                continue

        if quit == True:
            gameloop = False


if __name__ == "__main__":
    main()
