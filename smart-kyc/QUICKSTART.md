# Quick Start Guide - Smart KYC Screener

Get the demo running in **under 5 minutes**.

---

## Step 1: Install Dependencies

### Backend
```bash
cd backend
pip install -r requirements.txt
```

### Frontend
```bash
cd frontend
npm install
```

---

## Step 2: Start Services

### Terminal 1: Backend
```bash
cd backend
python main.py
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

**Expected Output:**
```
ready - started server on 0.0.0.0:3000
```

---

## Step 3: Open Browser

Navigate to: **http://localhost:3000**

---

## Step 4: Run the Demo

### Quick Test (30 seconds)

1. **Upload CSV**
   - Click "CSV Batch" tab
   - Drag `backend/data/applicants.csv` or click "Choose File"
   - Wait 2-3 seconds for processing

2. **View Results**
   - See 5 applicants screened
   - Note decisions: 2 Approved, 2 Review, 1 Blocked

3. **Inspect a Case**
   - Click "View Details" on Vladimir Petrov
   - See match score: 100%
   - See adverse media: 2 articles

4. **Check Metrics**
   - Click "Metrics" tab
   - See breakdown: 40% Approved, 40% Review, 20% Blocked

**Done!** ✅

---

## Step 5: Try Advanced Features

### Teach a New Rule
1. Click "View Details" on any case
2. Click "Teach New Rule" button
3. Fill in:
   - Rule ID: `test_rule`
   - Description: "Test rule for demo"
   - Outcome: REVIEW
   - Add condition: `country` equals `USA`
4. Click "Add Rule"
5. Re-upload CSV to see the rule in action

### Upload ID Document
1. Switch to "ID Document" tab
2. Upload any passport/license image
3. See extracted fields with bounding boxes

### View Reports
1. Select a REVIEW or BLOCK case
2. Click "Reports" tab
3. See auto-generated EDD and SAR drafts

---

## Troubleshooting

### Backend won't start
- **Error:** `ModuleNotFoundError`
- **Fix:** Run `pip install -r requirements.txt` in backend folder

### Frontend won't start
- **Error:** `Cannot find module`
- **Fix:** Run `npm install` in frontend folder

### CORS errors
- **Error:** `Access-Control-Allow-Origin`
- **Fix:** Backend is configured for CORS. Ensure backend is running on port 8000

### No data showing
- **Check:** Backend is running on http://localhost:8000
- **Check:** Frontend is running on http://localhost:3000
- **Check:** CSV file exists at `backend/data/applicants.csv`

---

## API Health Check

Test backend is running:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","timestamp":"2025-10-03T..."}
```

---

## Next Steps

- Read the full [DEMO_SCRIPT.md](./DEMO_SCRIPT.md) for the 90-second walkthrough
- Check [README.md](./README.md) for detailed documentation
- Explore the API at http://localhost:8000/docs (FastAPI auto-docs)

---

**Happy Screening!** 🛡️
