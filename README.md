# 🌍 Travel Whisperer

**Travel Whisperer** is an AI agent built during **bunq Hackathon 6.0** to help users understand their travel spending, set personalized savings goals, and discover relevant bunq tools.

> 💸 “You've spent €1,200 in France across 3 trips — time to start saving for Portugal?”

---

## 🎤 Why It Matters

**Travel Whisperer** is more than a finance bot — it's your joyful travel planner, powered by AI. By analyzing past spending, it recommends personalized destinations, savings plans, and built-in bunq tools like Travel Insurance or AutoSave. The result? More travel, happier bunqers — and more smart activations that drive value for bunq. This is AI that makes memories, not just margins.

---

## 🎯 What It Does

- ✈️ Detects travel patterns from your bunq transaction history  
- 🧠 Generates savings plans and travel suggestions using GPT-4  
- 🗺️ Visualizes spending by country and over time  
- 🛠️ Recommends bunq features like Travel Insurance, AutoSave, and sub-accounts  
- 🔗 Links to Together articles and deeplinks for in-app actions  

> _"More travel, happier bunqers. More travel insurance, smarter monetization."_ 💼✈️🎉

---


## 🎥 Demo

**Watch the walkthrough video:**  
📺 [👉 Click here to view the demo](https://your-demo-link.com)

---

## 🗃️ Dataset

This project uses a sample dataset provided by **bunq tech support via the Slack hackathon channel (2024 edition)**.

It includes:

- 🧾 Transactions  
- 💳 Monetary accounts  
- 💼 Cards  
- 📍 Activities (visited places)  
- 📚 Together topics (knowledge base)  
- 🔗 Deeplinks (in-app redirection URLs)


---

## 🛠️ Tech Stack

| Tool              | Purpose                                      |
|-------------------|----------------------------------------------|
| Python 🐍         | Backend logic and data handling              |
| Streamlit ⚡      | Interactive UI                               |
| OpenAI GPT-4 🤖    | AI recommendations + embeddings              |
| Plotly 📊         | Interactive visualizations (maps, charts)    |
| pandas + numpy 🧮 | Data manipulation                            |
| bunq API 🔗       | Account & transaction data (API-ready)       |

---

## 📁 Project Structure

```
Travel-Whisperer/
├── streamlit_app.py          # Main Streamlit interface
├── agent/                    # AI agent logic and helpers
├── scripts/                  # Embedding + user context scripts
├── data/                     # Cleaned bunq transaction exports
├── requirements.txt
└── README.md

```

---

## 🚀 Features

- 🌍 Travel map (choropleth) by country  
- 📆 Timeline of travel spending over time  
- 🤖 GPT-4 travel savings recommendations  
- 🔗 Auto-linked Together articles + deeplinks  
- 🧭 Travel goal input field with AI planning  

---

## 🧪 Getting Started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your OpenAI API key
export OPENAI_API_KEY=your-api-key-here

# 3. Run the app
streamlit run streamlit_app.py
```

---

## 📝 To-Do (Post-Hackathon)

- [ ] Integrate live bunq API (instead of CSVs)  
- [ ] Add bunq OAuth login  
- [ ] Integrate with AWS and Nvidia SDKs
- [ ] Clean and optimize the agent codebase  
- [ ] Fine-tune AI agents for more accurate personalization
- [ ] Embed deeplinks dynamically into text  
- [ ] Embed deeplinks dynamically into text  
- [ ] Mobile-friendly layout and PWA support  
- [ ] Chat-style interface with memory  

---

## 👥 Author

Built by **Samane Ahangar**  
🧠 Submitted to **[bunq Hackathon 6.0](https://developer.bunq.com/)**

---

## 📄 License

MIT License. Free to fork, remix, and build upon.
