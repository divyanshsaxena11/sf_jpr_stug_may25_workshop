# 🏥 Hospital Intelligence System — Healthcare Project

## 📖 Overview
This project demonstrates a **Hospital Intelligence System** built on structured healthcare datasets (patients, admissions, treatments, notes) and integrated with **Snowflake Cortex AI Services** — including **Cortex Agents**, **Cortex Analyst**, and **Cortex Search**.

The system simulates real-world hospital workflows, generating healthcare insights, billing analytics, and patient management solutions.

---

## 🗂️ Project Structure

| Type | Files | Description |
|:-----|:------|:------------|
| 📄 Study Library Archive PDFs | `medical guide.pdf`, ... | Simulated medical case studies and details on global reports for drugs |
| 📊 CSV Data Files | `patients.csv`, `admissions.csv`, `treatment_summary.csv`, `notes.csv`, `ward_occupancy.csv`, `invoices.csv` | Structured hospital datasets |
| 🧐 Semantic Model YAML | `hospital_semantic_model.yaml` | Snowflake Cortex Analyst semantic definitions |
| 🧐 Cortex Agent Setup | `hospital_agent_setup.sql` | SQL setup scripts for Cortex Agent training |
| 🌐 Streamlit App | `hospital_intelligence_app.py` | Interactive dashboard to visualize hospital data |
| 📋 Documentation | `README.md` | This project guide |

---

## 🧬 Dataset Details

### 1. Patients Table
- Patient demographics and health conditions
- Fields: Patient ID, Name, Age, Condition, Status

### 2. Admissions Table
- Hospital admissions, wards, and reasons
- Fields: Admission ID, Patient ID, Ward, Reason, Admission Time, Discharge Date

### 3. Treatment Summary Table
- Drug prescriptions and outcomes
- Fields: Patient ID, Drug Name, Start Date, End Date, Outcome

### 4. Clinical Notes Table
- Doctor notes and observations
- Fields: Note ID, Patient ID, Note Text, Note Timestamp

### 5. Ward Occupancy Table
- Bed usage across hospital wards
- Fields: Ward Name, Beds Total, Beds Occupied

---

## 🧬 Snowflake Cortex Integration

### Cortex Agent
- Allows natural language queries over hospital datasets
- Example: _"List all ICU admissions in April 2025."_

### Cortex Analyst
- Semantic layer for defining dimensions, time dimensions, and measures over data
- Improves structured query generation and data understanding

### Cortex Search
- Enables semantic search across PDF invoices and clinical notes
- Example: _"Find invoices for patients discharged in April 2025."_

---

## 🚀 How to Run

1. Set up a Snowflake account with Cortex access
2. Upload CSV datasets into Snowflake tables
3. Create semantic models using `patient_report.yaml`
4. Deploy the Cortex Project using `build_agents_for_healthcare.ipynb`
5. Upload PDF medical study guides to Snowflake stages for Cortex Search
6. Run `streamlit.py` Streamlit dashboard

---

## 🌟 Highlights

- Simulates real hospital workflows: Admissions ➞ Treatment ➞ Insights
- Leverages **Cortex AI Services** for intelligent healthcare analytics
- Includes realistic medical invoices for real-world data simulation
- Supports interactive healthcare challenges and question-answering use cases

---

## 📚 Future Enhancements

- Real-time vitals and monitoring data integration
- Predictive modeling for patient readmissions
- Sentiment analysis on clinical notes
- Full patient lifecycle tracking across multiple admissions

---

# 🩺 Built for Healthcare Intelligence, Powered by Snowflake Cortex 🚀
