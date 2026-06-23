# Orion Environment Setup

Version: 1.0

Status: Draft

Last Updated: 2026-06-23

---

# Purpose

Defines the recommended development environment for Orion OS.

---

# Python Version

Recommended:

```text id="uqef7g"
Python 3.12+
```

---

# Virtual Environment

Recommended:

```bash id="w30dsy"
python -m venv .venv
```

---

Activate:

Windows

```bash id="waf88y"
.venv\Scripts\activate
```

Linux / macOS

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

```bash id="2v7sre"
streamlit run src/dashboard/app.py
```

---

# Future Environment

Potential support:

* Docker
* PostgreSQL
* FastAPI
* React
