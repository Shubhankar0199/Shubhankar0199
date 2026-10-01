# Setup

## 1. Clone

```bash
git clone https://github.com/Shubhankar0199/Shubhankar0199.git
cd Shubhankar0199
```

## 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Add profile photo

The repository already contains the supplied photo at:

```text
assets/profile-photo.png
```

Replace it with another crop only if you want a different portrait.

## 4. Generate portrait

```bash
python scripts/dotify.py assets/profile-photo.png \
  --output assets/portrait.svg \
  --cols 100 \
  --detail 0.5 \
  --color \
  --reveal
```

## 5. Generate radar, statistics and project cards

Set a GitHub token locally if you want live repository data:

```bash
export GITHUB_TOKEN="YOUR_TOKEN"
python scripts/radar.py
python scripts/make_stats.py
python scripts/cards.py
```

The scripts never store the token in source files.

## 6. Configure GitHub Actions

Create a repository secret named:

```text
METRICS_TOKEN
```

A GitHub token with the permissions required by the metrics workflow should be stored there. Never put the token in `README.md`, Python files, or committed `.env` files.

## 7. Push

```bash
git add .
git commit -m "Create GitHub profile"
git push origin main
```

## 8. Run workflows

Open:

```text
GitHub → Actions
```

The workflows support `workflow_dispatch` so you can refresh them manually.

## Social links

Before publishing, replace these placeholders in `README.md`:

```text
YOUR_LINKEDIN_URL
YOUR_LEETCODE_URL
YOUR_PORTFOLIO_URL
YOUR_EMAIL
```

No social URLs are invented by this repository.
