# Python Developer Vacancies Scraper and Analysis

This project is designed for:
- Scraping Python Developer job vacancies from [DOU.ua](https://jobs.dou.ua).
- Analyzing the demand for various technologies mentioned in job descriptions using Python libraries.

The data is categorized into two levels:
- **Junior-Middle** 
- **Middle-Senior**

## Technologies Used
The following technologies were utilized in this project:
- **Scrapy** for data scraping.
- **Selenium** for handling dynamic web content.
- **Jupyter Notebook** for data analysis.
- **Numpy**, **Pandas**, and **Matplotlib** for data processing and visualization.

## How to Run the Project

### Step 1: Clone the repository
Clone this repository to your local machine:
```bash
git clone <repository-url>
cd <repository-folder>
```
### Step 2: Set up a virtual environment
Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows
```
### Step 3: Install dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```
### Step 4: Scrape new data
To scrape the latest job vacancies, run the following command:
```bash
scrapy crawl dou
```
### Step 5: Run data analysis
Open the Jupyter Notebook to analyze the data
