<div align="center">

# 💹 TrackIt

**A modular, database-driven personal finance tracker built with Flask.**

<p>
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" />
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" />
<img src="https://img.shields.io/badge/Jinja2-B41717?style=flat-square&logo=jinja&logoColor=white" />
<img src="https://img.shields.io/badge/Deployed-Render-46E3B7?style=flat-square&logo=render&logoColor=white" />
</p>

[**🔗 Live App**](https://trackit-nk.onrender.com)

</div>

---

## 📖 About

TrackIt is a personal finance tracking web app — but the real goal behind it wasn't the feature list. It was understanding **how production-style backend systems are actually structured**: API design, authentication flows, database persistence, and architecture that doesn't fall apart when it scales.

This project marks the shift from writing standalone scripts to designing systems with intent — clean separation of concerns, modular routing, and backend practices that mirror how real applications get built.

---

## 🏗️ Architecture Highlights

| Principle | How it's applied |
|---|---|
| **Modular routing** | Flask Blueprints separate concerns instead of one monolithic `app.py` |
| **Structured folders** | Clear separation by responsibility for long-term maintainability |
| **Session-based auth** | Secure, server-side session management — no token sprawl for a project this size |
| **REST-style endpoints** | Predictable, resource-oriented API design |
| **DB-driven persistence** | All state lives in PostgreSQL, not in memory or flat files |
| **Scalability-minded** | Architecture chosen to extend cleanly, not just to ship fast |

---

## ✨ Features

- 🔐 User authentication — register & login
- 🔒 Secure, session-based access control
- 💰 Add, view, and manage income records
- 💸 Add, view, and manage expense records
- 📊 Monthly financial summary
- 🧩 Reusable Jinja2 template structure

---

## 🧰 Tech Stack

```
Backend       Python · Flask
Database      PostgreSQL
Templating    Jinja2
Frontend      HTML · CSS
Deployment    Render
```

---

## 🌍 Deployment

Deployed on **Render** to simulate a real production backend environment — not just a local demo. The deployment process covered:

- Environment variable configuration
- Secure database connectivity
- Production-ready backend behavior under real hosting constraints

**Live:** [trackit-nk.onrender.com](https://trackit-nk.onrender.com)

---

## 🔜 Next Steps

- [ ] Integrate ML-based expense analysis
- [ ] Surface intelligent financial insights from spending patterns
- [ ] Refine API structure to support future scaling

---

## 📌 Learning Focus

This project was less about *"can I build a finance tracker"* and more about *"can I structure a backend the way real systems are structured."* Blueprint-based modularity, session auth, and a REST-style API layer were deliberate choices — practice for engineering systems that hold up beyond a single script.

---

<div align="center">

**Built by [Nithish Kumar](https://github.com/nithishkumar-dev-10)**

</div>
