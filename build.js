// Simple build script to prepare static assets
const fs = require('fs-extra');
const path = require('path');

// Ensure the build directory exists
fs.ensureDirSync('build');

// Copy static assets
fs.copySync('static', 'build/static');

// Create a simple index.html for static hosting
const indexHtml = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>StockMaster - Redirecting</title>
  <link rel="stylesheet" href="/static/css/style.css">
  <script>
    // Redirect to the deployed serverless function
    window.location.href = "/.netlify/functions/api";
  </script>
</head>
<body>
  <div style="text-align: center; margin-top: 50px;">
    <h1>StockMaster</h1>
    <p>Redirecting to application...</p>
  </div>
</body>
</html>
`;

fs.writeFileSync('build/index.html', indexHtml);

console.log('Build completed successfully!');