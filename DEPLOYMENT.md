# 🚀 Step-by-Step Deployment Guide: Render & Vercel

This document provides clear instructions for deploying the **KUBER Indian Monopoly** game to production using **Render** (FastAPI Backend with WebSockets) and **Vercel** (Next.js Frontend).

---

## 🛠️ Part 1: Deploy FastAPI Backend on Render

Render fully supports Python, FastAPI, and persistent WebSockets.

### Option A: Automatic Blueprint Deployment (Recommended)
1. Log in to [Render Dashboard](https://dashboard.render.com/).
2. Click **New +** $\rightarrow$ **Blueprint**.
3. Connect your GitHub repository: `https://github.com/Sri-Krishnan007/MONOPOLY`.
4. Render will automatically detect the [`render.yaml`](file:///c:/Sk%20PC/Exttra/MONOPOLY/render.yaml) file:
   - **Service Name:** `kuber-monopoly-backend`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Click **Apply**.
6. Once deployed, note down your backend URL (e.g., `https://kuber-monopoly-backend.onrender.com`).

### Option B: Manual Web Service Deployment
1. Go to [Render Dashboard](https://dashboard.render.com/) $\rightarrow$ **New +** $\rightarrow$ **Web Service**.
2. Select your repository `Sri-Krishnan007/MONOPOLY`.
3. Configure settings:
   - **Name:** `kuber-monopoly-backend`
   - **Runtime:** `Python 3`
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Choose the **Free** tier and click **Create Web Service**.

---

## ⚡ Part 2: Deploy Next.js Frontend on Vercel

### Steps:
1. Log in to your [Vercel Dashboard](https://vercel.com/).
2. Click **Add New...** $\rightarrow$ **Project**.
3. Import the GitHub repository: `Sri-Krishnan007/MONOPOLY`.
4. In the **Configure Project** screen:
   - **Framework Preset:** `Next.js`
   - **Root Directory:** Click *Edit* and select **`frontend`**.
5. Expand **Environment Variables** and add:
   | Variable Name | Value Example | Description |
   |---|---|---|
   | `NEXT_PUBLIC_API_URL` | `https://kuber-monopoly-backend.onrender.com` | Your Render Backend HTTPS URL |
   | `NEXT_PUBLIC_WS_URL` | `wss://kuber-monopoly-backend.onrender.com` | Your Render Backend WSS URL |
6. Click **Deploy**.
7. In ~60 seconds, your production site will be live at `https://monopoly-xxxx.vercel.app`!

---

## 🔍 Verification & Health Check

1. Test Backend: Visit `https://your-backend.onrender.com/api/board` in your browser. You should receive a JSON response with 40 Indian spaces.
2. Test Frontend: Open your Vercel URL, enter your name, pick a token (e.g. *Royal Elephant*), and click **"PLAY VS INDIAN AI TYCOONS"** to test live gameplay with WebSockets!
