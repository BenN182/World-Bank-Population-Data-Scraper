# World Bank Population Statistics Scraper

A Python-based web scraping application that extracts population statistics from the World Bank's data portal. The scraper collects country-wise population data and converts the figures into a human-readable format (millions/billions) with proper rounding.

---
## ✨ Features

- **Automated Data Collection**: Scrapes population data from the World Bank website
- **Smart Formatting**: Converts raw population figures (in thousands) to:
  - Millions (e.g., 43.84 Million)
  - Billions (e.g., 1.41 Billion)
- **CSV Export**: Saves data to a structured CSV file with multiple columns
- **Automatic Stopping**: Stops collection when it reaches Zimbabwe
- **Headless Mode**: Runs in headless mode for server environments
- **Progress Tracking**: Displays real-time progress during scraping

### Required Software
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Microsoft Edge Browser** - [Download Edge](https://www.microsoft.com/edge)
- **Microsoft Edge WebDriver** - Compatible with your Edge version

### Python Packages
- **Selenium** - Web automation framework
- **CSV** - Built-in Python module for CSV operations
- **OS** - Built-in Python module for operating system interactions
- **Time** - Built-in Python module for time operations

## 📦 Installation

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd world-population-scraper

```

### 2. Download EdgeDriver

```bash
Check your Microsoft Edge version:

Open Edge browser

Click on the three dots (⋮) in the top right corner

Go to Help and feedback → About Microsoft Edge

Note your version number (e.g., 115.0.1901.203)

Download the matching EdgeDriver:

Visit the official Microsoft Edge Driver download page

Download the version that matches your Edge browser

For Windows: Download the edgedriver_win64.zip file

Extract and place EdgeDriver:

Extract the downloaded zip file

Create an EdgeDriver folder in your project root directory

Place msedgedriver.exe inside the EdgeDriver folder

```
### 3. Project Structure 

```bash
world-population-scraper/
├── main.py
├── requirements.txt
├── README.md
├── EdgeDriver/
│   └── msedgedriver.exe
└── output/
    └── data.csv (generated after running)

```
## 📷 Project Screenshots

### Website

![Data We Are Scrapping](docs\Website.png)

---

### CSV Output

![Collected Data](docs\data.png)


## License

This project is intended for demonstration and portfolio purposes.

It showcases the scrapping of data from a website using python-selenium. We also use csv to save the collected data in a data.csv file.


