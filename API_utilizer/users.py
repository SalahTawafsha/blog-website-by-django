import argparse

from httpx import post, get

parser = argparse.ArgumentParser()

# log in argument (get token)
parser.add_argument(
    "-l",
    "--login",
    nargs=2,
    metavar=("user_name", "password"),
)

# sign up argument
parser.add_argument(
    "-s",
    "--sign-up",
    nargs=3,
    metavar=("token", "user_name", "password"),

)

# get users argument
parser.add_argument(
    "-a",
    "--get-users",
    metavar="token")

args = parser.parse_args()

if args.login:
    response = post(url="http://127.0.0.1:8000/api-token-auth/",
                    data={"username": args.login[0], "password": args.login[1]})

    print(response.text)

if args.sign_up:
    response = post(url="http://127.0.0.1:8000/API/users/",
                    headers={"Authorization": "token " + args.sign_up[0]},
                    data={"username": args.sign_up[1], "password": args.sign_up[2]})

    print(response.text)

if args.get_users:
    response = get(url="http://127.0.0.1:8000/API/users/",
                   headers={"Authorization": "token " + args.get_users})

    print(response.text)
