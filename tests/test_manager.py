"""Manager helper logic + the removed unsolicited-DM surface."""
import pytest

import facebook_api
from _fakes import FakeResponse
from conftest import FAKE_CLIENT_ID, FAKE_PAGE_ID
from manager import Manager

# (method name, args, expected HTTP method, expected endpoint suffix) for every
# thin pass-through on Manager — confirms each one actually reaches the Graph
# API through FacebookAPI rather than just not crashing.
_PROXY_CASES = [
    ("post_to_facebook", ("hi",), "POST", f"{FAKE_PAGE_ID}/feed"),
    ("reply_to_comment", ("p1", "c1", "hi"), "POST", "c1/comments"),
    ("get_page_posts", (), "GET", f"{FAKE_PAGE_ID}/posts"),
    ("get_post_comments", ("p1",), "GET", "p1/comments"),
    ("delete_post", ("p1",), "DELETE", "p1"),
    ("delete_comment", ("c1",), "DELETE", "c1"),
    ("hide_comment", ("c1",), "POST", "c1"),
    ("unhide_comment", ("c1",), "POST", "c1"),
    ("delete_comment_from_post", ("p1", "c1"), "DELETE", "c1"),
    ("get_number_of_comments", ("p1",), "GET", "p1/comments"),
    ("get_post_impressions", ("p1",), "GET", "p1/insights"),
    ("get_post_impressions_unique", ("p1",), "GET", "p1/insights"),
    ("get_post_impressions_paid", ("p1",), "GET", "p1/insights"),
    ("get_post_impressions_organic", ("p1",), "GET", "p1/insights"),
    ("get_post_engaged_users", ("p1",), "GET", "p1/insights"),
    ("get_post_clicks", ("p1",), "GET", "p1/insights"),
    ("get_post_reactions_like_total", ("p1",), "GET", "p1/insights"),
    ("get_post_reactions_love_total", ("p1",), "GET", "p1/insights"),
    ("get_post_reactions_wow_total", ("p1",), "GET", "p1/insights"),
    ("get_post_reactions_haha_total", ("p1",), "GET", "p1/insights"),
    ("get_post_reactions_sorry_total", ("p1",), "GET", "p1/insights"),
    ("get_post_reactions_anger_total", ("p1",), "GET", "p1/insights"),
    ("post_image_to_facebook", ("https://img/x.jpg", "cap"), "POST", f"{FAKE_PAGE_ID}/photos"),
    ("update_post", ("p1", "new"), "POST", "p1"),
    ("schedule_post", ("hi", 123), "POST", f"{FAKE_PAGE_ID}/feed"),
    ("get_page_fan_count", (), "GET", FAKE_PAGE_ID),
    ("get_post_share_count", ("p1",), "GET", "p1"),
    ("get_comment_replies", ("c1",), "GET", "c1/comments"),
    ("get_post_permalink", ("p1",), "GET", "p1"),
    ("get_scheduled_posts", (), "GET", f"{FAKE_PAGE_ID}/scheduled_posts"),
    ("get_page_info", (), "GET", FAKE_PAGE_ID),
]


@pytest.mark.parametrize("method,args,http_method,endpoint_suffix", _PROXY_CASES)
def test_proxy_method_reaches_graph_api(clients_file, stub, method, args, http_method, endpoint_suffix):
    m = Manager(FAKE_CLIENT_ID)
    getattr(m, method)(*args)
    call = stub["calls"][0]
    assert call["method"] == http_method
    assert call["url"].endswith(f"/{endpoint_suffix}")


def test_get_number_of_likes(clients_file, stub):
    stub["queue"].append(FakeResponse({"likes": {"summary": {"total_count": 7}}}))
    m = Manager(FAKE_CLIENT_ID)
    assert m.get_number_of_likes("p1") == 7


def test_get_post_insights_requests_all_metrics(clients_file, stub):
    m = Manager(FAKE_CLIENT_ID)
    m.get_post_insights("p1")
    assert stub["calls"][0]["params"]["metric"].count(",") == 11  # 12 metrics


def test_bulk_delete_comments(clients_file, stub):
    m = Manager(FAKE_CLIENT_ID)
    results = m.bulk_delete_comments(["c1", "c2"])
    assert [r["comment_id"] for r in results] == ["c1", "c2"]
    assert len(stub["calls"]) == 2


def test_bulk_hide_comments(clients_file, stub):
    m = Manager(FAKE_CLIENT_ID)
    results = m.bulk_hide_comments(["c1", "c2"])
    assert [r["comment_id"] for r in results] == ["c1", "c2"]
    assert all(call["params"].get("is_hidden") is True for call in stub["calls"])


def test_bulk_unhide_comments(clients_file, stub):
    m = Manager(FAKE_CLIENT_ID)
    results = m.bulk_unhide_comments(["c1", "c2"])
    assert [r["comment_id"] for r in results] == ["c1", "c2"]
    assert all(call["params"].get("is_hidden") is False for call in stub["calls"])


def test_filter_negative_comments(clients_file):
    m = Manager(FAKE_CLIENT_ID)
    comments = {"data": [
        {"message": "esto es terrible"},   # 'terrible'
        {"message": "great product"},      # clean
        {"message": "I hate it"},          # 'hate'
    ]}
    flagged = m.filter_negative_comments(comments)
    assert len(flagged) == 2


def test_top_commenters_ranking(clients_file, monkeypatch):
    m = Manager(FAKE_CLIENT_ID)
    monkeypatch.setattr(m, "get_post_comments", lambda pid: {"data": [
        {"from": {"id": "u1"}}, {"from": {"id": "u1"}}, {"from": {"id": "u2"}}]})
    ranked = m.get_post_top_commenters("p1")
    assert ranked[0] == {"user_id": "u1", "count": 2}
    assert ranked[1] == {"user_id": "u2", "count": 1}


def test_reactions_breakdown(clients_file, stub):
    m = Manager(FAKE_CLIENT_ID)
    stub["queue"].append(FakeResponse({"data": [
        {"name": "post_reactions_like_total", "values": [{"value": 12}]},
        {"name": "post_reactions_love_total", "values": [{"value": 3}]},
    ]}))
    out = m.get_post_reactions_breakdown("p1")
    assert out["post_reactions_like_total"] == 12
    assert out["post_reactions_love_total"] == 3


def test_unsolicited_dm_tool_removed():
    # Meta policy: unsolicited DMs are not exposed. The surface must be gone.
    assert not hasattr(Manager, "send_dm_to_user")
    assert not hasattr(facebook_api.FacebookAPI, "send_dm_to_user")
