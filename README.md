# 🌾 PriceHarvest — Agricultural Crop Price Analysis & Prediction

**B.Tech Project  | Data Science | Usha Mittal Institute of Technology, S.N.D.T. Women's University**

PriceHarvest is an integrated agricultural crop price analysis and prediction platform. It combines data preprocessing, Exploratory Data Analysis (EDA), time-series analysis, interactive visualization, a chatbot, multilingual accessibility, and machine learning-based crop price prediction.

The project uses agricultural market data from the **Agmarknet Portal, Government of India**.

---

## 🎯 Project Objective

Agricultural crop prices fluctuate due to seasonality, supply and demand, market conditions, transportation, and regional differences. PriceHarvest transforms raw agricultural market records into meaningful, accessible insights and predictions by providing:

* 📊 Exploratory Data Analysis
* 📈 Crop price trend analysis
* 📅 Seasonal and time-series analysis
* 🏙️ City-wise comparison
* 📉 Price behaviour and volatility analysis
* 📊 Interactive dashboard (Streamlit)
* 💼 Interactive business intelligence reports
* 🤖 Chatbot assistance
* 🌐 Multilingual accessibility (English, Hindi, Marathi)
* 🧠 Machine learning-based crop price prediction (XGBoost + Prophet)

---

## 📍 Dataset Scope

| Attribute                  | Scope                                        |
| --------------------------- | --------------------------------------------- |
| **Data Source**             | Agmarknet, Government of India                |
| **Study Period**            | January 2021 – June 2026                      |
| **Duration**                | Approximately 5.5 years                       |
| **Cities**                  | Mumbai, Nagpur, Nashik                        |
| **Crops**                   | Onion, Potato, Cabbage                        |
| **City–Crop Combinations**  | 9 (3 crops × 3 cities)                        |
| **Analysis Level**          | City–Crop                                     |
| **Primary Price Variable**  | Modal Price                                   |
| **Data Type**               | Agricultural market price records             |

> **Note:** Exact record counts are not hard-coded here, as the dataset is periodically updated.

---

## 🌱 Crops & Cities

**Crops:** 🧅 Onion · 🥔 Potato · 🥬 Cabbage
**Cities:** 📍 Mumbai · 📍 Nagpur · 📍 Nashik

This gives **9 City–Crop combinations** for the machine learning prediction component.

---

## 🔬 Analysis Performed

### 1. Data Preprocessing
* Date conversion and validation
* Price validation (invalid observations removed using min/max/modal logic)
* Selection of relevant columns
* Market/grade standardization
* Duplicate handling
* Chronological sorting
* City and crop labelling
* Daily City–Crop time-series construction (missing dates handled)

### 2. Exploratory Data Analysis (EDA)
* Statistical summaries
* Daily price trends
* Monthly price distributions
* Seasonal patterns
* Year-wise comparison
* Moving-average analysis (30-day, 90-day)
* City-wise and crop-wise comparison
* Identification of unusual/anomalous observations
* Price volatility analysis

### 3. Time-Series Analysis
* Daily, monthly, and year-wise price movement
* Seasonal behaviour
* Moving averages
* City–Crop trend comparison

---

## 🧠 Machine Learning & Prediction

The prediction pipeline covers all **9 City–Crop combinations** (Onion, Potato, Cabbage × Mumbai, Nagpur, Nashik).

**Feature Engineering:**
* Calendar features — year, month, day, day of week, day of year, week, quarter, month start/end, weekend indicator
* Lag features — 1, 2, 3, 7, 14, 21, 30 days
* Rolling statistics — mean, std, min, max over 7/14/30-day windows (current day excluded to prevent leakage)
* Price-change features — % change over 1/7/30 days, plus expanding mean (using only past observations)

**Train/Test Split:** Chronological — training on Jan 2021–Dec 2025, testing on Jan–Jun 2026.

