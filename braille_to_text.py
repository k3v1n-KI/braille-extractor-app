# Dictionary mapping Braille Unicode characters to English letters and numbers
braille_to_english = {
    # Letters
    '⠁': 'a', '⠃': 'b', '⠉': 'c', '⠙': 'd', '⠑': 'e',
    '⠋': 'f', '⠛': 'g', '⠓': 'h', '⠊': 'i', '⠚': 'j',
    '⠅': 'k', '⠇': 'l', '⠍': 'm', '⠝': 'n', '⠕': 'o',
    '⠏': 'p', '⠟': 'q', '⠗': 'r', '⠎': 's', '⠞': 't',
    '⠥': 'u', '⠧': 'v', '⠺': 'w', '⠭': 'x', '⠽': 'y', '⠵': 'z',
    ' ': ' ',  # Space in Braille

    # Numbers (preceded by ⠼ to indicate numbers)
    '⠼⠁': '1', '⠼⠃': '2', '⠼⠉': '3', '⠼⠙': '4', '⠼⠑': '5',
    '⠼⠋': '6', '⠼⠛': '7', '⠼⠓': '8', '⠼⠊': '9', '⠼⠚': '0',
    
    # Punctuation (basic)
    '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', ';': '⠆', ':': '⠒',
    '-': '⠤', "'": '⠄', '"': '⠶', '(': '⠷', ')': '⠾'
}

def braille_to_text(braille_text):
    english_text = ""
    i = 0
    while i < len(braille_text):
        # Check if the current character is the number indicator
        if braille_text[i] == '⠼' and i + 1 < len(braille_text):
            # Combine ⠼ with the next character to form the number
            braille_char = braille_text[i] + braille_text[i + 1]
            english_text += braille_to_english.get(braille_char, '?')
            i += 2  # Skip the next character since it's part of the number
        else:
            # Convert letters and spaces
            english_text += braille_to_english.get(braille_text[i], '?')
            i += 1
    return english_text

# # Sample Braille text: "Leaves turn brown and yellow in the fall. Add the sum to the product of these three."
# braille_text = "⠠⠇⠑⠁⠧⠑⠎ ⠞⠥⠗⠝ ⠃⠗⠕⠺⠝ ⠁⠝⠙ ⠽⠑⠇⠇⠕⠺ ⠊⠝ ⠞⠓⠑ ⠋⠁⠇⠇. ⠠⠁⠙⠙ ⠞⠓⠑ ⠎⠥⠍ ⠞⠕ ⠞⠓⠑ ⠏⠗⠕⠙⠥⠉⠞ ⠕⠋ ⠞⠓⠑⠎⠑ ⠞⠓⠗⠑⠑." 
# english_text = braille_to_text(braille_text)
# print("English text:", english_text)
