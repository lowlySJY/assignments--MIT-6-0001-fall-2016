# Problem Set 2, hangman.py
# Name: jinyi
# Collaborators:
# Time spent:7~8h

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print(len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """

    return random.choice(wordlist)
# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    f = True
    for i in secret_word:
        flag = 0
        for j in letters_guessed:
            if i == j:
                flag += 1
        # when flag is not 0, respresnt that i is in letters_guessed
        if flag == 0:
            f = False
            break       
    return f



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    L = ''
    for i in secret_word:
        flag = 0
        for j in letters_guessed:
            if i == j:
                flag += 1
        if flag == 0:
            L = L + '_ '
        else:
            L = L + i    
    return(L)



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # get a string comprised of all lowercase letters:
    alphabet = string.ascii_lowercase
    L = ''
    for i in alphabet:
        flag = 0
        for j in letters_guessed:
            if i == j:
                flag += 1
        if flag == 0:
            L = L + i        
    return L
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    
    # Initialization
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")    
    remaining_guess = 6 # num of guessing chane
    warnings = 3 # num of warnings
    letters_guessed = '' # letters that have guessed by the user  
    vowels = 'aeio' # If the vowel hasn’t been guessed and the vowel is not in the secret word, the user loses two guesses.
    print("You have", warnings, "warnings left.")
    print("---------------------------------------")
    lose = True
    while (remaining_guess > 0):
            print("You have", remaining_guess, "guesses left.")
            print("Available letters:", get_available_letters(letters_guessed))
            print("Please guess a letter:",end='')
            user_input = input()
            user_input = str.lower(user_input)
            # flag is used to judging the input whether come before
            flag = True
            for i in letters_guessed:
                if i == user_input:
                    flag = False
            if not(flag):
                warnings -= 1
                # if remaining guess samller than 0, the player will lose one guess
                if warnings <= 0:
                    remaining_guess -= 1
                    print("Oops! You've already guessed that letter. You have no warnings left:", get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! You've already guessed that letter. You have", warnings, "warnings left:", get_guessed_word(secret_word, letters_guessed))
                print("---------------------------------------")
                continue                               
            # the upper judge if the input is alpha
            if str.isalpha(user_input):
                # input is right letter and update letters_guessed. 
                letters_guessed += user_input
                # when the letter is in the secret word, print good guess
                if is_word_guessed(user_input, secret_word):                    
                    print("Good guess:", get_guessed_word(secret_word, letters_guessed))
                elif(is_word_guessed(user_input, vowels)):
                    remaining_guess -= 2
                    print("Oops! That vowel letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
                else:
                    remaining_guess -= 1
                    print("Oops! That Consonants letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
            # input is not letter
            else:
                warnings -= 1
                if warnings <= 0:
                    remaining_guess -= 1
                    print("Oops! You've already guessed that letter. You have no warnings left:", get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! You've already guessed that letter. You have", warnings, "warnings left:", get_guessed_word(secret_word, letters_guessed))
            print("---------------------------------------")
            unique_letters = secret_word[0]
            for m in secret_word:
                flag = True
                for n in unique_letters:
                    if m == n:
                        flag = False
                        break
                if flag:
                    unique_letters += m                
            if is_word_guessed(secret_word, letters_guessed):   
                score = remaining_guess * len(unique_letters)
                print("Congratulations, you won!")
                print("Your total score for this game is:",score)
                lose = False
                break
    if lose:
        print("Sorry, you ran out of guesses. The word was",secret_word,".")
        
        
# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # remove the space in my_word
    m = my_word.replace(' ','')
    # At first, judging whether the length is same.
    if len(m) == len(other_word):
        flag = True
        for i in range(len(m)):
            if m[i] != '_':
                if m[i] != other_word[i]:
                    flag = False
                    break
            # the hidden letter (_ ) cannot be one of the letters in the word that has already been revealed.
            else:
                for j in m:
                    if j == other_word[i]:
                        flag = False                
        if flag:
            return True
        else:
            return False
    else:
        return False


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    no_word = True
    for word in wordlist:
        if match_with_gaps(my_word, word): 
            no_word = False
            print(word)
    if no_word:
        print("No matches found")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    
    # Initialization
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")    
    remaining_guess = 6 # num of guessing chane
    warnings = 3 # num of warnings
    letters_guessed = '' # letters that have guessed by the user  
    vowels = 'aeio' # If the vowel hasn’t been guessed and the vowel is not in the secret word, the user loses two guesses.
    print("You have", warnings, "warnings left.")
    print("---------------------------------------")
    lose = True
    while (remaining_guess > 0):
            print("You have", remaining_guess, "guesses left.")
            print("Available letters:", get_available_letters(letters_guessed))
            print("Please guess a letter:",end='')
            user_input = input()
            user_input = str.lower(user_input)
            # * is used to given hint
            if user_input == '*':
                print("Possible word matches are:")
                show_possible_matches( get_guessed_word(secret_word, letters_guessed))
                print("---------------------------------------")
                continue
            # flag is used to judging the input whether come before
            flag = True
            for i in letters_guessed:
                if i == user_input:
                    flag = False
            if not(flag):
                warnings -= 1
                # if remaining guess samller than 0, the player will lose one guess
                if warnings <= 0:
                    remaining_guess -= 1
                    print("Oops! You've already guessed that letter. You have no warnings left:", get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! You've already guessed that letter. You have", warnings, "warnings left:", get_guessed_word(secret_word, letters_guessed))
                print("---------------------------------------")
                continue                               
            # the upper if block will judge if the input is alpha
            if str.isalpha(user_input):
                # input is right letter and update letters_guessed. 
                letters_guessed += user_input
                # when the letter is in the secret word, print good guess
                if is_word_guessed(user_input, secret_word):                    
                    print("Good guess:", get_guessed_word(secret_word, letters_guessed))
                elif(is_word_guessed(user_input, vowels)):
                    remaining_guess -= 2
                    print("Oops! That vowel letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
                else:
                    remaining_guess -= 1
                    print("Oops! That Consonants letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
            # input is not letter
            else:
                warnings -= 1
                if warnings <= 0:
                    remaining_guess -= 1
                    print("Oops! You've already guessed that letter. You have no warnings left:", get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! You've already guessed that letter. You have", warnings, "warnings left:", get_guessed_word(secret_word, letters_guessed))
            print("---------------------------------------")
            unique_letters = secret_word[0]
            for m in secret_word:
                flag = True
                for n in unique_letters:
                    if m == n:
                        flag = False
                        break
                if flag:
                    unique_letters += m                
            if is_word_guessed(secret_word, letters_guessed):   
                score = remaining_guess * len(unique_letters)
                print("Congratulations, you won!")
                print("Your total score for this game is:",score)
                lose = False
                break
    if lose:
        print("Sorry, you ran out of guesses. The word was",secret_word,".")


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # secret_word = 'slovet'
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