**Models:**
* **XGBoost regression** — separate model trained per City–Crop combination using engineered historical/temporal features
* **Prophet** — complementary time-series forecasting for trend, seasonality, and future price estimates

**Evaluation Metrics:** MAE (Mean Absolute Error) and MAPE (Mean Absolute Percentage Error)

### XGBoost Prediction Performance

| Crop    | City    | MAE       | MAPE     |
| ------- | ------- | --------: | -------: |
| Onion   | Mumbai  | 157.0     | 7.7%     |
| Onion   | Nagpur  | 359.6     | 13.4%    |
| Onion   | Nashik  | 1,487,105.5 | 70,781.1% |
| Potato  | Mumbai  | 192.5     | 21.1%    |
| Potato  | Nagpur  | 232.5     | 12.4%    |
| Potato  | Nashik  | 246.7     | 29.5%    |
| Cabbage | Mumbai  | 121.5     | 16.90%   |
| Cabbage | Nagpur  | 124.5     | 12.53%   |
| Cabbage | Nashik  | 163.9     | 23.15%   |

> ⚠️ **Nashik–Onion** shows a substantially higher error, traced to an anomalous observation in the underlying data that distorted lag/rolling features. Improved outlier detection and data validation for this case is a priority for the next phase.

**Feature Importance:** Lag features and rolling statistics were among the most influential features across several City–Crop models, indicating that recent price behaviour strongly drives predictions.

---

## 📊 Interactive Dashboard

The Streamlit dashboard lets users explore crop price trends, compare cities, and view seasonal behaviour and analytical insights interactively.

## 💼 Power BI Dashboard

Power BI provides business intelligence reporting with commodity-wise, city/district-level, monthly, and year-wise analysis, plus interactive filters and visual comparisons.

## 🤖 AI Chatbot

An AI-powered chatbot (Google Gemini API) is integrated into the website to assist users with dashboard navigation, agricultural analysis, and project information.

## 🌐 Multilingual Support

The interface supports 🇬🇧 English, 🇮🇳 Hindi, and 🇮🇳 Marathi (via Google Translate).

---

## 🏗️ Project Workflow

```text
Agmarknet Agricultural Data
            ↓
     Data Collection
            ↓
    Data Preprocessing
            ↓
   Data Validation & Cleaning
            ↓
   Daily Time-Series Creation
            ↓
 Exploratory Data Analysis
            ↓
 Time-Series & Seasonal Analysis
            ↓
 City–Crop Comparison
            ↓
 Feature Engineering
            ↓
 Chronological Train/Test Split
            ↓
 XGBoost Regression + Prophet Forecasting
            ↓
 Model Evaluation (MAE, MAPE) & Feature Importance
            ↓
 ┌───────────────────────────────┐
 │                               │
 ▼                               ▼
Streamlit Dashboard          Power BI
 │                               │
 └──────────────┬────────────────┘
                ↓
        PriceHarvest Website
                ↓
       AI Chatbot + Multilingual
```

---

## 📁 Project Structure

```text
PriceHarvest/
│
├── data/
│   ├── onion/
│   ├── potato/
│   └── cabbage/
│
├── src/
│   ├── preprocessing.py
│   ├── features.py
│   ├── eda.py
│   ├── comparison.py
│   ├── timeseries.py
│   ├── insights.py
│   └── advanced_viz.py
│
├── eda/
│   └── eda_analysis.ipynb
│
├── ml/
│   └── prediction notebooks / models (XGBoost, Prophet)
│
├── dashboard/
│   └── app.py
│
├── website/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── images/
│
├── outputs/
│   ├── charts/
│   ├── insights/
│   └── predictions/
│
├── main.py
├── requirements.txt
└── README.md
```

> File names may vary depending on the latest implementation of the project repository.

---

## 🚀 Quick Start

### 1. Clone / Open the Project
```bash
git clone <repository-url>
cd PriceHarvest
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Analysis Pipeline
```bash
python main.py
```

### 4. Open the EDA Notebook
```bash
jupyter notebook eda/eda_analysis.ipynb
```

### 5. Run the Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```
Available at `http://localhost:8501`

