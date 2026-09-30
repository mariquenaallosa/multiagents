"""Text chunking and front matter parsing for the ingestion pipeline."""


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Split a markdown document into its `key: value` front matter and its body."""
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        key, separator, value = line.partition(":")
        if separator:
            metadata[key.strip()] = value.strip()
    return metadata, text[end + len("\n---\n"):].lstrip("\n")


def chunk_text(text: str, max_chars: int = 800, overlap: int = 100) -> list[str]:
    """Group paragraphs into chunks of at most `max_chars`, repeating a tail of `overlap` chars."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    pieces: list[str] = []
    for paragraph in paragraphs:
        while len(paragraph) > max_chars:
            pieces.append(paragraph[:max_chars])
            paragraph = paragraph[max_chars:]
        pieces.append(paragraph)

    chunks: list[str] = []
    current = ""
    for piece in pieces:
        candidate = f"{current}\n\n{piece}" if current else piece
        if len(candidate) <= max_chars:
            current = candidate
            continue
        chunks.append(current)
        tail = current[-overlap:] if overlap else ""
        current = f"{tail}\n\n{piece}" if tail else piece
        if len(current) > max_chars:
            current = piece

    if current:
        chunks.append(current)
    return chunks
