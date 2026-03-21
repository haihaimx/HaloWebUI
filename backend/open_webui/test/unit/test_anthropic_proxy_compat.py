import pathlib
import sys


# Ensure `open_webui` is importable when running tests from repo root.
_BACKEND_DIR = pathlib.Path(__file__).resolve().parents[3]
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from open_webui.routers import anthropic


def test_resolve_thinking_payload_requires_explicit_opt_in():
    thinking, budget, enabled = anthropic._resolve_thinking_payload(
        {}, max_tokens=1024
    )
    assert thinking is None
    assert budget is None
    assert enabled is False

    thinking, budget, enabled = anthropic._resolve_thinking_payload(
        {"thinking": {"type": "enabled"}}, max_tokens=1024
    )
    assert thinking == {"type": "enabled", "budget_tokens": 1023}
    assert budget == 1023
    assert enabled is True

    thinking, budget, enabled = anthropic._resolve_thinking_payload(
        {"reasoning_effort": "minimal"}, max_tokens=1024
    )
    assert thinking == {"type": "enabled", "budget_tokens": 1023}
    assert budget == 1023
    assert enabled is True


def test_resolve_thinking_payload_none_max_tokens():
    """When user doesn't set max_tokens, it should use 128000 as ceiling."""
    thinking, budget, enabled = anthropic._resolve_thinking_payload(
        {}, max_tokens=None
    )
    assert thinking is None
    assert budget is None
    assert enabled is False

    thinking, budget, enabled = anthropic._resolve_thinking_payload(
        {"thinking": {"type": "enabled"}}, max_tokens=None
    )
    assert thinking == {"type": "enabled", "budget_tokens": 10240}
    assert budget == 10240
    assert enabled is True

    thinking, budget, enabled = anthropic._resolve_thinking_payload(
        {"reasoning_effort": "minimal"}, max_tokens=None
    )
    assert thinking == {"type": "enabled", "budget_tokens": 1024}
    assert budget == 1024
    assert enabled is True


def test_is_anyrouter_base_url():
    assert anthropic._is_anyrouter_base_url("https://anyrouter.top/v1") is True
    assert anthropic._is_anyrouter_base_url("https://api.anthropic.com/v1") is False


def test_needs_anyrouter_opus_cc_signature():
    assert (
        anthropic._needs_anyrouter_opus_cc_signature(
            "https://anyrouter.top/v1", "claude-opus-4-6"
        )
        is True
    )
    assert (
        anthropic._needs_anyrouter_opus_cc_signature(
            "https://anyrouter.top/v1", "claude-sonnet-4-6"
        )
        is False
    )
    assert (
        anthropic._needs_anyrouter_opus_cc_signature(
            "https://api.anthropic.com/v1", "claude-opus-4-6"
        )
        is False
    )


def test_resolve_proxy_model_alias_keeps_anyrouter_opus_short_alias():
    assert (
        anthropic._resolve_proxy_model_alias(
            "claude-opus-4-6", "https://anyrouter.top/v1"
        )
        == "claude-opus-4-6"
    )


def test_resolve_proxy_model_alias_maps_other_proxies():
    assert (
        anthropic._resolve_proxy_model_alias(
            "claude-opus-4-6", "https://proxy.example.com/v1"
        )
        == "claude-opus-4-6-20250918"
    )


def test_ensure_anyrouter_opus_system_signature_injects_when_missing():
    out = anthropic._ensure_anyrouter_opus_system_signature(None)

    assert out[0]["text"] == "You are a Claude agent, built on Anthropic's Claude Agent SDK."
    assert out[1]["text"] == "Follow the user instructions."


def test_ensure_anyrouter_opus_system_signature_preserves_existing_and_reorders():
    src = [
        {"type": "text", "text": "x-anthropic-billing-header: cc_version=2.1.63;"},
        {"type": "text", "text": "Use concise answers."},
        {"type": "text", "text": "Extra context."},
    ]
    out = anthropic._ensure_anyrouter_opus_system_signature(src)

    assert out[0]["text"] == "You are a Claude agent, built on Anthropic's Claude Agent SDK."
    assert out[1]["text"] == "x-anthropic-billing-header: cc_version=2.1.63;"
    assert out[2]["text"] == "Use concise answers."
    assert out[3]["text"] == "Extra context."
