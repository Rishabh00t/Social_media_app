from fastapi import FastAPI
from src.resource.Auth.api import auth_router
from src.resource.Post.api import post_router
from src.resource.comment.api import comment_router
from src.resource.like.api import like_router
from src.resource.user_profile.api import user_router
from src.resource.followers.api import follower_router


description = """
SocialBuzz API allows you to build and manage a vibrant social media platform. 🚀

## Posts

You can:
* **Create posts** to share your thoughts, images, or videos.
* **Read posts** from other users on the platform.
* **Update posts** to refine your content.
* **Delete posts** when no longer needed.

## Users

You will be able to:
* **Create user profiles** with detailed information.
* **Read user profiles** to connect with others.
* **Update user profiles** (_feature in progress_).
* **Delete user accounts** (_feature in progress_).

## Features

SocialBuzz API empowers your platform with:
* **Feed Management**: Display posts in chronological or curated order.
* **Comments & Likes**: Engage with content through interactions.
* **Follow System**: Follow other users to stay updated with their posts.
* **Notifications**: Keep users informed of updates and interactions.
* **Search Functionality**: Find posts or users easily.
"""

app = FastAPI(
    title="SocialBuzz",
    description=description,
    summary="Your go-to API for building a thriving social media experience.",
    version="1.2.0",
    terms_of_service="http://socialbuzz.example.com/terms/",
    contact={
        "name": "SocialBuzz Team",
        "url": "http://socialbuzz.example.com/contact/",
        "email": "support@socialbuzz.example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(like_router)
app.include_router(user_router)
app.include_router(follower_router)

@app.get("/")
def read_app():
    return {"welcome": "Welcome to the FastAPI Signup"}
