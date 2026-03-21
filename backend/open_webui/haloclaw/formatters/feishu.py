"""Convert markdown-formatted LLM output to Feishu text format.

Feishu text messages (msg_type="text") are plain text. Rich text requires
the "post" msg_type which is more complex. For now we convert markdown to
a readable plain-text representation.
"""

import re

# Practical message length limit for Feishu text messages
MAX_MESSAGE_LENGTH = 4000


def markdown_to_feishu_text(text: str) -> str:
    """Convert markdown to readable plain text for Feishu."""
    # Code blocks: preserve with ``` markers
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
    """Split a message into chunks fitting practical Feishu limit."""
    if len(text) <= MAX_MESSAGE_LENGTH:
        return [text]

    chunks = []
    while text:
        if len(text) <= MAX_MESSAGE_LENGTH:
            chunks.append(text)
            break

        cut = text.rfind("\n\n", 0, MAX_MESSAGE_LENGTH)
        if cut == -1:
            cut = text.rfind("\n", 0, MAX_MESSAGE_LENGTH)
        if cut == -1:
            cut = MAX_MESSAGE_LENGTH

        chunks.append(text[:cut])
        text = text[cut:].lstrip("\n")

    return chunks
