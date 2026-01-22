# Quick Start

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Usage

1. Enter a city name in the sidebar
2. Click "Analyze Climate"
3. View the results

## Run Tests

```bash
pytest tests/test_analysis.py -v
```

## Troubleshooting

**Command not found:**
- Make sure venv is activated (you should see `(venv)` in terminal)
- Try `python3` instead of `python` on macOS/Linux

**Import errors:**
- Check you're in the project root directory
- Verify dependencies: `pip list`
