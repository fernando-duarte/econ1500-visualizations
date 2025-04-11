# Deploying to Streamlit Community Cloud

This document provides step-by-step instructions for deploying this application to Streamlit Community Cloud.

## Prerequisites

1. A [GitHub](https://github.com/) account
2. A [Streamlit Community Cloud](https://streamlit.io/cloud) account (you can sign in with your GitHub account)
3. Git installed on your local machine

## Deployment Instructions

### Option 1: Using the Deployment Script

1. Navigate to the app directory:
   ```bash
   cd econ1500-apps
   ```

2. Run the deployment script:
   ```bash
   ./deploy.sh
   ```

3. Follow the prompts to:
   - Enter a commit message
   - Provide your GitHub repository URL (first time only)

4. After the script completes, follow the "Next steps" instructions provided.

### Option 2: Manual Deployment

1. Create a new public GitHub repository.

2. Initialize git in the app directory (if not already done):
   ```bash
   cd econ1500-apps
   git init
   ```

3. Add the GitHub repository as the remote origin:
   ```bash
   git remote add origin https://github.com/your-username/your-repo-name.git
   ```

4. Add all files, commit, and push to GitHub:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

5. Go to [Streamlit Community Cloud](https://streamlit.io/cloud) and sign in with your GitHub account.

6. Click "New app" and select your repository.

7. In the deployment settings:
   - Set the main file path to `Home.py`
   - Leave other settings as default

8. Click "Deploy!" and wait for the deployment to complete.

## Accessing Your Deployed App

Once deployed, your app will be available at:
```
https://[your-app-name].streamlit.app
```

## Updating Your Deployed App

After making changes to your code:

1. Commit and push changes to GitHub:
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```

2. Streamlit Cloud will automatically detect changes and redeploy your app.

## Troubleshooting

If your app fails to deploy, check:

1. Your `requirements.txt` file contains all necessary dependencies
2. You've set the correct main file path (`Home.py`)
3. Check the deployment logs for any errors

For additional help, refer to the [Streamlit Community Cloud documentation](https://docs.streamlit.io/streamlit-community-cloud). 