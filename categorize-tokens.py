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

    tokens.sort()

    for idx, token in enumerate(tokens):
        print(idx + 1, token)

    answer = input("Tokens sorted, categorize? (Y/n): ")
    if answer.rstrip().lower() not in ("y", ""):
        return tokens

    print("Categorize your tokens (separated by commas):")
    for key in categories.keys():
        keywords: str = ""
        keyword_list: List[str] = []
        while True:
            try:
                keywords = input(f"{key}? ")
                if not keywords:
                    raise Exception()
            except (EOFError, Exception):
                break
            if " " not in keywords:
                if type(keywords) is int:
                    if keywords == 0:
                        print("Invalid token number, try again")
                        continue
                    keyword_list = [tokens[int(keywords) - 1]]
                elif type(keywords) is str:
                    keyword_list = [keywords]
            else:
                split_keywords = keywords.split()
                for keyword in split_keywords:
                    try:
                        keyword = int(keyword) - 1
                        if keyword == -1:
                            print("Invalid token number, try again")
                            continue
                        keyword_list.append(tokens[keyword])
                    except ValueError:
                        keyword_list.append(keyword)
            categories[key].extend(keyword_list)
            break

    ordered_tokens = []
    for k, v in categories.items():
        # Skip categories that have no tokens
        if not categories[k]:
            continue
        # Extend the ordered_tokens list with the tokens in the current
        # category
        ordered_tokens.extend(v)

    return ordered_tokens


def main():
    if len(sys.argv) < 2:
        print("Syntax: PATH/TO/OUTPUT/FILE")
        return

    output_path = sys.argv[1]

    print("(Use Ctrl+C to quit at any time)")
    while True:
        try:
            prompt = ""
            tokens = []
            try:
                prompt = input("(prompt): ").rstrip()
                tokens = split_tokens(prompt)
            except EOFError:
                # Assume user means skip prompt input
                pass
            tokens = order_tokens(tokens)

            with open(output_path, 'w') as f:
                print(type(tokens))
                f.write(", ".join(tokens))
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
