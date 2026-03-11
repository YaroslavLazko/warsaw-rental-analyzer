# Warsaw Rental Market Analyzer & Deal Finder

An end-to-end data pipeline and interactive BI dashboard designed to solve a real-world problem: finding undervalued apartments in the highly dynamic Warsaw rental market.

## Project Overview
Finding an apartment in Warsaw often involves informational asymmetry, where renters overpay because they don't know the true market value per square meter in specific districts. This project automates the collection of real estate listings, processes the data, and highlights "Great Deals" using custom DAX median-based logic.

**Live/Automated:** The ETL pipeline is fully automated and runs daily at 12:00 PM via Windows Task Scheduler to ensure the database is always up-to-date.

## Dashboard Highlights

<img width="1112" height="623" alt="image" src="https://github.com/user-attachments/assets/7a9f184c-7665-4eb3-8031-c64ef799eb06" />


### Key Features:
1. **Market Overview:** A macro-level view of average prices and total listings across Warsaw districts using spatial mapping.
2. **The "Deal Finder" Engine:** A scatter plot analysis that compares individual apartment prices against the district's median price per square meter. 
3. **Actionable Table:** Conditionally formatted listings with direct web links to the original ad, instantly highlighting whether a flat is underpriced or overpriced.

<img width="1112" height="624" alt="image" src="https://github.com/user-attachments/assets/2cbdd1fb-181e-4657-ad34-8c766f8dce1e" />


## Tech Stack
* **Web Scraping & ETL:** Python (Pandas, BeautifulSoup/Requests)
* **Database:** PostgreSQL
* **Automation:** Windows Task Scheduler (.bat scripts)
* **Data Visualization:** Power BI (DAX, Power Query)

## Pipeline Architecture
1. **Extract:** Python scraper collects fresh rental listings from property platforms.
2. **Transform:** Pandas handles data cleaning, currency conversion (EUR to PLN), and standardizes categorical data (e.g., room counts).
3. **Load:** Cleaned data is appended to a local PostgreSQL database.
4. **Automate:** A `.bat` script triggered by Task Scheduler runs the entire ETL process daily.

## How to Run Locally
1. Clone the repository.
2. Install the required Python libraries directly: 
   ```bash
   pip install pandas requests beautifulsoup4 psycopg2-binary
4. Run `run_etl.bat` to execute the pipeline.
5. Open `dashboard/warsaw_rentals.pbix` in Power BI Desktop and hit "Refresh".
