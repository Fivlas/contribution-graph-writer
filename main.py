import os
import subprocess
from datetime import datetime, timedelta
from data.font import font
import requests

def create_text_matrix(text):
    max_chars = 52 // 6 
    
    if len(text) > max_chars:
        print(f"Warning: Text is too long ({len(text)} chars). Maximum allowed is {max_chars} chars.")
        print(f"Truncating text to: {text[:max_chars]}")
        text = text[:max_chars]
    
    grid = [[0 for _ in range(52)] for _ in range(7)]
    col = 0
    for char in text:
        if char not in font:
            print(f"Warning: Character '{char}' not found in font, replacing with space.")
            char = ' '
        char_matrix = font[char]
        for x in range(5):
            if col >= 52:
                break
            for y in range(7):
                grid[y][col] = char_matrix[y][x]
            col += 1
        if col < 52:
            col += 1
    return grid

def generate_commit_dates_from_matrix(grid, year):
    try:
        year = int(year)
    except ValueError:
        print(f"Error: '{year}' is not a valid year. Please enter a numeric year.")
        return []
        
    start_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
    while start_date.weekday() != 6:
        start_date += timedelta(days=1)

    dates = []
    for x in range(min(52, len(grid[0]))):
        for y in range(min(7, len(grid))):
            if grid[y][x]:
                commit_date = start_date + timedelta(weeks=x, days=y)
                if commit_date.year == year:
                    dates.append(commit_date)
    
    if not dates:
        print("Debug: No dates generated. Checking grid content...")
        has_ones = any(1 in row for row in grid)
        print(f"Grid contains active cells: {has_ones}")
        print(f"Grid dimensions: {len(grid)} rows x {len(grid[0])} columns")
    
    return dates

def make_commits(dates, repo_path, year):
    if not dates:
        print("Error: No commit dates provided.")
        return False
        
    os.makedirs(repo_path, exist_ok=True)
    os.chdir(repo_path)
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)
    if not os.path.exists("README.md"):
        with open("README.md", "w") as f:
            f.write(f"# Contribution Graph Text - {year}\n\nThis repository was created to display text on the GitHub contribution graph.")
    for date in dates:
        date_str = date.strftime("%Y-%m-%d")
        with open("log.txt", "a") as f:
            f.write(f"Commit for {date_str}\n")
        subprocess.run(["git", "add", "."], check=True)
        env = {
            "GIT_AUTHOR_DATE": f"{date_str}T12:00:00",
            "GIT_COMMITTER_DATE": f"{date_str}T12:00:00"
        }
        subprocess.run(
            ["git", "commit", "-m", f"Commit on {date_str}"],
            env={**os.environ, **env},
            check=True
        )
    subprocess.run(["git", "branch", "-M", "main"], check=True)
    return True

def create_github_repo(username, token, year):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": year,
        "description": f"Contribution Graph Text - {year}",
        "private": False,
        "auto_init": False
    }
    response = requests.post(f"https://api.github.com/user/repos", headers=headers, json=data)
    if response.status_code == 201:
        print(f"Repository {username}/{year} created successfully")
        return True
    else:
        print(f"Failed to create repository: {response.status_code} - {response.text}")
        return False

def push_to_github(username, token, year):
    repo_url = f"https://{token}@github.com/{username}/{year}.git"
    try:
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["git", "remote", "set-url", "origin", repo_url], check=True)
    subprocess.run(["git", "push", "-u", "origin", "main", "-f"], check=True)

def main():
    year = input("Year: ").strip()
    username = input("GitHub Username: ").strip()
    token = input("GitHub Access Token: ").strip()
    text = input("Text to display on grid: ").strip()

    if not year or not username or not token or not text:
        print("All fields are required.")
        return

    print(f"Creating matrix for text: '{text}'")
    grid = create_text_matrix(text)
        
    dates = generate_commit_dates_from_matrix(grid, year)

    if not dates:
        print("Error: No valid commit dates generated. Text might be too large or unsupported.")
        print("Please try a shorter text or check if the year is valid.")
        return

    print(f"Generated {len(dates)} commits to create the text pattern")
    
    print(f"Creating GitHub repository {username}/{year}")
    if not create_github_repo(username, token, year):
        print("Failed to create GitHub repository. Check your token permissions.")
        return
        
    repo_path = str(year)
    print(f"Creating repository in {repo_path}")
    if not make_commits(dates, repo_path, year):
        print("Failed to create commits.")
        return
        
    print(f"Pushing to GitHub as {username}/{year}")
    push_to_github(username, token, year)
    print(f"Done! Check https://github.com/{username}/{year}")

if __name__ == "__main__":
    main()
