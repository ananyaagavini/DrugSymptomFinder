#  DrugSymptomFinder 

**DrugSymptomFinder** is a web application that bridges lay-person symptom inputs (e.g., *"fever"*, *"joint pain"*, *"seizures"*, *"high blood sugar"*) to official clinical drug approval records using synonym expansion and fuzzy matching.

---

##  Important Data & Project Disclaimers

> [!IMPORTANT]
> 1. **Data Source**: This project uses real approved drug data from the **Central Drugs Standard Control Organization (CDSCO)**, Ministry of Health and Family Welfare, Government of India (`cdsco_drugs_for_app.csv`, 3,144 rows).
> 2. **No Manufacturer Column**: There is **NO manufacturer field** present in the official source dataset; as per project constraints, no manufacturer field is displayed, manufactured, or invented.
> 3. **Approval Date**: The `date_of_approval` column contains inconsistent string formats in government records and is treated strictly as display-only text.
> 4. **Educational Demo Only**: This tool is developed **strictly for educational and demonstration purposes**. It does **NOT** constitute medical advice. Always consult a licensed pharmacist or doctor for medical diagnosis or treatment.

---

##  Tech Stack & Architecture

- **Backend**: Python 3.9+, [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)
- **Data Engine**: SQLite 3, `pandas` (for ingestion), `rapidfuzz` (for fuzzy string matching & partial token ratio)
- **Frontend**: Clean Vanilla HTML5, CSS3 Glassmorphism UI, FontAwesome icons, native JavaScript (ES6 fetch, debounced autocomplete, confidence meter visualization)

---

##  Project Structure

```
DrugSymptomFinder/
├── cdsco_drugs_for_app.csv   # Real CDSCO dataset (3,144 approved drug records)
├── db.py                     # SQLite database schema setup & automatic ingestion
├── symptoms.py               # Lay-to-clinical synonym dictionary & autocomplete terms
├── matcher.py                # Rapidfuzz partial ratio & score ranking engine
├── main.py                   # FastAPI application & REST endpoints
├── test_matcher.py           # Unit tests covering 4 matching scenarios
├── requirements.txt          # Required Python dependencies
├── README.md                 # Project documentation & setup instructions
└── static/
    ├── index.html            # Responsive dark mode glassmorphism UI
    ├── style.css             # CSS design tokens, cards, and animations
    └── app.js                # Search, autocomplete, loading & empty state logic
```

---

##  Quick Start & Setup Instructions

### 1. Prerequisite Setup
Ensure Python 3.9+ is installed on your system.

### 2. Install Dependencies
Open your terminal in the project directory and run:
```bash
pip install -r requirements.txt
```

### 3. Run Matching Engine Tests
Execute the unit test suite to verify fuzzy matching, synonym expansion, and no-match scenarios:
```bash
python test_matcher.py
```

### 4. Start the Application Server
Launch the FastAPI development server:
```bash
python main.py
```
Or with uvicorn directly:
```bash
python -m uvicorn main:app --reload --port 8000
```


### 5. Access the Web Application
Open your web browser and navigate to:
 **`http://127.0.0.1:8000`**

---

## 🔍How Synonym Expansion & Fuzzy Matching Work

1. **User Input**: User types a lay symptom (e.g. `"fever"`).
2. **Synonym Expansion**: `symptoms.py` expands `"fever"` to clinical terms `["pyrexia", "fever", "hyperthermia", "febrile", "temperature"]`.
3. **Fuzzy Scoring**: `matcher.py` uses `rapidfuzz.fuzz.partial_ratio` & `token_set_ratio` against the `indication` text of all 3,144 records in the SQLite database.
4. **Ranking & Display**: Results are scored from 0 to 100%, sorted in descending confidence order, and displayed in a responsive card layout with visual match bars and warning disclaimers.
