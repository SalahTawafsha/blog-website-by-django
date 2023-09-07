import argparse

from httpx import post, get

parser = argparse.ArgumentParser()

# list all comments
parser.add_argument("-l", "--list-comments", action="store_true")

# add new comment by token
parser.add_argument(
    "-a",
    "--add-comment",
    nargs=3,
    metavar=("token", "post_id", "comment_body"),
)

args = parser.parse_args()

# py comments.py -l
if args.list_comments:
    response = get(url="http://127.0.0.1:8000/API/comments/")

    print(response.text)

# py comments.py -a <token> <post_id> <comment_body>
if args.add_comment:
    response = post(url=f"http://127.0.0.1:8000/API/comments/",
                    headers={"Authorization": "token " + args.add_comment[0]},
                    data={"post_id": args.add_comment[1], "body": args.add_comment[2]})

    print(response.text)
