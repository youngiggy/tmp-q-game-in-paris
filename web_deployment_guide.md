# Web Deployment Guide for Paris Street Game

This guide will walk you through the process of deploying your Paris Street Game to the web so others can play it without installing Python or Pygame.

## Option 1: Using Pygbag (Recommended)

[Pygbag](https://pygame-web.github.io/) is a tool that converts Pygame applications to WebAssembly, allowing them to run in modern web browsers.

### Step 1: Install Pygbag

```bash
pip install pygbag
```

### Step 2: Prepare Your Game

Make sure your game is in a single directory with all necessary assets. The main game file should be named `paris_game.py`.

### Step 3: Build the Web Version

```bash
cd /path/to/your/game
pygbag paris_game.py
```

This will create a `build/web` directory containing the web version of your game.

### Step 4: Test Locally

Pygbag starts a local web server during the build process. You can test your game by opening the URL shown in the terminal (usually http://localhost:8000).

### Step 5: Deploy to a Web Host

You can upload the contents of the `build/web` directory to any web hosting service:

- **GitHub Pages**: Free and easy to set up
- **Netlify**: Offers free hosting with drag-and-drop deployment
- **Vercel**: Good for frontend projects with simple deployment
- **Amazon S3**: Reliable but requires more setup

## Option 2: Using Replit

[Replit](https://replit.com/) is an online IDE that allows you to run code in the browser and share it with others.

### Step 1: Create a Replit Account

Go to [replit.com](https://replit.com/) and sign up for an account.

### Step 2: Create a New Python Repl

1. Click "Create Repl"
2. Select "Python" as the language
3. Give your project a name (e.g., "ParisStreetGame")
4. Click "Create Repl"

### Step 3: Upload Your Game Files

1. In the Files panel, upload your `paris_game.py` file
2. Create an `assets` directory and upload all your game assets

### Step 4: Install Pygame

In the Shell tab, run:

```bash
pip install pygame
```

### Step 5: Configure the Run Button

Create a `.replit` file with the following content:

```
language = "python3"
run = "python paris_game.py"
```

### Step 6: Share Your Game

Click the "Share" button at the top of the page to get a link that others can use to run your game.

## Option 3: GitHub Pages with Pygbag Automation

This option uses GitHub Actions to automatically build your game with Pygbag and deploy it to GitHub Pages.

### Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and create a new repository
2. Upload your game files to the repository

### Step 2: Create GitHub Actions Workflow

Create a file named `.github/workflows/build.yml` with the following content:

```yaml
name: Build and Deploy

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pygbag
    - name: Build with pygbag
      run: |
        pygbag --build paris_game.py
    - name: Deploy to GitHub Pages
      uses: JamesIves/github-pages-deploy-action@v4
      with:
        folder: build/web
```

### Step 3: Enable GitHub Pages

1. Go to your repository settings
2. Navigate to "Pages"
3. Under "Source", select "GitHub Actions"

### Step 4: Trigger the Build

Push a commit to the main branch to trigger the GitHub Actions workflow. Once complete, your game will be available at `https://yourusername.github.io/your-repository-name/`.

## Troubleshooting Common Issues

### Game Doesn't Load in Browser

- Make sure your game doesn't use any system-specific features
- Check browser console for errors
- Ensure all file paths use relative paths

### Performance Issues

- Optimize your game for web performance
- Reduce image sizes and complexity
- Consider adding loading screens for larger assets

### Input Handling Problems

- Web versions may handle keyboard/mouse input differently
- Test thoroughly and adjust input handling if needed

## Additional Resources

- [Pygbag Documentation](https://pygame-web.github.io/)
- [Replit Documentation](https://docs.replit.com/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
