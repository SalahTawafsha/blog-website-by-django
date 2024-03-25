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
- User can comment on posts once in 30 seconds to prevent spamming bots
- User can use chat gpt-3 to generate post
- User can use chat gpt-3 to summarize post
- User can use chat gpt-3 to fix grammar of post
- User can read 3 posts per day from the blog
- if user post or comment contains bad words it will be hidden by *** from other users
- if user post or comment contains more than 3 bad words he will receive warning
- if user received 3 warnings his account will be blocked for posting and comment for 10 days
- paging for posts with 4 posts per page
- APIs for functionality of the website

## Usage
```bash
py manage.py runserver
```

## Screenshots

### Sign UP
![Screenshot 2024-03-25 145025](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/ffaa1e60-8bd8-4c81-aded-27dc4128e787)

### Login
![Screenshot 2024-03-25 145702](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/9b3a2814-b364-454c-a27d-6bdb610b3320)

### Home Screen
![Screenshot 2024-03-25 150038](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/904d612d-ae98-4e5c-ab04-9f145c083a79)

### Create Post
![Screenshot 2024-03-25 150227](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/a23f9842-49e8-4bdc-aa00-612132aab4df)
- we can just enter title for a post then click on generate By GPT

![Screenshot 2024-03-25 150448](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/71680843-b2bf-4680-9944-4daed3713ee4)
- after some seconds the body will filled by post
- Note that we can summarize the post or fix post grammers by buttons in bottom of form

### Home Page after create the post
![Screenshot 2024-03-25 151007](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/67b6e192-9376-46ab-90bf-094fd3e04a52)

### if try to add three posts then try to add forth in same day
![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/9ca71427-116e-4c7f-b56c-df5fe927982c)
![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/f2c9695b-5fb9-47e3-b4de-9b84e74c1eaa)

### when click on post we can edit, summarize or fix grammer of post
![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/8bb67a63-bb07-4fe8-9c15-2b7691daf4a2)

### if scroll down we can show like, dislike and comments sections
![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/507521fd-1b8f-4a06-b142-76595a3d18fd)

### let's put like and comment
![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/48752636-e4bf-457e-ae7f-4609970ccc82)
![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/f0b39c5e-86af-40e8-8049-d227353d9ef9)

### try add new comment before 30 secound
![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/68482d79-55be-4339-a47b-1d77b297abd3)

### enter a not owned post
![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/2defc24e-dadf-436c-988e-2de7f0678d37)
- we can show count of posts that visited today (just three posts are allowd in day)
- we can subscribe user to show his posts
I subscribed to this user

### when a subscibed user create post, we will show notification in home screen
![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/9b709c9d-30c4-4b6f-86c2-5352f10fc9ce)
- we can click on title to show post
- we can click on delete to delete the notification
- note that page contains just three posts and we can control paging from buttons in bottom of posts

### when create comment with more that three bad words
![Screenshot 2024-03-25 155209](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/7682dc55-0ba2-4254-bc5f-5ff407b7a2d4)

![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/4953864b-c750-48af-bcbd-a8eb61151700)
- note that user will show warning in start of page
- also, comment will not added

### when create post with more that three bad words
![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/cc07de8b-bd21-4ac0-98d1-395f35335b30)

![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/8df70bae-54d5-4fd0-bf48-62f4eb13e003)
- note that user will show warning in start of page
- also, bad words will shown as ***

### add post when user is blocked (when recived three warnings)
![image](https://github.com/SalahTawafsha/blog-website-by-Django/assets/93351227/945f8512-8717-49ab-931f-d128787ce982)













