# 🤖 AI Sales Intern (Ava)

An autonomous voice agent that scrapes real estate leads, matches them with potential buyers, makes calls, closes deals, and makes money while you sleep.

## 🌟 What It Does

This tool creates an AI-powered sales representative that:

1. **Scrapes real estate agent leads** from platforms like Realtor.com and Zillow
2. **Mines buyer intent signals** from Twitter, Reddit, and Facebook groups
3. **Matches buyers to agents** based on location and specialization
4. **Makes real phone calls** using natural-sounding AI voice
5. **Handles live conversations** with GPT-4 intelligence
6. **Closes sales autonomously** and logs everything to your dashboard
7. **Runs 24/7** - works while you sleep, doesn't take breaks, never complains

## 📋 Real-World Results

In a real test with real estate agents:
- 38 outbound calls
- 11 live conversations  
- 4 paid signups at $149 each
- $596 in revenue
- $578 profit after costs ($18 total for API calls)
- 10.5% conversion rate (3x industry average)
- TCPA compliant with clear disclosures

## 🚀 Quick Start for Beginners

### Step 1: Clone the Repository
```bash
git clone https://github.com/llSourcell/my_ai_intern.git
cd my_ai_intern
```

### Step 2: Set Up API Keys
Create a `.env` file in the `/backend` directory:

```
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_AGENT_ID=h3dC4sQ9cPDtYItAe0Z8
LLM_API_KEY=your_openai_api_key
BRIGHTDATA_API_TOKEN=your_brightdata_api_token
BRIGHTDATA_WEB_UNLOCKER_ZONE=your_zone_name
DB_TYPE=sqlite
DATABASE_URL=sqlite:///leads.db
```

Where to get API keys:
- **Twilio:** Sign up at [twilio.com](https://www.twilio.com) (provides phone capabilities)
- **ElevenLabs:** Sign up at [elevenlabs.io](https://elevenlabs.io) (provides realistic voices)
- **OpenAI:** Sign up at [openai.com](https://openai.com) (powers the AI conversations)
- **Bright Data:** Sign up at [brightdata.com](https://brightdata.com) - receive $10 free MCP credits (powers web scraping)

### Step 3: Install Dependencies

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

### Step 4: Run the Application

```bash
# Start the backend (from the backend directory)
python app.py

# In a new terminal, start the frontend (from the frontend directory)
npm start
```

The dashboard will open at `http://localhost:3000`

## 💡 How to Use

1. **Configure your API keys** in the dashboard settings
2. Click **"Scrape New Leads"** to gather real estate agents
3. The system will automatically match agents with potential buyers from social media
4. Select leads and click **"Call"** to initiate automated outreach
5. Monitor conversations and results in real-time
6. View call logs and transcripts for each lead

## 🛠️ Customization

### Lead Generation Process

1. **Scrape Real Estate Agents:** Uses Bright Data's MCP to pull agent data from Realtor.com and Zillow
   ```python
   # MCP servers provide stealth mode for bots - unblockable real-time web access
   # Using Bright Data's Web Unlocker to access agent listings
   agents = scrape_agents_via_mcp("Austin, TX", limit=100)
   ```

2. **Mine Buyer Intent:** Searches social media for people looking to buy/sell
   ```python
   # Search for posts like "Moving to Austin" or "Need a 3-bed in 78704"
   buyer_signals = mine_intent_signals(["twitter", "reddit", "facebook_groups"])
   ```

3. **Match Buyers to Agents:** Connects buyers with agents in the same areas
   ```python
   # Match based on zip code, property type, and specialization
   matched_leads = match_buyer_to_agent(buyer_signals, agents)
   ```

### Customize Sales Scripts

Modify the prompt in `voice.py` to change the sales approach:

```python
# Customize your sales script here
script = f"Hi {agent_name}, this is Ava from Home IQ. We've tracked {buyer_count} qualified buyers searching in {zip_code} right now. Would you like a list?"
```

## 🔍 Technical Details

- **Backend:** Flask, SQLite, Bright Data MCP for scraping
- **APIs:** Twilio (calls), ElevenLabs (voice), OpenAI (GPT-4 intelligence)
- **Frontend:** React with Tailwind UI
- **Performance:** Automated scheduling, call logging, analytics

### Bright Data MCP Integration

This project uses Bright Data's Model Context Protocol (MCP) servers for powerful web scraping:

- **Unblockable Access:** MCP servers provide stealth mode that can bypass CAPTCHAs and blocks
- **Global Coverage:** Access data from anywhere with worldwide IP coverage
- **AI-Ready Data:** Automatically formats extracted content for AI processing
- **Dynamic Content:** Handles JavaScript-rendered content effortlessly

```javascript
// Example MCP Server connection
const SBR_CDP = 'wss://brd-customer-CUSTOMER_ID-zone-ZONE_NAME:PASSWORD@brd.superproxy.io:9222';

async function scrapeAgents() {
    const browser = await pw.chromium.connectOverCDP(SBR_CDP);
    const page = await browser.newPage();
    await page.goto('https://www.realtor.com/realestateandhomes-search/Austin_TX/pg-1');
    // Extract agent data...
}
```

## 📊 Scaling Strategies

Once your MVP is working, consider these scaling approaches:

1. **Vertical expansion:** Target different industries (e-commerce, insurance, etc.)
2. **Recurring revenue:** Convert one-time sales ($149) to subscriptions ($99/month)
3. **Self-optimization:** Let the AI improve pitches based on call outcomes

## ⚠️ Legal Compliance

This tool is designed with TCPA compliance in mind:
- Each call opens with a clear disclosure
- Provides opt-out options
- Logs all interactions

Always verify regulations in your region before automated calling.

## 🤝 Need Help?

- Check the code examples in each file
- Consult the API documentation for [Twilio](https://www.twilio.com/docs), [ElevenLabs](https://docs.elevenlabs.io/), [OpenAI](https://platform.openai.com/docs), and [Bright Data](https://brightdata.com/docs)
- Open an issue on GitHub

---

Built with ❤️ using Flask, React, and AI APIs
