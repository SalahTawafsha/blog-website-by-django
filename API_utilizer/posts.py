import argparse

from httpx import post, get, put, delete

parser = argparse.ArgumentParser()

# list all posts
parser.add_argument("-l", "--list-posts", action="store_true")

# add new post
parser.add_argument(
    "-a",
    "--add-post",
    nargs=3,
    metavar=("token", "post_title", "post_body"),
)

# update post
parser.add_argument(
    "-u",
    "--update-post",
    nargs=4,
    metavar=("token", "post_id", "new_post_title", "new_post_body"),
)

# delete post
parser.add_argument(
    "-d",
    "--delete-post",
    nargs=2,
    metavar=("token", "post_id"),
)

args = parser.parse_args()

# py posts.py -l
if args.list_posts:
    response = get(url="http://127.0.0.1:8000/API/posts/")

    print(response.text)

# py posts.py -a <token> <title> <body>
if args.add_post:
    response = post(url="http://127.0.0.1:8000/API/posts/",
                    headers={"Authorization": "token " + args.add_post[0]},
                    data={"title": args.add_post[1], "body": args.add_post[2]})

    print(response.text)

# py -u <token> <post-id> <new-title> <new-body>
if args.update_post:  # "token", "post_id", "post_title", "post_body"),
    response = put(url=f"http://127.0.0.1:8000/API/posts/{args.update_post[1]}/",
                   headers={"Authorization": "token " + args.update_post[0]},
                   data={"title": args.update_post[2], "body": args.update_post[3]})

    print(response.text)

# py -d <token> <post-id>
if args.delete_post:
    response = delete(url=f"http://127.0.0.1:8000/API/posts/{args.delete_post[1]}/",
                      headers={"Authorization": "token " + args.delete_post[0]},)

    print(response.text)
