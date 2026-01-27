#!/bin/bash

# Create directory structure
mkdir -p frontend/app backend/app

# Create backend files
cat << 'EOF' > backend/requirements.txt
fastapi
uvicorn
playwright
google-generativeai
sqlalchemy
EOF

cat << 'EOF' > backend/app/main.py
from fastapi import FastAPI
from .scraper import scrape_trends
from .analyzer import analyze_trend

app = FastAPI()

@app.get("/api/trends")
async def get_trends():
    video_data = await scrape_trends()
    analysis = await analyze_trend(video_data)
    return {"analysis": analysis}
EOF

cat << 'EOF' > backend/app/scraper.py
import json
from playwright.async_api import async_playwright

async def load_auth_cookies(page, platform):
    """Loads authentication cookies from a JSON file for a given platform."""
    try:
        with open(f"{platform}_cookies.json", 'r') as f:
            cookies = json.load(f)
            await page.context.add_cookies(cookies)
            return True
    except FileNotFoundError:
        print(f"Cookie file for {platform} not found. Scraping without authentication.")
        return False

async def scrape_trends():
    """
    Scrapes video descriptions from TikTok and Instagram Reels.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # It's important to use stealth mode to avoid detection
        # This is a simplified example. Real-world scraping requires more robust techniques.
        # await stealth_async(page)

        # Scrape TikTok
        await page.goto("https://www.tiktok.com/foryou")
        # NOTE: You would need to implement login logic or cookie loading here
        # For this example, we'll just grab some text
        tiktok_descriptions = await page.eval_on_selector_all(".tiktok-video-meta-title", "elements => elements.map(e => e.innerText)")


        # Scrape Instagram Reels
        await page.goto("https://www.instagram.com/reels/")
        # NOTE: You would need to implement login logic or cookie loading here
        # For this example, we'll just grab some text
        reels_descriptions = await page.eval_on_selector_all("._aajw", "elements => elements.map(e => e.innerText)")

        await browser.close()
        return tiktok_descriptions + reels_descriptions
EOF

cat << 'EOF' > backend/app/analyzer.py
import google.generativeai as genai
import os

async def analyze_trend(video_data):
    """
    Analyzes a list of video descriptions using the Gemini API to identify trends.
    """
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Analyze the following video descriptions from TikTok and Instagram Reels.
        Based on this data, answer the following questions:
        1. What is the emerging trend?
        2. Why is this trend going viral right now?
        3. Who is the target audience for this trend?

        Video Descriptions:
        {video_data}
        """
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during analysis: {e}"

EOF

# Create frontend files
cat << 'EOF' > frontend/app/page.tsx
"use client";

import { useState, useEffect } from 'react';

export default function Home() {
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        const res = await fetch('/api/trends');
        const data = await res.json();
        setAnalysis(data.analysis);
      } catch (error) {
        console.error('Error fetching trends:', error);
        setAnalysis('Failed to fetch trend analysis.');
      } finally {
        setLoading(false);
      }
    };

    fetchTrends();
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 w-full max-w-5xl items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl font-bold text-center">TrendHunter AI</h1>
      </div>

      <div className="mt-12 w-full max-w-5xl">
        <div className="grid grid-cols-1 gap-4">
          <div className="rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30">
            <h2 className="mb-3 text-2xl font-semibold">
              Trend Analysis
            </h2>
            {loading ? (
              <p>Loading analysis...</p>
            ) : (
              <p className="m-0 max-w-[30ch] text-sm opacity-50">
                {analysis}
              </p>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
EOF

# Make the script executable
chmod +x setup.sh

echo "Setup script created successfully. Run './setup.sh' to generate the project files."
