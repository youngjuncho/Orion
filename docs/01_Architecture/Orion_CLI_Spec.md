# Orion CLI Specification

Version: 1.0

Status: Draft

Last Updated: 2026-06-23

Depends On:

* Orion_Operating_Architecture.md

---

# Purpose

This document defines the command-line interface of Orion OS.

---

# Root Command

```bash
orion
```

---

# Framework Commands

Moon

```bash
orion moon
```

Aurora

```bash
orion aurora
```

Supernova

```bash
orion supernova
```

Phoenix

```bash
orion phoenix
```

---

# Dashboard Command

```bash
orion dashboard
```

---

# Data Commands

Update all data:

```bash
orion data update
```

Check status:

```bash
orion data status
```

---

# Moon Commands

```bash
orion moon run

orion moon report

orion moon allocation
```

---

# Aurora Commands

```bash
orion aurora report

orion aurora regime

orion aurora indicators
```

---

# Supernova Commands

```bash
orion supernova report

orion supernova leaders

orion supernova watchlist
```

---

# Phoenix Commands

```bash
orion phoenix report

orion phoenix leaders

orion phoenix categories
```

---

# System Commands

Version:

```bash
orion version
```

Health Check:

```bash
orion health
```

Configuration:

```bash
orion config
```

---

# Future Extensions

Potential support:

* notifications
* automation
* AI commentary

---

# Next Document

Orion_Dashboard_Spec.md
