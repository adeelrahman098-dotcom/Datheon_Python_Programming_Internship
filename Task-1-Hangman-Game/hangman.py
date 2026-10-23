import random
import sys
from pathlib import Path

HANGMAN_STAGES = [
    """
     +---+
         |
         |
         |
        ===
    """,
    """
     +---+
     O   |
         |
         |
        ===
    """,
    """
     +---+
     O   |
     |   |
         |
        ===
    """,
    """
     +---+
     O   |
    /|   |
         |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
         |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
    /    |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
    / \\  |
        ===
    """
]

# Fallback dataset if words.txt is not found
FALLBACK_WORDS = [
    ("animal", "python"),
    ("technology", "computer"),
    ("fruit", "banana"),
    ("country", "canada")
]

def load_words_from_file(filename="words.txt"):
    """
    Loads category-word pairs from words.txt.
    Expected line format: category:word
    """
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / filename
    word_list = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    cat, word = line.strip().split(":", 1)
                    cat = cat.strip().lower()
                    word = word.strip().lower()
                    if cat and word.isalpha():
                        word_list.append((cat, word))
        if word_list:
            return word_list
    except FileNotFoundError:
        print(f"⚠️ Note: '{filename}' not found. Using default word pool.")
    except Exception as e:
        print(f"⚠️ Error reading '{filename}': {e}. Using default word pool.")
    
    return FALLBACK_WORDS

def display_word(secret_word, guessed_letters):
    return " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )

def play_game():
    word_pool = load_words_from_file("words.txt")
    
    # Randomly select a tuple of (category, secret_word)
    category, secret_word = random.choice(word_pool)
    
    guessed_letters = set()
    wrong_guesses = 0
    max_attempts = 6

    print("\n================================")
    print("      WELCOME TO HANGMAN        ")
    print("================================")
    print(f"💡 CLUE / CATEGORY: {category.upper()}")

    while wrong_guesses < max_attempts:
        print(HANGMAN_STAGES[wrong_guesses])
        print("Word:", display_word(secret_word, guessed_letters))
        print("Guessed letters:", " ".join(sorted(guessed_letters)) or "None")
        print("Attempts remaining:", max_attempts - wrong_guesses)

        guess = input("Guess one letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("❌ Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("⚠️ You already guessed that letter. Try another.")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print("✅ Correct guess!")
        else:
            wrong_guesses += 1
            print("❌ Wrong guess!")

        if all(letter in guessed_letters for letter in secret_word):
            print(f"\n🎉 Congratulations! You won! The word was: {secret_word}")
            return

    print(HANGMAN_STAGES[max_attempts])
    print(f"\n💀 Game over! You lost. The word was: {secret_word}")


if __name__ == "__main__":
    while True:
        play_game()
        replay = input("\nWould you like to play again? (y/n): ").strip().lower()
        if replay != 'y':
            print("Thanks for playing!")
            break