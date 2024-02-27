# Blog website
Website with Django framework that is blog with ability to post, subscribe
user’s channels, show posts and interact with posts

## Installation
```bash
git clone https://github.com/SalahTawafsha/blog-website-by-Django.git
pip install -r requirements.txt
py manage.py migrate
```

## Blog features
- Login and register by django authentication
- User can post and edit post
- each post has a slug to show it in url
- User can just post 3 posts per day
- User can subscribe to other users
- User receive notification when subscribed user post
- User can like and comment on posts once in 30 seconds to prevent spamming bots
- User can use chat gpt-3 to generate post
- User can use chat gpt-3 to summarize post
- User can use chat gpt-3 to fix grammar of post
- User can read 3 posts per day from the blog
- if user post contain bad words it will be hidden by *** from other users
- if user post contain more than 3 bad words he will receive warning
- if user has 3 warnings his account will be blocked for posting and comment for 10 days
- paging for posts with 2 posts per page
- APIs for functionality of the website

## Usage
```bash
py manage.py runserver
```
