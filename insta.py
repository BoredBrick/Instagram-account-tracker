from win10toast_click import ToastNotifier
import instaloader
from datetime import datetime, timedelta
import os

previous_day = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
today = datetime.today().strftime('%Y-%m-%d')

path_today = os.getcwd() + "\\" + str(today)
path_today_stories = path_today + "\\" + "storicka"
path_yesterday = os.getcwd() + "\\" + str(previous_day)

found_previous = False
for i in range(2, 31):
    if os.path.isdir(path_yesterday):
        found_previous = True
        break
    else:
        previous_day = (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')
        path_yesterday = os.getcwd() + "\\" + str(previous_day)

if not found_previous:
    previous_day = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    today = datetime.today().strftime('%Y-%m-%d')

try:
    os.mkdir(path_today)
except:
    pass

old_file = path_yesterday + "\\" + str(previous_day) + '.txt'
new_file = path_today + "\\" + str(today) + '.txt'

L = instaloader.Instaloader(save_metadata=False, dirname_pattern=path_today_stories)
L.login("YOUR_LOGIN", "YOUR_PASSWORD")


profile = instaloader.Profile.from_username(L.context, "TRACKER_ACCOUNT_NAME")
L.dirname_pattern = path_today

with open(new_file, 'w') as file:
    for follower in profile.get_followers():
        file.write(follower.username + '\n')
    file.write('\n')
    for followee in profile.get_followees():
        file.write(followee.username + '\n')

if not found_previous:
    exit()

with open(old_file, 'r') as f:
    old_data = f.readlines()
    divide = old_data.index('\n')
    old_followers = old_data[:divide]
    old_followees = old_data[divide:]

with open(new_file, 'r') as f:
    new_data = f.readlines()
    divide = new_data.index('\n')
    new_followers = new_data[:divide]
    new_followees = new_data[divide:]

what_is_new_file = path_today + "\\" + "What is new" + '.txt'
with open(what_is_new_file, 'w') as f:

    who_followed = [follower for follower in new_followers if follower not in old_followers]
    who_unfollowed = [follower for follower in old_followers if follower not in new_followers]
    who_was_followed = [followee for followee in new_followees if followee not in old_followees]
    who_was_unfollowed = [followee for followee in old_followees if followee not in new_followees]

    f.write("Who followed:\n")
    for item in who_followed:
        f.write(item.strip() + '\n')
    f.write("\n\n")
    f.write("Who unfollowed:\n")
    for item in who_unfollowed:
        f.write(item.strip() + '\n')
    f.write("\n\n")
    f.write("Who was followed:\n")
    for item in who_was_followed:
        f.write(item.strip() + '\n')
    f.write("\n\n")
    f.write("Who was unfollowed:\n")
    for item in who_was_unfollowed:
        f.write(item.strip() + '\n')


def openFile():
    os.startfile(path_today)


file_count = 0

if os.path.isdir(path_today_stories):
    path, dirs, files = next(os.walk(path_today_stories))
    file_count = len(files)

DEFAULT_LINES = 10
num_lines = sum(1 for _ in open(what_is_new_file)) - DEFAULT_LINES

new_info_message = 'New stuff' if num_lines > 0 else "Nothing new"


toast = ToastNotifier()
toast.show_toast("InstaLoader daily update", f"Stories: {file_count}  {new_info_message}",
                 icon_path=None, duration=5, callback_on_click=openFile)
