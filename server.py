from mcp.server.fastmcp import FastMCP
from manager import Manager
from typing import Any

mcp = FastMCP("FacebookMCP")

@mcp.tool()
def post_to_facebook(client_id: str, message: str) -> dict[str, Any]:
    """Create a new Facebook Page post with a text message.
    Input: client_id (str), message (str)
    Output: dict with post ID and creation status
    """
    return Manager(client_id).post_to_facebook(message)

@mcp.tool()
def reply_to_comment(client_id: str, post_id: str, comment_id: str, message: str) -> dict[str, Any]:
    """Reply to a specific comment on a Facebook post.
    Input: client_id (str), post_id (str), comment_id (str), message (str)
    Output: dict with reply creation status
    """
    return Manager(client_id).reply_to_comment(post_id, comment_id, message)

@mcp.tool()
def get_page_posts(client_id: str) -> dict[str, Any]:
    """Fetch the most recent posts on the Page.
    Input: client_id (str)
    Output: dict with list of post objects and metadata
    """
    return Manager(client_id).get_page_posts()

@mcp.tool()
def get_post_comments(client_id: str, post_id: str) -> dict[str, Any]:
    """Retrieve all comments for a given post.
    Input: client_id (str), post_id (str)
    Output: dict with comment objects
    """
    return Manager(client_id).get_post_comments(post_id)

@mcp.tool()
def delete_post(client_id: str, post_id: str) -> dict[str, Any]:
    """Delete a specific post from the Facebook Page.
    Input: client_id (str), post_id (str)
    Output: dict with deletion result
    """
    return Manager(client_id).delete_post(post_id)

@mcp.tool()
def delete_comment(client_id: str, comment_id: str) -> dict[str, Any]:
    """Delete a specific comment from the Page.
    Input: client_id (str), comment_id (str)
    Output: dict with deletion result
    """
    return Manager(client_id).delete_comment(comment_id)


@mcp.tool()
def hide_comment(client_id: str, comment_id: str) -> dict[str, Any]:
    """Hide a comment from public view."""
    return Manager(client_id).hide_comment(comment_id)


@mcp.tool()
def unhide_comment(client_id: str, comment_id: str) -> dict[str, Any]:
    """Unhide a previously hidden comment."""
    return Manager(client_id).unhide_comment(comment_id)

@mcp.tool()
def delete_comment_from_post(client_id: str, post_id: str, comment_id: str) -> dict[str, Any]:
    """Alias to delete a comment on a post.
    Input: client_id (str), post_id (str), comment_id (str)
    Output: dict with deletion result
    """
    return Manager(client_id).delete_comment_from_post(post_id, comment_id)

@mcp.tool()
def filter_negative_comments(client_id: str, comments: dict[str, Any]) -> list[dict[str, Any]]:
    """Filter comments for basic negative sentiment.
    Input: client_id (str), comments (dict)
    Output: list of flagged negative comments
    """
    return Manager(client_id).filter_negative_comments(comments)

@mcp.tool()
def get_number_of_comments(client_id: str, post_id: str) -> int:
    """Count the number of comments on a given post.
    Input: client_id (str), post_id (str)
    Output: integer count of comments
    """
    return Manager(client_id).get_number_of_comments(post_id)

@mcp.tool()
def get_number_of_likes(client_id: str, post_id: str) -> int:
    """Return the number of likes on a post.
    Input: client_id (str), post_id (str)
    Output: integer count of likes
    """
    return Manager(client_id).get_number_of_likes(post_id)

