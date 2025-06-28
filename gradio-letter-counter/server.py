from mcp.server.fastmcp import FastMCP
from typing import Optional

# Create the MCP server
mcp = FastMCP(name="Letter Counter MCP Server")

def letter_counter(word: str, letter: str) -> int:
    """Count the occurrences of a specific letter in a word.
    
    Args:
        word: The word or phrase to analyze
        letter: The letter to count occurrences of
        
    Returns:
        The number of times the letter appears in the word
    """
    return word.lower().count(letter.lower())

@mcp.tool()
def count_letter_in_word(word: str, letter: str) -> dict:
    """Count how many times a specific letter appears in a word or phrase.
    
    Args:
        word: The word or phrase to analyze
        letter: The letter to count (single character)
        
    Returns:
        Dictionary with the word, letter, and count
    """
    if len(letter) != 1:
        return {"error": "Letter must be a single character"}
    
    count = letter_counter(word, letter)
    return {
        "word": word,
        "letter": letter,
        "count": count,
        "message": f"The letter '{letter}' appears {count} time(s) in '{word}'"
    }

@mcp.resource("letter-counter://stats/{word}")
def get_word_stats(word: str) -> dict:
    """Get statistics about all letters in a word.
    
    Args:
        word: The word to analyze
        
    Returns:
        Dictionary with letter frequency statistics
    """
    letter_counts = {}
    for letter in word.lower():
        if letter.isalpha():
            letter_counts[letter] = letter_counts.get(letter, 0) + 1
    
    return {
        "word": word,
        "total_letters": len([c for c in word if c.isalpha()]),
        "unique_letters": len(letter_counts),
        "letter_counts": letter_counts
    }

if __name__ == "__main__":
    print(f"\n--- Starting {mcp} via __main__ ---")
    mcp.run() 