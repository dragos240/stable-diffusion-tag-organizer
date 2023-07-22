import readline
from typing import List, Optional


class TagCompleter(object):
    tokens: List[str]
    matches: List[str]

    def __init__(self, tokens: List[str]):
        readline.clear_history()
        self.tokens = tokens

    def complete(self, text: str, state: int):
        """Completion function for TagCompleter

        Args:
            text (str): The text of the input
            state (int): The index of the suggestion

        Returns:
            str: The completed text for the given state
        """
        # Make sure the text is stripped since a user may enter a space
        # after the delimiter
        text = text.strip()

        # In case tab is hit with an empty text buffer, use all tokens
        self.matches = self.tokens
        if text:
            # Check if the input text is inside any given token
            self.matches = [token
                            for token in self.tokens
                            if text in token]

        match: Optional[str] = None

        try:
            match = self.matches[state]
        except IndexError:
            pass

        return match

    def remove_tokens(self, tokens_to_remove: List[str]):
        """Removes a list of tokens if they exist from self.tokens

        Args:
            tokens_to_remove (List[str]): Tokens to remove
        """
        for token in tokens_to_remove:
            if token in self.tokens:
                self.tokens.remove(token)


def init_completer(tokens: List[str]) -> TagCompleter:
    """Initializes the completer and returns it

    Args:
        tokens (List[str]): Tokens used to initialize the completer

    Returns:
        TagCompleter: The final completer
    """
    completer = TagCompleter(tokens)
    readline.set_completer_delims(',')
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')

    return completer
