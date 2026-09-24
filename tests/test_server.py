"""MCP tool registration and the list_clients discovery tool."""
import asyncio
from unittest.mock import MagicMock, patch

import pytest

import server
from conftest import FAKE_CLIENT_ID

# (tool function, args, manager method, expected call args) for every tool that
# delegates to Manager(client_id) — confirms each tool wires client_id and its
# other arguments through to the right Manager method.
_DELEGATION_CASES = [
    (server.post_to_facebook, (FAKE_CLIENT_ID, "hi"), "post_to_facebook", ("hi",)),
    (server.reply_to_comment, (FAKE_CLIENT_ID, "p1", "c1", "hi"), "reply_to_comment", ("p1", "c1", "hi")),
    (server.get_page_posts, (FAKE_CLIENT_ID,), "get_page_posts", ()),
    (server.get_post_comments, (FAKE_CLIENT_ID, "p1"), "get_post_comments", ("p1",)),
    (server.delete_post, (FAKE_CLIENT_ID, "p1"), "delete_post", ("p1",)),
    (server.delete_comment, (FAKE_CLIENT_ID, "c1"), "delete_comment", ("c1",)),
    (server.hide_comment, (FAKE_CLIENT_ID, "c1"), "hide_comment", ("c1",)),
    (server.unhide_comment, (FAKE_CLIENT_ID, "c1"), "unhide_comment", ("c1",)),
    (server.delete_comment_from_post, (FAKE_CLIENT_ID, "p1", "c1"), "delete_comment_from_post", ("p1", "c1")),
    (server.filter_negative_comments, (FAKE_CLIENT_ID, {"data": []}), "filter_negative_comments", ({"data": []},)),
    (server.get_number_of_comments, (FAKE_CLIENT_ID, "p1"), "get_number_of_comments", ("p1",)),
    (server.get_number_of_likes, (FAKE_CLIENT_ID, "p1"), "get_number_of_likes", ("p1",)),
    (server.get_post_insights, (FAKE_CLIENT_ID, "p1"), "get_post_insights", ("p1",)),
    (server.get_post_impressions, (FAKE_CLIENT_ID, "p1"), "get_post_impressions", ("p1",)),
    (server.get_post_impressions_unique, (FAKE_CLIENT_ID, "p1"), "get_post_impressions_unique", ("p1",)),
    (server.get_post_impressions_paid, (FAKE_CLIENT_ID, "p1"), "get_post_impressions_paid", ("p1",)),
    (server.get_post_impressions_organic, (FAKE_CLIENT_ID, "p1"), "get_post_impressions_organic", ("p1",)),
    (server.get_post_engaged_users, (FAKE_CLIENT_ID, "p1"), "get_post_engaged_users", ("p1",)),
    (server.get_post_clicks, (FAKE_CLIENT_ID, "p1"), "get_post_clicks", ("p1",)),
    (server.get_post_reactions_like_total, (FAKE_CLIENT_ID, "p1"), "get_post_reactions_like_total", ("p1",)),
    (server.get_post_reactions_love_total, (FAKE_CLIENT_ID, "p1"), "get_post_reactions_love_total", ("p1",)),
    (server.get_post_reactions_wow_total, (FAKE_CLIENT_ID, "p1"), "get_post_reactions_wow_total", ("p1",)),
    (server.get_post_reactions_haha_total, (FAKE_CLIENT_ID, "p1"), "get_post_reactions_haha_total", ("p1",)),
    (server.get_post_reactions_sorry_total, (FAKE_CLIENT_ID, "p1"), "get_post_reactions_sorry_total", ("p1",)),
    (server.get_post_reactions_anger_total, (FAKE_CLIENT_ID, "p1"), "get_post_reactions_anger_total", ("p1",)),
    (server.get_post_top_commenters, (FAKE_CLIENT_ID, "p1"), "get_post_top_commenters", ("p1",)),
    (server.post_image_to_facebook, (FAKE_CLIENT_ID, "https://img/x.jpg", "cap"), "post_image_to_facebook", ("https://img/x.jpg", "cap")),
    (server.update_post, (FAKE_CLIENT_ID, "p1", "new"), "update_post", ("p1", "new")),
    (server.schedule_post, (FAKE_CLIENT_ID, "hi", 123), "schedule_post", ("hi", 123)),
    (server.get_page_fan_count, (FAKE_CLIENT_ID,), "get_page_fan_count", ()),
    (server.get_post_share_count, (FAKE_CLIENT_ID, "p1"), "get_post_share_count", ("p1",)),
    (server.get_post_reactions_breakdown, (FAKE_CLIENT_ID, "p1"), "get_post_reactions_breakdown", ("p1",)),
    (server.bulk_delete_comments, (FAKE_CLIENT_ID, ["c1", "c2"]), "bulk_delete_comments", (["c1", "c2"],)),
    (server.bulk_hide_comments, (FAKE_CLIENT_ID, ["c1", "c2"]), "bulk_hide_comments", (["c1", "c2"],)),
    (server.bulk_unhide_comments, (FAKE_CLIENT_ID, ["c1", "c2"]), "bulk_unhide_comments", (["c1", "c2"],)),
    (server.get_comment_replies, (FAKE_CLIENT_ID, "c1"), "get_comment_replies", ("c1",)),
    (server.get_post_permalink, (FAKE_CLIENT_ID, "p1"), "get_post_permalink", ("p1",)),
    (server.get_scheduled_posts, (FAKE_CLIENT_ID,), "get_scheduled_posts", ()),
    (server.get_page_info, (FAKE_CLIENT_ID,), "get_page_info", ()),
]


def _tool_names() -> set[str]:
    tools = asyncio.run(server.mcp.list_tools())
    return {t.name for t in tools}


def test_send_dm_to_user_not_registered():
    # Meta policy: unsolicited DMs are not exposed as a tool.
    assert "send_dm_to_user" not in _tool_names()


def test_every_tool_except_list_clients_takes_client_id():
    tools = asyncio.run(server.mcp.list_tools())
    for tool in tools:
        if tool.name == "list_clients":
            continue
        properties = tool.inputSchema.get("properties", {})
        assert "client_id" in properties, f"{tool.name} is missing client_id"


def test_list_clients_returns_configured_slugs(clients_file):
    assert server.list_clients() == [FAKE_CLIENT_ID]


@pytest.mark.parametrize("tool_fn,call_args,manager_method,expected_args", _DELEGATION_CASES)
def test_tool_delegates_to_manager(tool_fn, call_args, manager_method, expected_args):
    mock_manager = MagicMock()
    with patch("server.Manager", return_value=mock_manager) as mock_manager_cls:
        tool_fn(*call_args)
    mock_manager_cls.assert_called_once_with(FAKE_CLIENT_ID)
    getattr(mock_manager, manager_method).assert_called_once_with(*expected_args)
