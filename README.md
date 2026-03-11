# 🏙️ Warsaw Rental Market Analyzer & Deal Finder

An end-to-end data pipeline and interactive BI dashboard designed to solve a real-world problem: finding undervalued apartments in the highly dynamic Warsaw rental market.

## 📌 Project Overview
Finding an apartment in Warsaw often involves informational asymmetry, where renters overpay because they don't know the true market value per square meter in specific districts. 
This project automates the collection of real estate listings, processes the data, and highlights "Great Deals" using custom DAX median-based logic.

**🔴 Live/Automated:** The ETL pipeline is fully automated and runs daily at 12:00 PM via Task Scheduler to ensure the database is always up-to-date.

## ⚙️ Tech Stack
* **Web Scraping & ETL:** Python (Pandas, BeautifulSoup/Requests)
* **Database:** PostgreSQL
* **Automation:** Windows Task Scheduler (.bat scripts)
* **Data Visualization & Analytics:** Power BI (DAX, Power Query)

## 📊 Dashboard Highlights
*(Add a screenshot or GIF of your Power BI dashboard here. Put the image in the `assets/` folder)*
`![Market Overview](assets/dashboard_overview.png)`

### Key Features:
1. **Market Overview:** A macro-level view of average prices and total listings across Warsaw districts using spatial mapping.
2. **The "Deal Finder" Engine:** A scatter plot analysis that compares individual apartment prices against the **district's median price per square meter**. 
3. **Actionable Table:** Conditionally formatted listings with direct web links to the original ad, instantly highlighting whether a flat is underpriced (green arrow) or overpriced (red arrow).

## 🏗️ Pipeline Architecture
1. **Extract:** Python scraper bypasses basic protections and collects fresh rental listings from property platforms.
2. **Transform:** Pandas handles data cleaning, currency conversion (EUR to PLN), and standardizes categorical data (e.g., room counts, district names).
3. **Load:** Cleaned data is appended to a local PostgreSQL database.
4. **Automate:** A `.bat` script triggered by Task Scheduler runs the entire ETL process daily at 12:00 PM.

## 🚀 How to Run Locally
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your PostgreSQL credentials in `load_to_postgres.py`.
4. Run `run_etl.bat` to execute the pipeline.
5. Open `dashboard/warsaw_rentals.pbix` in Power BI Desktop and hit "Refresh".
