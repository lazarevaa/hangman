# Problem Set 2, hangman.py
# Name: Lazareva Maria KM-02
# Collaborators: my brother
# Time spent: ~4 hours

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
    print("  ", len(wordlist), "words loaded.")
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
    secret_word_set = set(secret_word)
    return secret_word_set.issubset(set(letters_guessed))


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    current_guessed_word = secret_word
    for i in current_guessed_word:
        if i not in letters_guessed:
            current_guessed_word = current_guessed_word.replace(i, '_')
        else:
            current_guessed_word = current_guessed_word
    return current_guessed_word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    lowercase_letters = string.ascii_lowercase
    for i in letters_guessed:
        lowercase_letters = lowercase_letters.replace(i, '')
    return lowercase_letters


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
    user_letters, attempts, warnings, vowels = [], 6, 3, ["a", "e", "i", "o", "u"]
    print(f"I am thinking of a word that is {len(secret_word)} letters long")
    while attempts > 0 and not is_word_guessed(secret_word, user_letters):
        print(f"You have {warnings} warnings left.\n"
              f"You have {attempts} guesses left.\n"
              f"Available letters: {get_available_letters(user_letters)}")
        user_guess = input("Please guess a letter:").lower()
        if user_guess in user_letters:
            print("You already guessed this letter.")
        elif user_guess in secret_word:
            print("Wow! You guessed!")
        elif not user_guess.isalpha() or not user_guess.isascii():
            if warnings > 0:
                print("Nope! Wrong character, be careful.")
                warnings -= 1
            else:
                print("Oops! You lost all warnings. This time you lose one of your attempts!")
                attempts -= 1
        elif user_guess in vowels:
            print("Wrong vowel! You lose two attempts!")
            attempts -= 2
        else:
            print("Oh no! You failed to guess.")
            attempts -= 1
        user_letters.append(user_guess)
        print(get_guessed_word(secret_word, user_letters))
        print("")

    if not is_word_guessed(secret_word, user_letters):
        print(f'You lose. Better luck next time!\nSecret word was {secret_word}.')
    else:
        print("Congrats! You won! :)")

    score = len(set(secret_word)) * attempts
    print(f"Your score: {score}")


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
    my_word_clean = my_word.replace(' ', '')
    matching = []
    if len(my_word_clean) != len(other_word):
        return False
    for i, j in zip(my_word_clean, other_word):
        if i != '_':
            if i == j:
                matching.append(True)
            else:
                matching.append(False)
        else:
            if j not in set(my_word_clean):
                matching.append(True)
            else:
                matching.append(False)
    if set(matching) == {True}:
        return True
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
    matches_list = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            matches_list.append(word)

    if matches_list:
        for word in matches_list:
            print(word, end= ' ')
    else:
        print('No possible matches.')


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
    user_letters, attempts, warnings, vowels = [], 6, 3, ["a", "e", "i", "o", "u"]
    print(f"I am thinking of a word that is {len(secret_word)} letters long")
    while attempts > 0 and not is_word_guessed(secret_word, user_letters):
        print(f"You have {warnings} warnings left.\n"
              f"You have {attempts} guesses left.\n"
              f"Available letters: {get_available_letters(user_letters)}")
        user_guess = input("Please guess a letter:").lower()
        if user_guess == "*":
            show_possible_matches(get_guessed_word(secret_word, user_letters))
        elif user_guess in user_letters:
            print("You already guessed this letter.")
        elif user_guess in secret_word:
            print("Wow! You guessed!")
        elif not user_guess.isalpha() or not user_guess.isascii():
            if warnings > 0:
                print("Nope! Wrong character, be careful.")
                warnings -= 1
            else:
                print("Oops! You lost all warnings. This time you lose one of your attempts!")
                attempts -= 1
        elif user_guess in vowels:
            print("Wrong vowel! You lose two attempts!")
            attempts -= 2
        else:
            print("Oh no! You failed to guess.")
            attempts -= 1
        user_letters.append(user_guess)
        print(get_guessed_word(secret_word, user_letters))
        print("")

    if not is_word_guessed(secret_word, user_letters):
        print(f'You lose. Better luck next time!\nSecret word was {secret_word}.')
    else:
        print("Congrats! You won! :)")

    score = len(set(secret_word)) * attempts
    print(f"Your score: {score}")



if __name__ == "__main__":

    running = True
    while running:

        secret_word = choose_word(wordlist)
        hangman_with_hints(secret_word)

        ans = input('Do you wanna try again? y/n: ')
        if ans != 'y':
            running = False

