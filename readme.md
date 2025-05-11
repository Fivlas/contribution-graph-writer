# GitHub Contribution Graph Text Generator

This project allows you to **draw custom text** on your GitHub profile’s contribution graph by generating a commit history that creates patterns visible in the GitHub activity heatmap.

## ✨ Features

-   Convert input text into a 7x52 grid (one year of GitHub contribution boxes)
-   Auto-generates commits with specific dates to match your desired text
-   Pushes the commit history to a new GitHub repository for display
-   Uses GitHub API to automatically create a remote repo

## 🛠 Requirements

-   Python 3.x
-   Git installed and accessible from the terminal
-   A GitHub [Personal Access Token (PAT)](https://github.com/settings/tokens) with `repo` permissions

## 📦 Installation

1. Clone or download this repository.
2. Install dependencies:

```bash
pip install requests
```

## 🚀 Usage

Run the script:

```bash
python3 your_script_name.py
```

Then follow the prompts:

-   Year: The year to target on your GitHub grid (e.g., 2025)

-   GitHub Username: Your GitHub username

-   GitHub Access Token: Your PAT with repo access

-   Text to display: A short message (max ~8 characters, depending on width)

The script will:

1. Create a 7x52 grid pattern of your text

2. Create a local Git repo

3. Make timestamped commits to match the grid

4. Push the repo to GitHub

## 📌 Important Notes

-   Text longer than the allowed width will be truncated.

-   Only characters defined in the font dictionary (data/font.py) are supported.

-   Commits are backdated and may violate GitHub Terms if abused.

-   Use responsibly — this is mainly for educational or artistic purposes.

## 🧾 License

MIT License. Use at your own risk.

## ❤️ Credits

Inspired by creative uses of GitHub contribution graphs. Built using Python, Git, and GitHub API.
