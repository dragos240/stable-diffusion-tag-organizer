#!/usr/bin/env python3
import sys
from typing import Dict, List, Optional
import readline
import argparse
import os


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

    # Flatten prompt
    prompt.replace("\n", "")

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
        tokens (List[str]): Tokens to parse

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


def categorize_tokens(tokens: List[str]) -> List[str]:
    """Categorize tokens by category into a List

    Args:
        tokens (List[str]): Tokens

    Returns:
        List[str]: Categorized tokens
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

    print("Categorize your tokens (separated by commas):")
    for category in categories.keys():
        tokens_input: str = ""
        section_tokens: List[str] = []

        try:
            tokens_input = input(f"{category}? ")
            if not tokens_input:
                raise EOFError()
        except EOFError:
            continue
        except KeyboardInterrupt:
            break

        # If there's a comma, multiple tokens were specified
        # Else, there must be a single token
        if "," in tokens_input:
            # Split the keywords and remove duplicates
            section_tokens.extend(remove_dups(split_tokens(tokens_input)))
        else:
            section_tokens.append(tokens_input)

    categorized_tokens = tokens.copy()
    for vals in categories.values():
        categorized_tokens.extend(vals)

    return categorized_tokens


class TagCompleter(object):
    tags: List[str]
    matches: List[str]

    def __init__(self, tags: List[str]):
        self.tags = tags

    def complete(self, text: str, state: int):
        tokens = [token.rstrip()
                  for token in text.split(",")]
        last_token = tokens[-1]

        if state == 0:
            if not text:
                # If tab is hit with an empty text buffer
                self.matches = self.tags
            else:
                self.matches = [tag
                                for tag in self.tags
                                if tag.startswith(last_token)]

        try:
            return self.matches[state]
        except IndexError:
            return None

    def display_matches(self,
                        substitution: str,
                        matches: List[str],
                        longest_match_length: int):
        line_buffer = readline.get_line_buffer()

        print()

        for match in matches:
            print(match)

        print(f"> {line_buffer}", end="")
        sys.stdout.flush()


def set_completer(tokens: List[str]):
    completer = TagCompleter(tokens)
    readline.set_completer_delims(',')
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')
    readline.set_completion_display_matches_hook(
        completer.display_matches)


def main():
    parser = argparse.ArgumentParser(
        description="Tool for managing tags for Stable Diffusion prompts")

    parser.add_argument("output_file",
                        help="Output file for tags",
                        type=str,
                        metavar="FILE")

    args = parser.parse_args()

    output_path = args.output_file

    prompt: Optional[str] = None
    if os.path.exists("./prompt.txt"):
        with open("./prompt.txt", "r") as f:
            prompt = "".join(f.readlines())
    print("(Use Ctrl+C to quit at any time)")
    while True:
        try:
            tokens = []
            try:
                if prompt is None:
                    prompt = input("(prompt): ").rstrip()
                tokens = split_tokens(prompt)
            except EOFError:
                # Assume user means skip prompt input
                pass

            # Sort the tokens before printing them
            tokens.sort()

            # Print tokens
            print_token_list(tokens)

            # Set up autocomplete
            set_completer(tokens)

            answer = input("Tokens sorted, categorize? (Y/n): ")
            if answer.rstrip().lower() in ("y", ""):
                tokens = categorize_tokens(tokens)

            with open(output_path, 'w') as f:
                f.write(", ".join(tokens))
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
