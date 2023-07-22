from typing import List


def split_tokens(prompt: str) -> List[str]:
    """
    Separates top-level tokens from the input string.

    Top-level tokens are separated by commas (',') and are not nested within
    parentheses or brackets.

    Args:
        prompt (str): The input string containing the tokens.

    Returns:
        list: A list of top-level tokens.

    Examples:
        >>> prompt = "Zootopia, solo (((nick wilde))) with ((neck tuft))"
        >>> separate_tokens(prompt)
        ['Zootopia', 'solo (((nick wilde))) with ((neck tuft))']
    """
    # Stored tokens
    tokens = []
    # Current token being processed
    current_token = ""
    # How deep we are into parenthesis
    paren_depth = 0
    # How deep we are into brackets
    bracket_depth = 0

    for c in prompt:
        if c == "(":
            paren_depth += 1
        elif c == ")":
            paren_depth -= 1
        elif c == "[":
            bracket_depth += 1
        elif c == "]":
            bracket_depth -= 1

        if paren_depth == 0 \
                and bracket_depth == 0 \
                and c == ",":
            # If we are not within any parentheses or square brackets and
            # encounter a comma, add the current token to the list
            tokens.append(current_token.strip())
            current_token = ""
        else:
            # Build the current token by appending the characters
            current_token += c

    tokens.append(current_token.strip())

    return tokens


def print_token_list(tokens: List[str]):
    """Prints given tokens, numbering them as it does

    Args:
        tokens (List[str]): Tokens to print
    """
    for idx, token in enumerate(tokens):
        print(f"{idx + 1}. {token}")


def remove_dups(tokens: List[str]) -> List[str]:
    """Remove duplicate tokens if they exist

    Args:
        tokens (List[str]): List of tokens to parse

    Returns:
        List[str]: Pruned tokens
    """
    ALLOWED_KEYWORDS = [
        "BREAK"
    ]
    pruned_tokens = []

    for token in tokens:
        if token not in pruned_tokens \
                or token in ALLOWED_KEYWORDS:
            pruned_tokens.append(token)

    return pruned_tokens
