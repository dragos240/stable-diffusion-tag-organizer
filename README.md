# stable-diffusion-tag-organizer

> **Note**: This tool is very WIP, so don't be suprised if it doesn't work perfectly.

Stable Diffusion Tag Organizer is a tool for categorization and general management of Stable Diffusion .

## What this tool does

This tool accepts an optional prompt, which will then be deconstructed into tokens. These tokens can then be sorted into the following categories:

- Headers
- Artist
- Style
- Subject
- Subject pose
- Subject other
- Scene
- View
- Lighting
- Footers

These categories determine the order of the tokens in the final prompt.

## How to use this tool

The tool takes a path to a text file as its only argument. The rest of the tool is interactive.

```
$ ./categorize-tokens.py PATH/TO/OUTPUT
(Use Ctrl+C to quit at any time)
(prompt): woman with a hat at the beach, beach, woman, ((masterpiece))
1 ((masterpiece))
2 beach
3 woman
4 woman with a hat at the beach
Tokens sorted, categorize? (Y/n): y
Categorize your tokens (separated by commas):
headers? woman
artist? woman with a hat at the beach
style?
subject?
subject_pose? standing
subject_other?
scene?
view?
lighting?
footers? ((masterpiece))
```

You can either use tab completion to enter values from the given prompt or you can use custom tokens. Each token must be separated by a comma.