from typing import List

from .utils import remove_dups, split_tokens
from .completer import TagCompleter

DEFAULT_CATEGORIES = [
    "headers",
    "style",
    "subject",
    "pov",
    "footers"
]


def categorize_tokens(prompt_tokens: List[str],
                      completer: TagCompleter,
                      category_list: List[str]) -> List[str]:
    """Handle categorization of tokens

    This function takes user input per category, adds it to a final list of
    tokens, then appends any prompt tokens that weren't already specified

    Args:
        prompt_tokens (List[str]): Tokens specified in the prompt (if any)

    Returns:
        List[str]: Categorized tokens
    """
    categories: List[str] = DEFAULT_CATEGORIES.copy()
    if category_list:
        categories = category_list
    final_tokens: List[str] = []

    print("Categorize your tokens (separated by commas):")
    for cat in categories:
        tokens_str: str = ""
        # tokens specified per category
        category_tokens: List[str] = []

        try:
            tokens_str = input(f"{cat}? ")
            if not tokens_str:
                raise EOFError()
        except EOFError:
            continue
        except KeyboardInterrupt:
            break

        # If there's a comma, multiple tokens were specified
        # else, there must be a single token
        if "," in tokens_str:
            # Split the keywords and remove duplicates
            category_tokens.extend(remove_dups(split_tokens(tokens_str)))
        elif len(tokens_str) != 0:
            category_tokens.append(tokens_str)

        category_tokens[-1] = "\n" + category_tokens[-1]

        completer.remove_tokens(category_tokens)

        final_tokens.extend(category_tokens)

    # Add prompt_tokens to the end of final_tokens, skipping duplicates
    for p_token in prompt_tokens:
        if p_token not in final_tokens:
            final_tokens.append(p_token)

    return final_tokens
