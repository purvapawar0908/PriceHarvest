# 🌾 PriceHarvest — Crop Price Analysis & Trend Identification

**BTech Mini Project | Data Science | SNDT Women's University**  
**Phase 1: EDA, Time-Series Analysis & Interactive Dashboard**

---

## 👥 Team

| Name | Roll No | Contribution |
|---|---|---|
| Sakshi Jagdish Patil | 51 | Data preprocessing, EDA, seasonal trend analysis |
| Purva Atul Pawar | 54 | Dashboard development, interactive visualizations |
| Siddhi Jagdish Shinde | 68 | Website design, documentation, time-series analysis |

---

## 📁 Project Structure

```
PriceHarvest/
├── data/                        ← Raw CSV datasets (from Agmarknet)
│   ├── haryana_wheat.csv
│   ├── haryana_tomato.csv
│   ├── haryana_onion.csv
│   ├── mumbai_wheat.csv
│   ├── mumbai_tomato.csv
│   └── mumbai_onion.csv
│
├── src/                         ← Python source modules
│   ├── preprocessing.py         ← Module 1: Data loading & cleaning
│   ├── features.py              ← Module 2: Feature engineering
│   ├── eda.py                   ← Module 3: Individual crop EDA charts
│   ├── comparison.py            ← Module 4: Haryana vs Mumbai comparison
│   ├── timeseries.py            ← Module 5: Time-series analysis
│   ├── insights.py              ← Module 6: Intelligence report engine
│   └── advanced_viz.py          ← Module 7: Advanced visualizations
│
├── eda/
│   └── eda_analysis.ipynb       ← Jupyter notebook with all EDA steps
│
├── dashboard/
│   └── app.py                   ← Streamlit interactive dashboard
│
├── website/
│   ├── index.html               ← Professional project website
│   ├── style.css                ← Website styling
│   ├── script.js                ← Website animations & interactivity
│   └── images/                  ← EDA chart images for website
│
├── outputs/
│   ├── charts/                  ← All generated chart PNGs
│   └── insights/                ← Intelligence reports (JSON + TXT)
│
├── main.py                      ← Master pipeline runner
├── requirements.txt             ← Python dependencies
└── README.md                    ← This file
```

---

## 🚀 Quick Start (VS Code)

### Step 1 — Open Project
```bash
# Open VS Code, then open the PriceHarvest folder
code PriceHarvest/
```

### Step 2 — Install Dependencies
```bash
# Open VS Code terminal (Ctrl + `)
pip install -r requirements.txt
```

### Step 3 — Run the Full EDA Pipeline
```bash
# From PriceHarvest/ folder
python main.py
```
This generates all charts into `outputs/charts/` and saves the intelligence report.

### Step 4 — Open the EDA Notebook
```bash
# From PriceHarvest/ folder
jupyter notebook eda/eda_analysis.ipynb
```
Or open it directly in VS Code with the Jupyter extension.

### Step 5 — Run the Interactive Dashboard
```bash
# From PriceHarvest/ folder
streamlit run dashboard/app.py
```
Opens at: **http://localhost:8501**

### Step 6 — Preview the Website
- Right-click `website/index.html` in VS Code
- Click **"Open with Live Server"**
- (Install the Live Server extension from VS Code Extensions if needed)

---

## 📊 Dataset

**Source:** [Agmarknet Portal, Government of India](https://agmarknet.gov.in)

| Field | Description |
|---|---|
| `Arrival_Date` | Date of price record at market |
| `State` | Haryana or Maharashtra |
| `District` | District within the state |
| `Market` | APMC / Mandi name |
| `Commodity` | Crop: Wheat / Tomato / Onion |
| `Min_Price` | Minimum price (₹/Quintal) |
| `Max_Price` | Maximum price (₹/Quintal) |
| `Modal_Price` | Most common transaction price (₹/Quintal) |

**Coverage:** January 2023 – December 2025 · 7,497 records · 3 crops · 2 states

---

## 💡 Key Findings (Phase 1)

| Finding | Detail |
|---|---|
| **Most Volatile Crop** | Tomato (CV = 71.8% in Mumbai) |
| **Most Stable Crop** | Wheat (CV = 5.4% in Mumbai) |
| **Biggest Regional Gap** | Wheat 84% costlier in Mumbai vs Haryana |
| **Best Month for Onion** | November (post-Kharif peak) |
| **Tomato Peaks** | July–August (monsoon disruptions) |
| **Highest Price Ever** | ₹120/kg Tomato at Gharaunda — Jul 2023 |
| **Price Correlation** | Min ↔ Modal price: r = 0.94 |

---

## 🛠️ Tools & Technologies

- **Python 3.10+** — Core programming
- **Pandas & NumPy** — Data manipulation
- **Matplotlib & Seaborn** — Static visualizations
- **Streamlit** — Interactive dashboard
- **Plotly** — Interactive charts (Phase 2)
- **Jupyter Notebook** — EDA documentation
- **VS Code** — Development environment

---

## 🗺️ Phase Roadmap

### ✅ Phase 1 (Current)
- [x] Data preprocessing & cleaning
- [x] Feature engineering (rolling stats, volatility index)
- [x] Individual crop EDA (6 chart types per dataset)
- [x] State comparison analysis
- [x] Time-series decomposition & forecasting
- [x] Price intelligence insights engine
- [x] Streamlit interactive dashboard
- [x] Professional project website

### 🔜 Phase 2 (Upcoming)
- [ ] Linear Regression for price prediction
- [ ] Random Forest / Decision Tree classification
- [ ] ARIMA / Prophet time-series forecasting
- [ ] Scikit-learn model pipeline
- [ ] Model evaluation metrics

---

## 📄 References

- Agmarknet Portal, Government of India — https://agmarknet.gov.in
- Ministry of Agriculture & Farmers Welfare, Government of India
- Streamlit Documentation — https://docs.streamlit.io
- Scikit-learn Documentation — https://scikit-learn.org

---

*Department of Data Science and Engineering | Usha Mittal Institute of Technology | SNDT Women's University | Academic Year 2026–27*
