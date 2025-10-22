# How to publish to GitHub Wiki

Option A — Manual copy via GitHub UI
1. Open your repository on GitHub.
2. Go to Wiki tab and create the Home page.
3. Copy-paste the contents of docs/wiki/*.md into corresponding wiki pages (same titles recommended).

Option B — Push to the wiki git repository
1. Clone the wiki repo locally (replace ORG/REPO):
   git clone git@github.com:ORG/REPO.wiki.git
2. Copy files from docs/wiki/ into the cloned REPO.wiki folder.
3. Commit and push:
   git add . && git commit -m "docs(wiki): publish pages" && git push

Notes
- Wiki-style links like [[Page Name]] are supported by GitHub Wiki.
- Keep docs/wiki as the source of truth and update regularly.
