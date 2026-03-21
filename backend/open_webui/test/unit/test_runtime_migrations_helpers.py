from open_webui.runtime_migrations import (
    _extract_note_content,
    _extract_oauth_sub,
    _extract_text_content,
    _extract_usage_tokens,
    _merge_meta,
)


def test_extract_oauth_sub_prefers_oidc():
    oauth = {
        "github": {"sub": "gh-1"},
        "oidc": {"sub": "oidc-1"},
    }
    assert _extract_oauth_sub(oauth) == "oidc@oidc-1"


def test_extract_note_content_prefers_markdown():
    data = {"content": {"md": "hello markdown"}}
    assert _extract_note_content(data) == "hello markdown"


def test_extract_text_content_flattens_nested_blocks():
    content = [
        {"type": "text", "text": "hello"},
        {"content": {"md": "world"}},
    ]
    assert _extract_text_content(content) == "hello\nworld"


def test_extract_usage_tokens_supports_multiple_shapes():
    usage = {"input_tokens": "12", "output_tokens": 34}
    assert _extract_usage_tokens(usage) == (12, 34)


def test_merge_meta_keeps_existing_and_adds_source_payload():
    merged = _merge_meta({"foo": "bar"}, {"raw_content": {"text": "hello"}})
    assert merged["foo"] == "bar"
    assert merged["halo_migrated_from_openwebui"]["raw_content"] == {"text": "hello"}
