# Customer Analytics Dashboard

An interactive data analytics dashboard built with Streamlit, 
connected live to a PostgreSQL DVD Rental database. 
This dashboard explores customer behavior, revenue patterns, 
loyalty segmentation, and individual customer profiles.


## Team — Group FMS (DS 2)

| Name | Role |
|------|------|
| Marsha Aulia Rizky | Loyalty & Segmentation (Tab 3) |
| Putri Jingga | Behavior Analysis (Tab 2) |
| Syakira Latifah | Overview & Revenue (Tab 1) |

## Dashboard Features

### Tab 1 — Overview
- 5 KPI Cards: Total Customers, Total Revenue, Total Rentals, Avg Transaction, Avg Spend per Customer
- Monthly Revenue & Transactions (dual-axis chart)
- Top N Customers by Spending (interactive slider)
- Customer Distribution by Country
- Cumulative Revenue Growth

### Tab 2 — Behavior
- Favorite Film Genres across all customers
- Scatter Plot: Rental Frequency vs Revenue (with OLS trendline, r = 0.88)
- Histogram: Rental Frequency Distribution
- Rental Duration Distribution

### Tab 3 — Loyalty & Segments
- RFM Segmentation: Champions, Loyal, At Risk, Lost
- Average Spending per RFM Segment
- Spending Tier Analysis (Quartile-based: Low / Mid / High / Top Spender)
- Revenue Contribution by Spending Tier
- At-Risk Customers Table (inactive 90+ days)
- Key Insights: Revenue Concentration, Frequency-Revenue Correlation, Return Behavior

### Tab 4 — Customer Detail
- Search any customer by name
- Individual KPI Cards: Total Rentals, Total Spent, Avg Transaction, First & Last Rental
- Rental Activity Over Time (line chart)
- Favorite Genres per customer
- Full Rental History Table


## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core programming language |
| Streamlit | Web dashboard framework |
| PostgreSQL | Database (dvdrental) |
| SQLAlchemy | Database connection |
| Pandas | Data manipulation |
| Plotly Express & Graph Objects | Interactive visualizations |


## Database

This project uses the **dvdrental** PostgreSQL sample database.  
Tables used: `customer`, `rental`, `payment`, `inventory`, `film`, `film_category`, `category`, `address`, `city`, `country`


## How to Run?

### 1. Clone this repository
```bash
git clone https://github.com/USERNAME/REPO-NAME.git
cd REPO-NAME
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL
- Make sure PostgreSQL is running
- Load the dvdrental database
- Update the database connection in `dashboard.py`:
```python
DB_URL = "postgresql+psycopg2://YOUR_USER:YOUR_PASSWORD@localhost:5432/dvdrental"
```

### 5. Run the app
```bash
streamlit run dashboard.py
```
