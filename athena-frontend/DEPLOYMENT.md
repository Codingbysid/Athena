# 🚀 Athena Frontend Deployment Guide

This guide covers deployment options for the Athena frontend across different platforms and environments.

## 📋 Prerequisites

- Node.js 16+ installed
- Git repository access
- API service running (Athena backend)
- Environment variables configured

## 🔧 Environment Configuration

### Required Environment Variables

Create a `.env` file in the project root:

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:5002
VITE_API_TIMEOUT=10000

# Tableau Configuration
VITE_TABLEAU_SERVER_URL=https://your-tableau-server.com
VITE_TABLEAU_SITE_URL=
VITE_TABLEAU_DASHBOARD_PATH=/views/AthenaHealthScores/AthenaDashboard

# Salesforce Configuration
VITE_SALESFORCE_CLIENT_ID=your_client_id
VITE_SALESFORCE_CLIENT_SECRET=your_client_secret
VITE_SALESFORCE_INSTANCE_URL=https://your-instance.salesforce.com

# Slack Configuration
VITE_SLACK_BOT_TOKEN=xoxb-your-bot-token
VITE_SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook

# Feature Flags
VITE_ENABLE_TABLEAU=true
VITE_ENABLE_SALESFORCE=true
VITE_ENABLE_SLACK=true
VITE_ENABLE_ANALYTICS=true
```

### Production Environment Variables

For production, use secure environment variables:

```bash
# Production API
VITE_API_BASE_URL=https://api.athena.com
VITE_API_TIMEOUT=15000

# Production Tableau
VITE_TABLEAU_SERVER_URL=https://tableau.athena.com
VITE_TABLEAU_DASHBOARD_PATH=/views/Production/AthenaDashboard

# Production Salesforce
VITE_SALESFORCE_CLIENT_ID=prod_client_id
VITE_SALESFORCE_INSTANCE_URL=https://login.salesforce.com
```

## 🚀 Deployment Options

### 1. Vercel (Recommended)

Vercel provides the best performance and developer experience for React applications.

#### Setup

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Login to Vercel**
```bash
vercel login
```

3. **Deploy**
```bash
vercel --prod
```

#### Configuration

Create `vercel.json` in project root:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

#### Environment Variables in Vercel

1. Go to Vercel Dashboard
2. Select your project
3. Go to Settings → Environment Variables
4. Add all required environment variables

### 2. Netlify

#### Setup

1. **Build the project**
```bash
npm run build
```

2. **Deploy to Netlify**
```bash
# Option 1: Drag and drop dist/ folder
# Option 2: Use Netlify CLI
npm install -g netlify-cli
netlify deploy --dir=dist --prod
```

#### Configuration

Create `netlify.toml` in project root:

```toml
[build]
  publish = "dist"
  command = "npm run build"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"

[[headers]]
  for = "/static/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

### 3. AWS S3 + CloudFront

#### Setup

1. **Install AWS CLI**
```bash
pip install awscli
aws configure
```

2. **Create S3 bucket**
```bash
aws s3 mb s3://athena-frontend
aws s3 website --index-document index.html --error-document index.html s3://athena-frontend
```

3. **Build and deploy**
```bash
npm run build
aws s3 sync dist/ s3://athena-frontend --delete
```

4. **Configure CloudFront**
- Create CloudFront distribution
- Set S3 bucket as origin
- Configure custom error pages for SPA routing

#### CloudFormation Template

Create `cloudformation.yml`:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Athena Frontend Infrastructure'

Parameters:
  DomainName:
    Type: String
    Default: athena-frontend.com

Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref DomainName
      WebsiteConfiguration:
        IndexDocument: index.html
        ErrorDocument: index.html

  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Origins:
          - Id: S3Origin
            DomainName: !GetAtt S3Bucket.RegionalDomainName
            S3OriginConfig:
              OriginAccessIdentity: !Ref CloudFrontOAI
        DefaultCacheBehavior:
          TargetOriginId: S3Origin
          ViewerProtocolPolicy: redirect-to-https
          DefaultTTL: 86400
          MaxTTL: 31536000
          MinTTL: 0
        Enabled: true
        DefaultRootObject: index.html
        CustomErrorResponses:
          - ErrorCode: 404
            ResponseCode: 200
            ResponsePagePath: /index.html

  CloudFrontOAI:
    Type: AWS::CloudFront::CloudFrontOriginAccessIdentity
    Properties:
      CloudFrontOriginAccessIdentityConfig:
        Comment: !Sub 'OAI for ${DomainName}'
