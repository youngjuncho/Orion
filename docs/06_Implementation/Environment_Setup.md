# Orion Environment Setup

Version: 1.0

Status: Draft

Last Updated: 2026-07-26

---

# Purpose

Defines the recommended development environment for Orion OS.

---

# Python Version

Recommended:

```text id="uqef7g"
Python 3.10+
```

The current Windows development environment uses Python 3.10 through a conda environment named `orion`.

Future production environments may standardize on a newer Python version after dependency compatibility is reviewed.

---

# Local Development Environment

Recommended:

```powershell
conda activate orion
```

Verify:

```powershell
python -c "import sys; print(sys.executable)"
```

Expected local interpreter:

```text
C:\Users\yj44c\anaconda3\envs\orion\python.exe
```

VSCode should use the same interpreter.

---

# Alternative Virtual Environment

For non-conda environments:

```bash id="w30dsy"
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\activate
```

Activate on Linux or macOS:

```bash id="j25e74"
source .venv/bin/activate
```

---

# Install Dependencies

```bash id="5km40o"
pip install -r requirements.txt
```

---

# Initial Packages

Core

```text id="8kfx43"
pandas
numpy
pyyaml
```

---

Data

```text id="5vjrfv"
yfinance
requests
fredapi
```

---

Visualization

```text id="sx5rj4"
streamlit
plotly
```

---

Testing

```text id="jst9nw"
pytest
```

---

# Environment Variables

Create:

```text id="hlbbq2"
.env
```

Examples:

```text id="xgdbvj"
FRED_API_KEY=

CRYPTOQUANT_API_KEY=
```

---

# Development Startup

Update Data

```bash id="uhqy95"
orion data update
```

Run Dashboard

```powershell
$env:PYTHONPATH = "src"
python -m orion.cli dashboard
```

---

# Future Environment

Potential support:

* Docker
* PostgreSQL
* FastAPI
* React
