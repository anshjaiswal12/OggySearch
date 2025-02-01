I'll help you push your code to GitHub. Here are the steps you need to follow:

1. First, initialize a git repository in your project folder (if not already done):
```bash
git init
```

2. Add your files to git staging (notice we're not adding .env due to .gitignore):
```bash
git add OggySearch.py .gitignore README.md
```

3. Create your first commit:
```bash
git commit -m "Initial commit: OggySearch application"
```

4. Add your GitHub repository as remote:
```bash
git remote add origin https://github.com/anshjaiswal12/OggySearch.git
```

5. Push your code to GitHub:
```bash
git push -u origin main
```

If you're pushing for the first time, you might need to:
1. Authenticate with GitHub (you'll be prompted for your credentials)
2. If you're using main branch (newer repos) instead of master branch, use `main` in the push command as shown above
3. If you get a rejection due to unrelated histories, you can force the push with:
```bash
git push -u origin main --force
```

Important notes:
1. Make sure your `.gitignore` file is properly set up before pushing
2. Verify that `.env` file is not being tracked by git (you can check with `git status`)
3. The `.env` file should not appear in the files being added to git

After pushing, you should see your code appear in your GitHub repository at https://github.com/anshjaiswal12/OggySearch.git
