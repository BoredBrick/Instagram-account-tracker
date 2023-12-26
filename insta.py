import os
from datetime import datetime, timedelta
import instaloader
import re

from winotify import Notification

# Find the latest folder
date_folder_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
folders = [folder for folder in os.listdir() if os.path.isdir(
    folder) and date_folder_pattern.match(folder)]
latest_folder = max(folders) if folders else None

# Set the default previous_day to yesterday if no matching folders are found
previous_day = (datetime.today() - timedelta(days=1)
                ).strftime('%Y-%m-%d') if not latest_folder else latest_folder
today = datetime.today().strftime('%Y-%m-%d')

# Update paths
path_today = os.path.join(os.getcwd(), today)
path_yesterday = os.path.join(os.getcwd(), previous_day)
found_previous = os.path.isdir(path_yesterday)

try:
    os.mkdir(path_today)
except FileExistsError:
    pass

old_file = os.path.join(path_yesterday, f'{previous_day}.txt')
new_file = os.path.join(path_today, f'{today}.txt')
what_is_new_file = os.path.join(path_today, "What is new.txt")


loader = instaloader.Instaloader(
    save_metadata=False)
loader.load_session_from_file("caban__daniel")

profile = instaloader.Profile.from_username(loader.context, "caban__daniel")


loader.dirname_pattern = path_today

print("Loading instagram data...")


with open(new_file, 'w') as file:
    for follower in profile.get_followers():
        file.write(follower.username + '\n')
    file.write('\n')
    for followee in profile.get_followees():
        file.write(followee.username + '\n')

if not found_previous:
    exit()


def read_followers_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.readlines()
            divide = data.index('\n')
            followers = data[:divide]
            followees = data[divide:]
            return followers, followees
    except FileNotFoundError:
        return [], []


def write_what_is_new(file_path, data):
    with open(file_path, 'w') as f:
        for category, items in data.items():
            f.write(f"{category}:\n")
            f.writelines(item.strip() + '\n' for item in items)
            f.write("\n\n")


old_followers, old_followees = read_followers_data(old_file)
new_followers, new_followees = read_followers_data(new_file)

changes = {
    'Who followed': [follower for follower in new_followers if follower not in old_followers],
    'Who unfollowed': [follower for follower in old_followers if follower not in new_followers],
    'Who was followed': [followee for followee in new_followees if followee not in old_followees],
    'Who was unfollowed': [followee for followee in old_followees if followee not in new_followees]
}

print("Writing what is new...")
write_what_is_new(what_is_new_file, changes)


path, dirs, files = next(os.walk(path_today))
file_count = len(files)

DEFAULT_LINES = 10
num_lines = sum(1 for _ in open(what_is_new_file)) - DEFAULT_LINES

new_info_message = 'New info!' if num_lines > 0 else "Nothing new"


file_count = 0

DEFAULT_LINES = 10
num_lines = sum(1 for _ in open(what_is_new_file)) - DEFAULT_LINES

new_info_message = 'New stuff' if num_lines > 0 else "Nothing new"


toast = Notification(
    app_id="Instaloader",
    title="Instaloader",
    msg=(
        f'New followers: {len(changes["Who followed"])} | '
        f'Unfollowers: {len(changes["Who unfollowed"])} | '
        f'New followees: {len(changes["Who was followed"])} | '
        f'Unfollowees: {len(changes["Who was unfollowed"])}'
    ),
    duration="long"
)

toast.show()

os.startfile(path_today)
