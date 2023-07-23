from typing import Optional
import os
import argparse

from .utils import split_tokens, print_token_list
from .completer import init_completer
from .categorize import categorize_tokens


def main():
    parser = argparse.ArgumentParser(
        description="Tool for managing tags for Stable Diffusion prompts")

    parser.add_argument("output_file",
                        help="Output file for tags",
                        type=str,
                        metavar="FILE")

    parser.add_argument("-c", "--categories",
                        help="A file containing a list of categories to use",
                        type=str,
                        metavar="PATH",
                        default=None,
                        dest="category_path")

    args = parser.parse_args()

    output_path = args.output_file
    categories: Optional[str] = []
    if args.category_path is not None:
        if os.path.exists(args.category_path):
            print("Using categories from user defined list")
            with open(args.category_path, 'r') as f:
                categories = [line.rstrip() for line in f.readlines()]

    # Use the text inside of prompt.txt if it exists in the current dir
    prompt: Optional[str] = None
    if os.path.exists("./prompt.txt"):
        with open("./prompt.txt", "r") as f:
            prompt = "".join(f.readlines())

    print("(Use Ctrl+C to quit, Tab to autocomplete)")
    try:
        tokens = []
        try:
            if prompt is None:
                prompt = input("(prompt): ").rstrip()
            tokens = split_tokens(prompt)
        except EOFError:
            # Assume user means skip prompt input
            pass

        # New list for listed tokens, to preserve original order
        listed_tokens = tokens.copy()

        # Sort the listed tokens so that it's easier to comb through
        # specified tokens
        listed_tokens.sort()

        # Print tokens
        print_token_list(listed_tokens)

        # Set up autocomplete
        completer = init_completer(tokens)

        try:
            answer = input("Tokens sorted, categorize? (Y/n): ")
            if answer.rstrip().lower() in ("y", ""):
                tokens = categorize_tokens(tokens, completer, categories)
        except KeyboardInterrupt:
            pass

        with open(output_path, 'w') as f:
            f.write(", ".join(tokens).lstrip())
    except KeyboardInterrupt:
        pass
