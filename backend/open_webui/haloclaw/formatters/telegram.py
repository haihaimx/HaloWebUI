"""Convert markdown-formatted LLM output to Telegram-safe HTML."""

import re

# Telegram supports: <b>, <i>, <u>, <s>, <code>, <pre>, <a>, <tg-spoiler>
# Max message length: 4096 characters

MAX_MESSAGE_LENGTH = 4096


def markdown_to_telegram_html(text: str) -> str:
    """Convert common markdown to Telegram HTML parse mode.

    Handles: bold, italic, strikethrough, code, code blocks, links.
    Strips unsupported elements gracefully.
    """
    # Escape HTML entities first (before we add our own tags)
    text = _escape_html(text)

    # Code blocks (``` ... ```) — must be before inline code
    text = re.sub(
        r"```(\w*)\n(.*?)```",
        lambda m: f"<pre>{m.group(2)}</pre>",
        text,
        flags=re.DOTALL,
    )

    # Inline code (`...`)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    # Bold (**...**  or __...__)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)

    # Italic (*...* or _..._) — but not inside bold tags
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)", r"<i>\1</i>", text)

    # Strikethrough (~~...~~)
    text = re.sub(r"~~(.+?)~~", r"<s>\1</s>", text)

    # Links [text](url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)

    # Headers (# ... ) — convert to bold since Telegram has no header support
    text = re.sub(r"^#{1,6}\s+(.+)$", r"<b>\1</b>", text, flags=re.MULTILINE)

    # Bullet lists (- or * at start of line) — keep as-is with bullet char
    text = re.sub(r"^[\-\*]\s+", "\u2022 ", text, flags=re.MULTILINE)

    # Numbered lists — keep as-is
    # No conversion needed, Telegram displays them fine

    return text


def _escape_html(text: str) -> str:
    """Escape HTML special chars, but preserve already-valid constructs."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def split_message(text: str) -> list[str]:
    """Split a long message into chunks that fit Telegram's 4096-char limit.

    Splits on paragraph boundaries (double newline) first, then on single
    newlines, then hard-cuts at the limit.
    """
    if len(text) <= MAX_MESSAGE_LENGTH:
        return [text]

    chunks = []
    while text:
        if len(text) <= MAX_MESSAGE_LENGTH:
            chunks.append(text)
            break

        # Try splitting at double newline
        cut = text.rfind("\n\n", 0, MAX_MESSAGE_LENGTH)
        if cut == -1:
            # Try single newline
            cut = text.rfind("\n", 0, MAX_MESSAGE_LENGTH)
        if cut == -1:
            # Hard cut
            cut = MAX_MESSAGE_LENGTH

        chunks.append(text[:cut])
        text = text[cut:].lstrip("\n")

    return chunks
