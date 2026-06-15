# 🌟 Astral Algo — Algorithmic Forex Trading System

Elite algorithmic trading signals for prop firm traders. Real-time MetaTrader 5 integration, Telegram alerts, and live dashboard.

---

## 📋 Architecture

```
MT5 Terminal (VPS)
    └── AstralAlgo_SMC.mq5 (EA)
            │  HTTP POST (signals, updates, heartbeat)
            ▼
    Backend Server (Railway)
    └── main.py (FastAPI)
            ├── Supabase (database)
            ├── Telegram Bot (alerts)
            └── WebSocket (live push to website)
                    │
                    ▼
            Website (Vercel)
            └── astroalgo.html (live dashboard)
```

---

## 🚀 Quick Deployment

### **Option 1: Frontend to Vercel** (Static HTML)

1. **Sign up at [vercel.com](https://vercel.com)**
2. **Connect your GitHub repository**
3. **Vercel auto-detects and deploys** `astroalgo.html` to your domain
4. **Your frontend is LIVE** 🎉

**Result:** `https://astroalgo-bot.vercel.app` (or custom domain)

---

### **Option 2: Backend to Railway** (Python FastAPI)

1. **Sign up at [railway.app](https://railway.app)**
2. **Connect your GitHub repository**
3. **Railway auto-detects `Dockerfile` and deploys**
4. **Set environment variables** in Railway dashboard

#### Environment Variables (Railway):
```
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-key
TELEGRAM_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
EA_SECRET=astral_algo_secret_2026
ALLOWED_ORIGINS=https://astroalgo-bot.vercel.app
DAILY_SUMMARY_HOUR=23
DAILY_SUMMARY_MIN=50
```

**Result:** `https://your-railway-app.up.railway.app` (auto-assigned)

---

## 🔧 Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/timothymaturlu-dot/astroalgo_bot.git
   cd astroalgo_bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase, Telegram, etc.
   ```

5. **Run backend**
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Open frontend**
   ```
   http://localhost:8000/astroalgo.html
   ```
   or open `astroalgo.html` directly in your browser (local mode, no WebSocket)

---

## 📡 API Endpoints

### **From MT5 EA → Backend**

#### Send Signal
```http
POST /ea/signal
Header: X-EA-Secret: astral_algo_secret_2026
Body: {
  "symbol": "XAUUSD",
  "direction": "BUY",
  "entry": 2341.50,
  "sl": 2332.00,
  "tp1": 2354.00,
  "tp2": 2368.00,
  "tp3": 2385.00,
  "lots": 0.25,
  "rr": 2.4,
  "confidence": 92.0,
  "session": "New York Kill Zone",
  "confluences": "HTF Bias ✓ | MSB ✓ | Liq Sweep ✓ | OB ✓",
  "magic": 20260612
}
```

#### Trade Update
```http
POST /ea/trade-update
Header: X-EA-Secret: astral_algo_secret_2026
Body: {
  "signal_id": "sig_001",
  "ticket": 123456,
  "symbol": "XAUUSD",
  "direction": "BUY",
  "status": "TP1_HIT",
  "exit_price": 2354.00,
  "pnl_pips": 82,
  "pnl_usd": 205.00,
  "magic": 20260612
}
```

#### Account Snapshot
```http
POST /ea/account
Header: X-EA-Secret: astral_algo_secret_2026
Body: {
  "magic": 20260612,
  "balance": 50000,
  "equity": 51240,
  "margin": 1200,
  "free_margin": 49040,
  "daily_dd_pct": 1.2,
  "total_dd_pct": 3.8,
  "open_trades": 3,
  "daily_pnl_usd": 620,
  "daily_pnl_pct": 1.24,
  "server_time": "2026-06-15T14:30:00Z"
}
```

#### Heartbeat
```http
POST /ea/heartbeat
Header: X-EA-Secret: astral_algo_secret_2026
Body: {
  "magic": 20260612,
  "symbol": "XAUUSD",
  "uptime_sec": 86400,
  "in_session": true,
  "bias": "BULLISH",
  "spread": 3.2
}
```

### **From Website → Backend**

#### Get Signals
```http
GET /signals?limit=20&status=ACTIVE&symbol=XAUUSD
Response: {
  "signals": [...],
  "count": 20
}
```

#### Get Performance
```http
GET /performance?days=30
Response: {
  "period_days": 30,
  "total_signals": 148,
  "closed_trades": 132,
  "wins": 114,
  "losses": 18,
  "win_rate_pct": 86.4,
  "total_pips": 4812.0,
  "total_pnl_usd": 9624.0,
  "by_symbol": {...}
}
```

#### WebSocket Connection
```javascript
const ws = new WebSocket('wss://your-railway-app.up.railway.app/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'new_signal') {
    // Handle new signal
  } else if (data.type === 'trade_update') {
    // Handle trade update
  } else if (data.type === 'account_update') {
    // Handle account update
  }
};
```

#### Health Check
```http
GET /health
Response: {
  "status": "ok",
  "version": "2.4.0",
  "db": "connected",
  "telegram": "configured",
  "ws_clients": 5
}
```

---

## 🎯 MT5 EA Configuration

In your **Astroalgo_SMC.mq5** EA inputs, set:

```
ServerURL = "https://your-railway-app.up.railway.app"
ServerSecret = "astral_algo_secret_2026"
```

---

## 📊 Database Setup (Supabase)

Create these tables in your Supabase database:

### **signals** table
```sql
CREATE TABLE signals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  symbol TEXT NOT NULL,
  direction TEXT NOT NULL,
  entry FLOAT NOT NULL,
  sl FLOAT NOT NULL,
  tp1 FLOAT NOT NULL,
  tp2 FLOAT NOT NULL,
  tp3 FLOAT NOT NULL,
  lots FLOAT NOT NULL,
  rr FLOAT NOT NULL,
  confidence FLOAT NOT NULL,
  session TEXT,
  confluences TEXT,
  magic INT NOT NULL,
  account_size FLOAT,
  risk_pct FLOAT,
  propfirm_mode BOOLEAN DEFAULT true,
  status TEXT DEFAULT 'ACTIVE',
  pips_gained FLOAT DEFAULT 0,
  pnl_usd FLOAT DEFAULT 0,
  created_at TIMESTAMP DEFAULT now(),
  closed_at TIMESTAMP
);
```

### **account_snapshots** table
```sql
CREATE TABLE account_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  magic INT NOT NULL,
  balance FLOAT NOT NULL,
  equity FLOAT NOT NULL,
  margin FLOAT NOT NULL,
  free_margin FLOAT NOT NULL,
  daily_dd_pct FLOAT NOT NULL,
  total_dd_pct FLOAT NOT NULL,
  open_trades INT NOT NULL,
  daily_pnl_usd FLOAT NOT NULL,
  daily_pnl_pct FLOAT NOT NULL,
  server_time TIMESTAMP,
  recorded_at TIMESTAMP DEFAULT now()
);
```

---

## 🔐 Security

- **X-EA-Secret Header:** All MT5 → Backend requests must include `X-EA-Secret` header
- **CORS Enabled:** Frontend can call backend API
- **Supabase RLS:** Implement row-level security for sensitive data
- **Environment Variables:** Store all secrets in `.env` (never commit!)

---

## 📱 Telegram Bot Setup

1. **Create a Telegram Bot:**
   - Chat with [@BotFather](https://t.me/BotFather) on Telegram
   - Type `/newbot` and follow instructions
   - Copy your **bot token**

2. **Get Your Chat ID:**
   - Create a Telegram group or use DM
   - Add your bot to the group
   - Go to: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - Find `chat.id` in the response
   - Use that as `TELEGRAM_CHAT_ID`

3. **Set Environment Variables:**
   ```
   TELEGRAM_TOKEN=your-bot-token-here
   TELEGRAM_CHAT_ID=your-chat-id-here
   ```

---

## 📈 Features

✅ **Real-time Signal Delivery** — WebSocket push to all connected dashboards  
✅ **Telegram Alerts** — Instant notifications for signals, TP hits, SL hits  
✅ **PropFirm Compliance** — Built-in drawdown & risk monitoring  
✅ **Live Dashboard** — Professional signal tracker & performance stats  
✅ **Multi-Session** — London, NY, Asia coverage  
✅ **Scheduled Jobs** — Daily summaries, health checks  
✅ **Mock Mode** — Test without Supabase connected  

---

## 🛠️ Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check ports
lsof -i :8000  # Is 8000 already in use?
```

### WebSocket connection fails
- Ensure backend is running on correct URL
- Check CORS settings in `main.py`
- Verify `ALLOWED_ORIGINS` in `.env`

### Telegram messages not sending
- Verify `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID`
- Test with: `https://api.telegram.org/bot<TOKEN>/getMe`
- Add bot to your group/channel

---

## 📞 Support

For issues or questions:
- Check logs: `tail -f astralalgo.log`
- Test endpoints: Use Postman or `curl`
- Health check: `GET /health`

---

## 📄 License

Proprietary © 2026 Astral Algo. All rights reserved.

---

**Ready to trade? Deploy now and start receiving signals! 🚀**