### 6. Open the Website
Open `website/index.html` (use the **Live Server** extension in VS Code for local development).

---

## 🛠️ Technologies Used

**Programming & Data Analysis:** Python, Pandas, NumPy
**Visualization:** Matplotlib, Seaborn, Plotly
**Machine Learning / Forecasting:** XGBoost, Prophet, Scikit-learn
**Dashboard & BI:** Streamlit, Microsoft Power BI
**Web Development:** HTML, CSS, JavaScript
**AI & Accessibility:** Google Gemini API, Google Translate
**Dev Tools:** Jupyter Notebook, VS Code, Git/GitHub

---

## 📌 Project Status

| Component                                       | Status            |
| ------------------------------------------------ | ----------------- |
| Agricultural data collection                      | ✅ Completed       |
| Data preprocessing                                 | ✅ Completed       |
| Exploratory Data Analysis                          | ✅ Completed       |
| Time-series analysis                               | ✅ Completed       |
| City-wise and crop-wise analysis                   | ✅ Completed       |
| Streamlit dashboard                                | ✅ Completed       |
| Power BI reporting                                 | ✅ Completed       |
| AI chatbot                                         | ✅ Completed       |
| Multilingual interface (English, Hindi, Marathi)   | ✅ Completed       |
| ML prediction (XGBoost, 9 City–Crop combinations)  | ✅ Completed       |
| Prophet-based forecasting                          | ✅ Completed       |
| Model evaluation (MAE, MAPE) & feature importance  | ✅ Completed       |
| Nashik–Onion outlier handling / data validation    | 🟡 In Progress    |
| Prediction results integration into website        | 🔜 Upcoming       |

---

## 🗺️ Development Roadmap

### ✅ Completed
* Agricultural data collection, preprocessing, and cleaning
* Exploratory Data Analysis and seasonal trend analysis
* City-wise and crop-wise analysis, interactive visualizations
* Streamlit dashboard, Power BI integration
* AI chatbot integration
* English, Hindi, Marathi interfaces
* Feature engineering (calendar, lag, rolling, price-change)
* XGBoost regression across 9 City–Crop combinations
* Prophet-based forecasting
* Model evaluation (MAE, MAPE) and feature importance analysis

### 🟡 Currently in Development
* Improved outlier detection and data validation (esp. Nashik–Onion)
* Integrating finalized prediction/forecast results into the website

### 🔜 Future Scope
* Incorporate weather and rainfall information
* Include agricultural production and market-arrival variables
* Compare additional machine learning and forecasting models
* Improve handling of extreme price observations
* Automated data updates
* Real-time / near-real-time crop price prediction
* Expand to additional crops, cities, and markets
* Expanded chatbot and multilingual capabilities

---

## 📚 Data Source

**Agmarknet — Agricultural Marketing Information Network**, Government of India. Datasets contain agricultural market price information collected from Agricultural Produce Market Committees (APMCs).

---

## 📖 References

* Agmarknet — Government of India
* Ministry of Agriculture & Farmers Welfare, Government of India
* Streamlit Documentation
* Scikit-learn Documentation
* XGBoost Documentation
* Prophet (Facebook/Meta) Documentation
* Latex Documentation

---

## 🎓 Academic Information

**Project:** PriceHarvest — Agricultural Crop Price Analysis & Prediction
**Degree:** Bachelor of Technology in Data Science
**Department:** Data Science and Engineering
**Institute:** Usha Mittal Institute of Technology
**University:** S.N.D.T. Women's University
**Academic Year:** 2025–26

---

## 🌾 About PriceHarvest

PriceHarvest brings together agricultural data, exploratory analysis, time-series analysis, business intelligence, AI assistance, and machine learning into a single platform — making historical agricultural market data easier to explore, compare, understand, and use for crop price prediction.