@mcp.tool()
def get_post_insights(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch all insights metrics (impressions, reactions, clicks, etc).
    Input: client_id (str), post_id (str)
    Output: dict with multiple metrics and their values
    """
    return Manager(client_id).get_post_insights(post_id)

@mcp.tool()
def get_post_impressions(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch total impressions of a post.
    Input: client_id (str), post_id (str)
    Output: dict with total impression count
    """
    return Manager(client_id).get_post_impressions(post_id)

@mcp.tool()
def get_post_impressions_unique(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch unique impressions of a post.
    Input: client_id (str), post_id (str)
    Output: dict with unique impression count
    """
    return Manager(client_id).get_post_impressions_unique(post_id)

@mcp.tool()
def get_post_impressions_paid(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch paid impressions of a post.
    Input: client_id (str), post_id (str)
    Output: dict with paid impression count
    """
    return Manager(client_id).get_post_impressions_paid(post_id)

@mcp.tool()
def get_post_impressions_organic(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch organic impressions of a post.
    Input: client_id (str), post_id (str)
    Output: dict with organic impression count
    """
    return Manager(client_id).get_post_impressions_organic(post_id)

@mcp.tool()
def get_post_engaged_users(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch number of engaged users.
    Input: client_id (str), post_id (str)
    Output: dict with engagement count
    """
    return Manager(client_id).get_post_engaged_users(post_id)

@mcp.tool()
def get_post_clicks(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch number of post clicks.
    Input: client_id (str), post_id (str)
    Output: dict with click count
    """
    return Manager(client_id).get_post_clicks(post_id)

@mcp.tool()
def get_post_reactions_like_total(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch number of 'Like' reactions.
    Input: client_id (str), post_id (str)
    Output: dict with like count
    """
    return Manager(client_id).get_post_reactions_like_total(post_id)

@mcp.tool()
def get_post_reactions_love_total(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch number of 'Love' reactions.
    Input: client_id (str), post_id (str)
    Output: dict with love count
    """
    return Manager(client_id).get_post_reactions_love_total(post_id)

@mcp.tool()
def get_post_reactions_wow_total(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch number of 'Wow' reactions.
    Input: client_id (str), post_id (str)
    Output: dict with wow count
    """
    return Manager(client_id).get_post_reactions_wow_total(post_id)

@mcp.tool()
def get_post_reactions_haha_total(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch number of 'Haha' reactions.
    Input: client_id (str), post_id (str)
    Output: dict with haha count
    """
    return Manager(client_id).get_post_reactions_haha_total(post_id)

@mcp.tool()
def get_post_reactions_sorry_total(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch number of 'Sorry' reactions.
    Input: client_id (str), post_id (str)
    Output: dict with sorry count
    """
    return Manager(client_id).get_post_reactions_sorry_total(post_id)

@mcp.tool()
def get_post_reactions_anger_total(client_id: str, post_id: str) -> dict[str, Any]:
    """Fetch number of 'Anger' reactions.
    Input: client_id (str), post_id (str)
    Output: dict with anger count
    """
    return Manager(client_id).get_post_reactions_anger_total(post_id)

@mcp.tool()
def get_post_top_commenters(client_id: str, post_id: str) -> list[dict[str, Any]]:
    """Get the top commenters on a post.
    Input: client_id (str), post_id (str)
    Output: list of user IDs with comment counts
    """
    return Manager(client_id).get_post_top_commenters(post_id)

@mcp.tool()
def post_image_to_facebook(client_id: str, image_url: str, caption: str) -> dict[str, Any]:
    """Post an image with a caption to the Facebook page.
    Input: client_id (str), image_url (str), caption (str)
    Output: dict of post result
    """
    return Manager(client_id).post_image_to_facebook(image_url, caption)

@mcp.tool()
def send_dm_to_user(client_id: str, user_id: str, message: str) -> dict[str, Any]:
    """Send a direct message to a user.
    Input: client_id (str), user_id (str), message (str)
    Output: dict of result from Messenger API
    """
    return Manager(client_id).send_dm_to_user(user_id, message)

@mcp.tool()
def update_post(client_id: str, post_id: str, new_message: str) -> dict[str, Any]:
    """Updates an existing post's message.
    Input: client_id (str), post_id (str), new_message (str)
    Output: dict of update result
    """
    return Manager(client_id).update_post(post_id, new_message)

@mcp.tool()
def schedule_post(client_id: str, message: str, publish_time: int) -> dict[str, Any]:
    """Schedule a new post for future publishing.
    Input: client_id (str), message (str), publish_time (Unix timestamp)
    Output: dict with scheduled post info
    """
    return Manager(client_id).schedule_post(message, publish_time)

@mcp.tool()
def get_page_fan_count(client_id: str) -> int:
    """Get the Page's total fan/like count.
    Input: client_id (str)
    Output: integer fan count
    """
    return Manager(client_id).get_page_fan_count()

@mcp.tool()
def get_post_share_count(client_id: str, post_id: str) -> int:
    """Get the number of shares for a post.
    Input: client_id (str), post_id (str)
    Output: integer share count
    """
    return Manager(client_id).get_post_share_count(post_id)


@mcp.tool()
def get_post_reactions_breakdown(client_id: str, post_id: str) -> dict[str, Any]:
    """Get counts for all reaction types on a post."""
    return Manager(client_id).get_post_reactions_breakdown(post_id)


@mcp.tool()
def bulk_delete_comments(client_id: str, comment_ids: list[str]) -> list[dict[str, Any]]:
    """Delete multiple comments by ID."""
    return Manager(client_id).bulk_delete_comments(comment_ids)


@mcp.tool()
def bulk_hide_comments(client_id: str, comment_ids: list[str]) -> list[dict[str, Any]]:
    """Hide multiple comments by ID."""
    return Manager(client_id).bulk_hide_comments(comment_ids)


@mcp.tool()
def bulk_unhide_comments(client_id: str, comment_ids: list[str]) -> list[dict[str, Any]]:
    """Unhide multiple comments by ID."""
    return Manager(client_id).bulk_unhide_comments(comment_ids)


@mcp.tool()
def get_comment_replies(client_id: str, comment_id: str) -> dict[str, Any]:
    """Get all replies to a specific comment."""
    return Manager(client_id).get_comment_replies(comment_id)


@mcp.tool()
def get_post_permalink(client_id: str, post_id: str) -> dict[str, Any]:
    """Get the permalink URL of a post."""
    return Manager(client_id).get_post_permalink(post_id)


@mcp.tool()
def get_scheduled_posts(client_id: str) -> dict[str, Any]:
    """List all scheduled (unpublished) posts on the Page."""
    return Manager(client_id).get_scheduled_posts()


@mcp.tool()
def get_page_info(client_id: str) -> dict[str, Any]:
    """Get extended information about the Facebook Page."""
    return Manager(client_id).get_page_info()


@mcp.tool()
def list_clients() -> list[str]:
    """List the configured client_id slugs available for use in every other tool's client_id argument."""
    from config import load_clients
    return sorted(load_clients().keys())
