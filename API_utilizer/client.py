import argparse

from httpx import post, get, delete, put

HOST = "127.0.0.1:8000"
COMMENTS_END_POINTS = \
    {
        "GET_COMMENTS": "http://" + HOST + "/API/comments/",
        "ADD_COMMENT": "http://" + HOST + "/API/comments/",
    }

POSTS_END_POINTS = \
    {
        "GET_POSTS": "http://" + HOST + "/API/posts/",
        "ADD_POST": "http://" + HOST + "/API/posts/",
        "UPDATE_POST": "http://" + HOST + "/API/posts/{post_id}/",
        "DELETE_POST": "http://" + HOST + "/API/posts/{post_id}/"
    }

USERS_END_POINTS = \
    {
        "LOG_IN": "http://" + HOST + "/API/api-token-auth/",
        "SIGN_UP": "http://" + HOST + "/API/users/",
        "GET_USERS": "http://" + HOST + "/API/users/",
    }

parser = argparse.ArgumentParser()

# ********* USERS *********
# log in argument (get token)
parser.add_argument(
    "-gt",
    "--get-token",
    nargs=2,
    metavar=("user_name", "password"),
)

# sign up argument
parser.add_argument(
    "-su",
    "--sign-up",
    nargs=4,
    metavar=("token", "user_name", "email", "password"),

)

# get users argument
parser.add_argument(
    "-lu",
    "--list-users",
    metavar="token")

# ********* POSTS *********
# list all posts
parser.add_argument("-lp", "--list-posts", action="store_true")

# add new post
parser.add_argument(
    "-ap",
    "--add-post",
    nargs=3,
    metavar=("token", "post_title", "post_body"),
)

# update post
parser.add_argument(
    "-up",
    "--update-post",
    nargs=4,
    metavar=("token", "post_id", "new_post_title", "new_post_body"),
)

# delete post
parser.add_argument(
    "-dp",
    "--delete-post",
    nargs=2,
    metavar=("token", "post_id"),
)

# ********* Comments *********

# list all comments
parser.add_argument("-lc", "--list-comments", action="store_true")

# add new comment by token
parser.add_argument(
    "-ac",
    "--add-comment",
    nargs=3,
    metavar=("token", "post_id", "comment_body"),
)

args = parser.parse_args()

# py client.py -gt <username> <password>
if args.get_token:
    response = post(url=USERS_END_POINTS["LOG_IN"],
                    data={"username": args.get_token[0], "password": args.get_token[1]})

    print(response.json())

# py client.py -su <token> <username> <email> <password>
if args.sign_up:
    response = post(url=USERS_END_POINTS["SIGN_UP"],
                    headers={"Authorization": "token " + args.sign_up[0]},
                    data={"username": args.sign_up[1], "email": args.sign_up[2],
                          "password": args.sign_up[3]})

    print(response.text)

# py client.py -lu <token>
if args.list_users:
    response = get(url=USERS_END_POINTS["GET_USERS"],
                   headers={"Authorization": "token " + args.list_users})

    print(response.text)

# py client.py -lp
if args.list_posts:
    response = get(url=POSTS_END_POINTS["GET_POSTS"])

    print(response.text)

# py client.py -ap <token> <title> <body>
if args.add_post:
    response = post(url=POSTS_END_POINTS["ADD_POST"],
                    headers={"Authorization": "token " + args.add_post[0]},
                    data={"title": args.add_post[1], "body": args.add_post[2]})

    print(response.text)

# py client.py -up <token> <post-id> <new-title> <new-body>
if args.update_post:
    response = put(url=POSTS_END_POINTS["UPDATE_POST"].format(post_id=args.update_post[1]),
                   headers={"Authorization": "token " + args.update_post[0]},
                   data={"title": args.update_post[2], "body": args.update_post[3]})

    print(response.text)

# py client.py -dp <token> <post-id>
if args.delete_post:
    response = delete(url=POSTS_END_POINTS["DELETE_POST"].format(post_id=args.delete_post[1]),
                      headers={"Authorization": "token " + args.delete_post[0]}, )

    print(response.text)

# py client.py -lc
if args.list_comments:
    response = get(url=COMMENTS_END_POINTS["GET_COMMENTS"])

    print(response.text)

# py client.py -ac <token> <post_id> <comment_body>
if args.add_comment:
    response = post(url=COMMENTS_END_POINTS["ADD_COMMENT"],
                    headers={"Authorization": "token " + args.add_comment[0]},
                    data={"post_id": args.add_comment[1], "body": args.add_comment[2]})

    print(response.text)
