# Customer Analytics Dashboard

A Streamlit-based interactive analytics dashboard for exploring 
customer behavior in a DVD rental store, connected live to a 
PostgreSQL database.

## Team
Marsha Aulia Rizky · Fatwa · Putri Jingga · Syakira Latifah  
Advanced Database — President University

## Features
- **Overview** — KPIs for total customers, rentals, and revenue
- **Segmentation** — Group customers by rental frequency & spending
- **Behavior** — Rental duration patterns & frequency vs revenue correlation
- **Customer Profile** — Search any customer, see full rental history & favorite genres

## Tech Stack
Python · Streamlit · PostgreSQL · SQLAlchemy · Pandas · Plotly

## How to Run
1. Clone the repo
2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. Setup PostgreSQL with DVD Rental database
4. Run the app
```bash
streamlit run bismillah.py
```
