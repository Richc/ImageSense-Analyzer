# Git Quick Reference

## Repository Information

**Repository:** https://github.com/Richc/ImageSense-Analyzer
**Owner:** Richc
**Branch:** main
**Initial Commit:** 572de88

---

## Common Git Commands

### Daily Workflow

```bash
# Check status
git status

# Add changes
git add .                    # Add all files
git add filename.py          # Add specific file

# Commit changes
git commit -m "Your message here"

# Push to GitHub
git push

# Pull latest changes
git pull
```

### Viewing History

```bash
# View commit log
git log
git log --oneline           # Compact view
git log --graph --oneline   # With branch visualization

# View changes
git diff                    # Unstaged changes
git diff --staged           # Staged changes
```

### Branching

```bash
# Create and switch to new branch
git checkout -b feature-name

# Switch branches
git checkout main
git checkout feature-name

# List branches
git branch

# Merge branch into main
git checkout main
git merge feature-name

# Delete branch
git branch -d feature-name
```

### Undoing Changes

```bash
# Discard changes in working directory
git checkout -- filename.py

# Unstage file
git reset HEAD filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### Remote Operations

```bash
# View remotes
git remote -v

# Push to remote
git push origin main

# Pull from remote
git pull origin main

# Fetch changes (doesn't merge)
git fetch
```

---

## Project-Specific Notes

### Protected Files (.gitignore)

These files are **never** committed:
- `.env` - Environment variables
- `*.key` - API keys
- `__pycache__/` - Python cache
- `.DS_Store` - macOS system files

### Making Updates

After editing files:

```bash
# 1. Check what changed
git status

# 2. Add your changes
git add .

# 3. Commit with descriptive message
git commit -m "Add feature: describe what you changed"

# 4. Push to GitHub
git push
```

### Commit Message Best Practices

**Good commit messages:**
- `Add cost tracking to image analyzer`
- `Fix JSON parsing error in API response`
- `Update README with installation instructions`
- `Refactor image processing to use async`

**Poor commit messages:**
- `update`
- `fix bug`
- `changes`
- `asdf`

### Format:
```
<type>: <description>

[optional body]
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting/style
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance

**Examples:**
```bash
git commit -m "feat: add batch folder processing"
git commit -m "fix: resolve tkinterdnd2 compatibility issue on Windows"
git commit -m "docs: update cost estimation in README"
```

---

## Backup Workflow

### Daily Backup
```bash
git add .
git commit -m "Daily backup: [describe work done]"
git push
```

### Before Major Changes
```bash
# Create a backup branch
git checkout -b backup-$(date +%Y%m%d)
git push -u origin backup-$(date +%Y%m%d)
git checkout main
```

---

## GitHub Web Interface

**Repository URL:** https://github.com/Richc/ImageSense-Analyzer

**Quick Links:**
- Code: https://github.com/Richc/ImageSense-Analyzer
- Issues: https://github.com/Richc/ImageSense-Analyzer/issues
- Settings: https://github.com/Richc/ImageSense-Analyzer/settings

**Things to do on GitHub:**
1. ✅ Repository created
2. ⬜ Add topics/tags (Optional)
3. ⬜ Add license (Optional)
4. ⬜ Enable GitHub Actions (Optional)
5. ⬜ Add collaborators (Optional)

---

## Troubleshooting

### "Push rejected"
```bash
# Pull first, then push
git pull --rebase
git push
```

### "Merge conflict"
```bash
# 1. Open conflicted files
# 2. Look for <<<<<<< markers
# 3. Resolve conflicts manually
# 4. Add resolved files
git add .
git commit -m "Resolve merge conflicts"
```

### "Accidentally committed sensitive data"
```bash
# Remove from last commit
git rm --cached filename.key
git commit --amend -m "Remove sensitive file"
git push --force

# If already pushed: contact GitHub support or use BFG Repo-Cleaner
```

### "Want to undo everything"
```bash
# Discard all local changes
git reset --hard origin/main
```

---

## Quick Tips

1. **Commit often** - Small, focused commits are better than large ones
2. **Pull before push** - Always sync before pushing
3. **Use branches** - Keep main clean, work in feature branches
4. **Write good messages** - Your future self will thank you
5. **Check before committing** - Use `git diff` and `git status`
6. **Never commit secrets** - API keys, passwords, tokens stay local

---

## GitHub CLI Commands

Since you have `gh` installed:

```bash
# View repository info
gh repo view

# Open repository in browser
gh repo view --web

# Create issue
gh issue create

# View pull requests
gh pr list

# Create release
gh release create v1.0.0 --title "Release v1.0.0" --notes "Initial release"
```

---

## Useful Aliases

Add to `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    lg = log --oneline --graph --all
    last = log -1 HEAD
    unstage = reset HEAD --
```

Then use: `git st` instead of `git status`, etc.

---

**Last Updated:** 2026-02-20
**Repository:** https://github.com/Richc/ImageSense-Analyzer