```

### 4. Docker Deployment

#### Dockerfile

Create `Dockerfile`:

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

#### Nginx Configuration

Create `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        # Gzip compression
        gzip on;
        gzip_vary on;
        gzip_min_length 1024;
        gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

        # Cache static assets
        location /static/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # SPA routing
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    }
}
```

#### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  athena-frontend:
    build: .
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
    restart: unless-stopped

  athena-api:
    image: athena-api:latest
    ports:
      - "5002:5002"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/athena
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=athena
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 5. Salesforce Lightning Web Component

#### Setup

1. **Install Salesforce CLI**
```bash
npm install -g @salesforce/cli
sfdx auth:web:login
```

2. **Create LWC project**
```bash
sfdx force:project:create --projectname athena-lwc
cd athena-lwc
```

3. **Build for LWC**
```bash
npm run build:lwc
```

4. **Deploy to Salesforce**
```bash
sfdx force:source:deploy -p force-app/main/default/lwc/
```

#### LWC Configuration

Create `force-app/main/default/lwc/athenaDashboard/athenaDashboard.js`:

```javascript
import { LightningElement, api, track } from 'lwc';
import { loadScript } from 'lightning/platformResourceLoader';

export default class AthenaDashboard extends LightningElement {
    @api recordId;
    @track isLoading = true;
    @track error;

    connectedCallback() {
        this.loadAthenaApp();
    }

    async loadAthenaApp() {
        try {
            // Load the built React app
            await loadScript(this, '/resource/athena_frontend');
            this.isLoading = false;
        } catch (error) {
            this.error = error;
            this.isLoading = false;
        }
    }
}
```

## 🔒 Security Considerations

### HTTPS Configuration

Ensure HTTPS is enabled in production:

```javascript
// vite.config.js
export default defineConfig({
  server: {
    https: true
  }
});
```

### Content Security Policy

Add CSP headers in production:

```html
<!-- index.html -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline' 'unsafe-eval';
               style-src 'self' 'unsafe-inline';
               img-src 'self' data: https:;
               connect-src 'self' https://api.athena.com;">
```

### Environment Variable Security

- Never commit `.env` files to version control
- Use secure environment variable management
- Rotate API keys regularly
- Use least privilege access

## 📊 Performance Optimization

### Build Optimization

```javascript
// vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          query: ['@tanstack/react-query'],
          ui: ['axios']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  }
});
```

### Caching Strategy

```javascript
// Service Worker for caching
const CACHE_NAME = 'athena-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});
```

## 🧪 Testing Deployment

### Pre-deployment Checklist

- [ ] All tests pass
- [ ] Build completes successfully
- [ ] Environment variables configured
- [ ] API endpoints accessible
- [ ] SSL certificates valid
- [ ] Domain DNS configured
- [ ] Monitoring setup

### Post-deployment Verification

```bash
# Health check
curl -I https://your-domain.com

# API connectivity
curl https://your-domain.com/api/health

# Performance test
lighthouse https://your-domain.com --output=json
```

## 📈 Monitoring and Analytics

### Error Tracking

```javascript
// Add Sentry for error tracking
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: process.env.VITE_SENTRY_DSN,
  environment: process.env.NODE_ENV
});
```

### Performance Monitoring

```javascript
// Add Google Analytics
import ReactGA from 'react-ga';

ReactGA.initialize('GA_TRACKING_ID');
ReactGA.pageview(window.location.pathname);
```

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Athena Frontend

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      - run: npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build
      - uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          working-directory: ./
```

## 🆘 Troubleshooting

### Common Issues

1. **Build fails**
   - Check Node.js version (16+)
   - Clear node_modules and reinstall
   - Verify environment variables

2. **API connection fails**
   - Check CORS configuration
   - Verify API endpoint URL
   - Test API directly with curl

3. **Tableau dashboard not loading**
   - Verify Tableau server URL
   - Check authentication tokens
   - Test embedding URL directly

4. **Salesforce sync issues**
   - Verify OAuth configuration
   - Check API permissions
   - Test Salesforce connection

### Debug Commands

```bash
# Check build output
npm run build --verbose

# Test API connectivity
curl -v http://localhost:5002/health

# Check environment variables
node -e "console.log(process.env)"

# Analyze bundle size
npm run build && npx vite-bundle-analyzer dist
```

---

**Athena Frontend Deployment** - Ready for production deployment! 🚀
