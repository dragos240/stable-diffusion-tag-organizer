#!/usr/bin/env python3
import sys
from typing import Dict, List


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

        if paren_depth == 0 and bracket_depth == 0 and c == ",":
            # If we are not within any parentheses or square brackets and
            # encounter a comma, add the current token to the list
            tokens.append(current_token.strip())
            current_token = ""
        else:
            # Build the current token by appending the characters
            current_token += c

    tokens.append(current_token.strip())

    return tokens


def order_tokens(tokens: List[str]) -> List[str]:
    """Order tokens by category into a single List

    Args:
        tokens (List[str]): Tokens

    Returns:
        List[str]: Ordered tokens
    """
    categories: Dict[str, List[str]] = {
        "headers": [],
        "artist": [],
        "style": [],
        "subject": [],
        "subject_pose": [],
        "subject_other": [],
        "scene": [],
        "view": [],
        "lighting": [],
        "footers": []
    }

    for idx, token in enumerate(tokens):
        print(idx + 1, token)

    print("Choose your categories (separated by spaces):")
    for key in categories.keys():
        tids: str = ""
        vals: List[int] = []
        try:
            while True:
                tids = input(f"{key}? ")
                if not tids:
                    break
                if " " not in tids:
                    if int(tids) == 0:
                        print("Invalid token number, try again")
                        continue
                    vals = [tokens[int(tids) - 1]]
                else:
                    vals = [tokens[int(tid) - 1] for tid in tids.split()]
                    if -1 in vals:
                        print("Invalid token number, try again")
                        continue
                categories[key].extend(vals)
                break
        except ValueError:
            print("Not a list of numbers, try again")

    ordered_tokens = []
    for k, v in categories.items():
        # Skip categories that have no tokens
        if not categories[k]:
            continue
        # Extend the ordered_tokens list with the tokens in the current category
        ordered_tokens.extend(v)

    return ordered_tokens


def main():
    if len(sys.argv) < 2:
        print("Syntax: PATH/TO/OUTPUT/FILE")
        return

    output_path = sys.argv[1]

    print("(Use Ctrl+C or Ctrl+D to quit)")
    while True:
        try:
            prompt = input("(prompt): ")
            tokens = split_tokens(prompt)
            tokens = order_tokens(tokens)

            with open(output_path, 'w') as f:
                print(type(tokens))
                f.write(", ".join(tokens))
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == '__main__':
    main()
