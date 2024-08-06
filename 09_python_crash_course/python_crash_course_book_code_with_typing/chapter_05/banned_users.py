banned_users:list[str] = ['andrew', 'carolina', 'david']
user:str = 'marie'

if user not in banned_users:
    print(f"{user.title()}, you can post a response if you wish.")