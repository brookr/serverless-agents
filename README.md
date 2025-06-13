# Serverless Agent Architecture Starter

A production-ready starter project demonstrating how to build full-stack applications with AI agents deployed to Vercel, orchestrated by Inngest, and powered by Next.js 15. This architecture pattern enables you to build scalable AI-powered applications with long-running workflows.

🔗 **GitHub Repository**: [https://github.com/brookr/serverless-agents](https://github.com/brookr/serverless-agents)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fbrookr%2Fserverless-agents&env=OPENAI_API_KEY,NEWSLETTER_READ_WRITE_TOKEN&envDescription=Configure%20your%20AI%20agents%20and%20storage&envLink=https%3A%2F%2Fgithub.com%2Fbrookr%2Fserverless-agents%23environment-setup&project-name=serverless-agents&repository-name=serverless-agents)

⚠️ **Important**: After deploying, you must configure the Inngest integration in Vercel. See [Deployment Instructions](#-deployment) for details.

![Architecture Pattern](public/newspaper-icon.svg)

## 🏗️ Architecture Pattern

This starter demonstrates a modern serverless architecture for AI applications:

- **AI Agents as Vercel Functions**: Python FastAPI agents that deploy as serverless functions
- **Next.js Frontend**: Modern React application with App Router
- **Inngest Orchestration**: Reliable workflow management for long-running AI tasks
- **Vercel Blob Storage**: Persistent storage for generated content
- **Two-Stage Processing**: Separation of concerns with research and formatting agents

## 🎯 Why This Architecture?

This pattern solves common challenges in AI application development:

- **Serverless Scalability**: Agents scale automatically with demand
- **Long-Running Jobs**: Inngest handles workflows that exceed typical timeout limits
- **Cost Efficiency**: Pay only for actual usage, no idle servers
- **Developer Experience**: Local development mirrors production exactly
- **Type Safety**: Full TypeScript support across the stack

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- OpenAI API key
- Vercel account (free tier works)

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/brookr/serverless-agents.git
cd serverless-agents

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env.local` file:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
NEWSLETTER_READ_WRITE_TOKEN=your_vercel_blob_token

# Optional (Inngest will auto-generate if not provided)
INNGEST_SIGNING_KEY=your_inngest_signing_key
```

### 3. Run Development Servers

You'll need three terminals:

**Terminal 1 - Python Agent Server:**

```bash
uvicorn api.agents:app --reload --reload-dir api --port 8000
```

**Terminal 2 - Next.js Development:**

```bash
npm run dev
```

**Terminal 3 - Inngest Dev Server:**

```bash
npx inngest-cli@latest dev --no-discovery -u http://localhost:3000/api/inngest
```

### 4. Access the Application

- **Main App**: http://localhost:3000
- **Python API**: http://localhost:8000
- **Inngest Dashboard**: http://localhost:8288

## 📁 Project Structure

```text
├── src/
│   ├── app/                      # Next.js app directory
│   │   ├── api/
│   │   │   ├── inngest/         # Inngest webhook endpoint
│   │   │   └── newsletter/      # API routes for the example app
│   │   └── newsletter/
│   │       └── [slug]/          # Dynamic pages
│   ├── components/              # React components
│   │   └── ui/                  # shadcn/ui components
│   ├── inngest/
│   │   ├── client.ts           # Inngest client configuration
│   │   └── functions.ts        # Workflow definitions
│   └── lib/
│       └── *.ts                # Utilities and helpers
├── api/
│   └── agents.py               # FastAPI agent definitions
├── public/                     # Static assets
├── vercel.json                # Vercel routing configuration
├── requirements.txt            # Python dependencies
└── package.json               # Node.js dependencies
```

## 🔧 Core Components

### 1. AI Agents (FastAPI + Vercel Functions)

The `api/agents.py` file demonstrates how to structure AI agents:

```python
# Example agent structure
research_agent = Agent(
    name="Research Agent",
    model="gpt-4.1",
    instructions="...",
    tools=[WebSearchTool()]
)

@app.post("/research")
async def research_endpoint(request: TopicsRequest):
    # Agent logic here
```

### 2. Inngest Workflows

The `src/inngest/functions.ts` shows how to orchestrate long-running tasks:

```typescript
export const generateNewsletter = inngest.createFunction(
  { id: "generate-newsletter" },
  { event: "newsletter/generate" },
  async ({ event, step }) => {
    // Multi-step workflow with retries and error handling
  }
);
```

### 3. Next.js Integration

API routes in `src/app/api/` demonstrate the integration pattern:

- Webhook endpoint for Inngest
- Status checking endpoints
- Trigger endpoints for workflows

### 4. Vercel Configuration

The `vercel.json` file is critical for proper Python API routing. Build python after NextJS, and configure the routes to point to the python file:

```json
{
  "builds": [
    { "src": "package.json", "use": "@vercel/next" },
    { "src": "api/agents.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "^/api/agents/(.*)", "dest": "/api/agents.py" },
    { "src": "^/api/agents$", "dest": "/api/agents.py" }
  ]
}
```

This configuration ensures that all `/api/agents/*` paths are routed to your Python FastAPI application.

## 🎨 Customizing for Your Use Case

This starter uses a newsletter generator as an example, but the architecture supports any AI-powered application:

### Common Patterns

1. **Document Processing**
   - Replace newsletter generation with document analysis
   - Use multiple agents for extraction, summarization, etc.

2. **Data Pipeline**
   - Implement ETL workflows with AI enhancement
   - Chain multiple processing steps

3. **Content Generation**
   - Build blog post generators, report writers, etc.
   - Add review and approval workflows

4. **Multi-Modal Applications**
   - Integrate image generation APIs
   - Process audio/video with AI agents

### Key Files to Modify

- `api/agents.py` - Define your AI agents and their capabilities
- `src/inngest/functions.ts` - Create your workflow logic
- `src/app/api/` - Add your API endpoints
- `src/app/` - Build your UI

## 🚢 Deployment

### One-Click Deploy with Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fbrookr%2Fserverless-agents&env=OPENAI_API_KEY,NEWSLETTER_READ_WRITE_TOKEN&envDescription=Configure%20your%20AI%20agents%20and%20storage&envLink=https%3A%2F%2Fgithub.com%2Fbrookr%2Fserverless-agents%23environment-setup&project-name=serverless-agents&repository-name=serverless-agents)

1. **Click the Deploy Button**
   - This will fork the repository to your GitHub account
   - You'll be prompted to enter the required environment variables:
     - `OPENAI_API_KEY` - Your OpenAI API key
     - `NEWSLETTER_READ_WRITE_TOKEN` - Generate this in Vercel Blob storage settings

2. **Configure Inngest Integration** ⚠️ **Critical Step**

   After deployment completes:
   - Go to your new project in the Vercel dashboard
   - Navigate to **Settings** → **Integrations**
   - Search for and install the **Inngest** integration
   - Follow the setup wizard to connect your Inngest account
   - This automatically adds `INNGEST_EVENT_KEY` and `INNGEST_SIGNING_KEY`

   **Note**: Without this step, the API routes will return 404 errors!

3. **Redeploy Your Project**
   - After installing Inngest, go to the **Deployments** tab
   - Click the three dots menu on the latest deployment
   - Select **Redeploy**
   - Wait for the deployment to complete

4. **Verify Everything Works**
   - Visit your deployed site
   - Try generating a newsletter
   - Check that all API endpoints respond:
     - `/api/newsletter/[slug]` - Newsletter generation
     - `/api/agents/ping` - Python API health check
     - `/api/agents/research` - AI research agent
     - `/api/agents/format` - AI formatting agent
     - `/api/inngest` - Inngest webhook

### Manual Deployment

If you prefer to deploy manually:

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/serverless-agents
cd serverless-agents

# Login to Vercel
vercel login

# Deploy (you'll be prompted for env vars)
vercel --prod
```

Then follow steps 2-4 above to configure Inngest.

### Environment Variables Reference

| Variable | Description | When Added |
|----------|-------------|------------|
| `OPENAI_API_KEY` | OpenAI API key for AI agents | During deployment |
| `NEWSLETTER_READ_WRITE_TOKEN` | Vercel Blob storage token | During deployment |
| `INNGEST_EVENT_KEY` | Event security key | Auto-added by Inngest |
| `INNGEST_SIGNING_KEY` | Webhook signing key | Auto-added by Inngest |

### Troubleshooting

- **404 on API routes**: Make sure you've installed the Inngest integration and redeployed
- **500 on Python agents**: Check that `OPENAI_API_KEY` is set correctly
- **Newsletter not generating**: Verify all environment variables are present in Vercel dashboard

## 🔍 Understanding the Architecture

### Request Flow

1. **User Interaction** → Next.js frontend
2. **API Route** → Triggers Inngest workflow
3. **Inngest Function** → Orchestrates the process
4. **Agent Calls** → Vercel Functions execute AI tasks
5. **Storage** → Results saved to Vercel Blob
6. **Response** → User sees the result

### Why Inngest?

- **Reliability**: Automatic retries and error handling
- **Observability**: Built-in monitoring and debugging
- **Scalability**: Handles thousands of concurrent workflows
- **Developer Experience**: Great local development tools

### Why Vercel Functions for Agents?

- **Zero Config**: Python agents deploy automatically
- **Auto-scaling**: Handle any load without infrastructure management
- **Cost Effective**: Pay per execution, not for idle time
- **Global Edge**: Deploy close to your users

## 📄 License

This project is licensed under CC0 1.0 Universal - see the [LICENSE.md](LICENSE.md) file.

## 📚 Learn More

### Architecture Components

- [Next.js Documentation](https://nextjs.org/docs)
- [Inngest Documentation](https://www.inngest.com/docs)
- [Vercel Functions](https://vercel.com/docs/functions)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### Related Patterns

- [Serverless AI Patterns](https://vercel.com/guides/serverless-ai-patterns)
- [Long-Running Jobs with Inngest](https://www.inngest.com/docs/guides/long-running-jobs)
- [Python on Vercel](https://vercel.com/docs/functions/runtimes/python)

## 🎯 Next Steps

1. **Explore the Code**: Start with `api/agents.py` and `src/inngest/functions.ts`
2. **Run Locally**: Get the development environment running
3. **Modify for Your Use Case**: Replace the newsletter example with your own AI workflow
4. **Deploy**: Push to production on Vercel
5. **Share**: Let us know what you build!

### 🤝 Contributing

We welcome contributions! See our [Contributing Guidelines](CONTRIBUTING.md) for details.

📦 **Repository**: [https://github.com/brookr/serverless-agents](https://github.com/brookr/serverless-agents)

### Contributors

Author: [@brookr](https://github.com/brookr)

Contributors:

- [@chrisg220](https://github.com/chrisg220)
- YOUR NAME HERE!

---

Built as a reference architecture for modern AI applications. Use this as a starting point for your own serverless agent projects.
