# StockMaster Deployment Guide

This guide provides instructions for deploying the StockMaster inventory management application to Netlify or Vercel.

## Deployment Options

### Option 1: Vercel Deployment

1. **Prerequisites**
   - A Vercel account
   - Vercel CLI (optional)

2. **Deployment Steps**
   - Push your code to a GitHub repository
   - Connect your Vercel account to GitHub
   - Import your repository in the Vercel dashboard
   - Vercel will automatically detect the Python application
   - Deploy using the `vercel.json` configuration

3. **Environment Variables**
   - Set `SECRET_KEY` for Flask security
   - Set `DATABASE_URL` for your database connection

### Option 2: Netlify Deployment

1. **Prerequisites**
   - A Netlify account
   - Netlify CLI (optional)

2. **Deployment Steps**
   - Push your code to a GitHub repository
   - Connect your Netlify account to GitHub
   - Import your repository in the Netlify dashboard
   - Configure build settings according to `netlify.toml`
   - Deploy your application

3. **Environment Variables**
   - Set `SECRET_KEY` for Flask security
   - Set `DATABASE_URL` for your database connection

## Important Notes

- **Database**: Both Netlify and Vercel are primarily for frontend hosting. For a full-stack application:
  - Use a separate database service (e.g., MongoDB Atlas, Supabase, or PostgreSQL on Railway)
  - Update the `DATABASE_URL` environment variable accordingly

- **Serverless Functions**: The Flask application needs to be adapted to run as serverless functions:
  - Netlify: Uses the function in `netlify/functions/api.js`
  - Vercel: Uses the configuration in `vercel.json`

## Deployment Files

The following files have been prepared for deployment:

1. `vercel.json` - Configuration for Vercel deployment
2. `netlify.toml` - Configuration for Netlify deployment
3. `netlify/functions/api.js` - Serverless function for Netlify
4. `build.js` - Script to prepare static assets
5. `requirements.txt` - Lists all Python dependencies
6. Updated `app.py` with production configuration

## Limitations

Flask applications are traditionally designed for server environments. Deploying to Netlify or Vercel requires:

1. Adapting your application to work with serverless functions
2. Using a separate database service
3. Potentially restructuring parts of your application

For a more straightforward deployment of a Flask application, consider:
- Heroku
- Railway
- Render
- PythonAnywhere
- AWS Elastic Beanstalk