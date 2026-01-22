# 🚀 Quick Start Guide

## Step 1: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Run the Application

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## Step 4: Use the App

1. Enter a city name in the sidebar (e.g., "New York", "London", "Tokyo")
2. Click "🔍 Analyze Climate" button
3. View the anomaly analysis and visualizations

## Optional: Run Tests

```bash
pytest tests/test_analysis.py -v
```

## Troubleshooting

**If you get "command not found" errors:**
- Make sure your virtual environment is activated (you should see `(venv)` in your terminal)
- Try using `python3` instead of `python` if on macOS/Linux

**If Streamlit doesn't open automatically:**
- Copy the URL from the terminal (usually `http://localhost:8501`)
- Paste it into your browser

**If you get import errors:**
- Make sure you're in the project root directory
- Verify all dependencies are installed: `pip list`
