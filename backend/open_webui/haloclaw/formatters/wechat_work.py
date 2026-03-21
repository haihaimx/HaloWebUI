"""Convert markdown-formatted LLM output to WeChat Work text format.

WeChat Work text messages support plain text only (no HTML/markdown).
We convert markdown to a readable plain-text representation using
Chinese-style emphasis markers 【】 for headers/bold.
"""

import re

# WeChat Work text message max length: 2048 characters
MAX_MESSAGE_LENGTH = 2048


def markdown_to_wx_text(text: str) -> str:
    """Convert markdown to readable plain text for WeChat Work."""
    # Code blocks: preserve with ``` markers (readable in plain text)
    text = re.sub(
        r"```\w*\n(.*?)```",
        lambda m: f"```\n{m.group(1)}```",
        text,
        flags=re.DOTALL,
    )

    # Bold → Chinese emphasis markers
    text = re.sub(r"\*\*(.+?)\*\*", r"【\1】", text)
    text = re.sub(r"__(.+?)__", r"【\1】", text)

    # Italic → strip markers
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", text)
    text = re.sub(r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)", r"\1", text)

    # Strikethrough → strip markers
    text = re.sub(r"~~(.+?)~~", r"\1", text)

    # Links: [text](url) → text (url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)

    # Headers → emphasis markers
    text = re.sub(r"^#{1,6}\s+(.+)$", r"【\1】", text, flags=re.MULTILINE)

    # Bullet lists → bullet char
    text = re.sub(r"^[\-\*]\s+", "• ", text, flags=re.MULTILINE)

    return text


def split_message(text: str) -> list[str]:
    """Split a message into chunks fitting WeChat Work's 2048-char limit."""
    if len(text) <= MAX_MESSAGE_LENGTH:
        return [text]

    chunks = []
    while text:
        if len(text) <= MAX_MESSAGE_LENGTH:
            chunks.append(text)
            break

        # Try splitting at paragraph boundary
        cut = text.rfind("\n\n", 0, MAX_MESSAGE_LENGTH)
        if cut == -1:
            cut = text.rfind("\n", 0, MAX_MESSAGE_LENGTH)
        if cut == -1:
            cut = MAX_MESSAGE_LENGTH

        chunks.append(text[:cut])
        text = text[cut:].lstrip("\n")

    return chunks
