from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os


edge_options = webdriver.EdgeOptions()
edge_options.add_argument("--headless") 
edge_options.add_argument("--no-sandbox")
edge_options.add_argument("--disable-dev-shm-usage")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--log-level=3")
edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])

EDGE_DRIVER_PATH = r"EdgeDriver\msedgedriver.exe"
driver = webdriver.Edge(service=EdgeService(EDGE_DRIVER_PATH), options=edge_options)
driver.maximize_window()
driver.implicitly_wait(100)

driver.get("https://data.worldbank.org/indicator/SP.POP.TOTL")
time.sleep(10)  # Wait for page to load

# Create output directory if it doesn't exist
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define CSV file path
csv_file_path = os.path.join(output_dir, "data.csv")

def format_population(population_str):
    """
    Convert population from thousands to millions/billions with proper formatting
    """
    try:
        # Remove commas and spaces, convert to float
        # Population is in thousands
        population_clean = population_str.replace(',', '').replace(' ', '').strip()
        
        if not population_clean:
            return "N/A"
            
        population_num = float(population_clean)
        
        # Convert from thousands to actual number
        actual_population = population_num * 1000
        
        # Format based on size
        if actual_population >= 1_000_000_000:  # 1 Billion+
            value = actual_population / 1_000_000_000
            return f"{value:.2f} Billion"
        elif actual_population >= 1_000_000:  # 1 Million+
            value = actual_population / 1_000_000
            return f"{value:.2f} Million"
        elif actual_population >= 1_000:  # 1 Thousand+
            value = actual_population / 1_000
            return f"{value:.2f} Thousand"
        else:
            return f"{actual_population:.0f}"
            
    except (ValueError, TypeError) as e:
        return population_str  # Return original if conversion fails

def format_population_simple(population_str):
    """
    Alternative: Format as millions/billions with concise notation
    """
    try:
        population_clean = population_str.replace(',', '').replace(' ', '').strip()
        
        if not population_clean:
            return "N/A"
            
        population_num = float(population_clean)
        actual_population = population_num * 1000  # Convert from thousands
        
        if actual_population >= 1_000_000_000:
            return f"{actual_population / 1_000_000_000:.1f}B"
        elif actual_population >= 1_000_000:
            return f"{actual_population / 1_000_000:.1f}M"
        elif actual_population >= 1_000:
            return f"{actual_population / 1_000:.1f}K"
        else:
            return f"{actual_population:.0f}"
            
    except (ValueError, TypeError):
        return population_str

# Open CSV file for writing
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header with new column
    csv_writer.writerow(['Country', 'Census Year', 'Population (in thousands)', 'Formatted Population'])
    
    # Initialize row counter
    row_counter = 1
    found_zimbabwe = False
    max_attempts = 300  # Safety limit to prevent infinite loop
    
    while row_counter <= max_attempts and not found_zimbabwe:
        try:
            # Construct XPaths for the current row
            base_xpath = "/html/body/div[1]/div/div/div/div[3]/div/div/article/section/div/div/div/section/div/div[2]/div[{}]"
            
            # Country XPath (column 1)
            country_xpath = base_xpath.format(row_counter) + "/div[1]"
            # Census Year XPath (column 2)
            year_xpath = base_xpath.format(row_counter) + "/div[2]"
            # Population XPath (column 3)
            population_xpath = base_xpath.format(row_counter) + "/div[3]"
            
            # Extract data for current row
            country_element = driver.find_element(By.XPATH, country_xpath)
            country = country_element.text.strip()
            
            year_element = driver.find_element(By.XPATH, year_xpath)
            year = year_element.text.strip()
            
            population_element = driver.find_element(By.XPATH, population_xpath)
            population = population_element.text.strip()
            
            # Check if we have valid data (not empty)
            if not country and not year and not population:
                print(f"No more data found at row {row_counter}. Stopping...")
                break
            
            # Format the population
            formatted_population = format_population(population)
            
            # Print and write to CSV
            print(f"Row {row_counter:3d}: {country:<30} | Year: {year:<10} | Population: {population:>15} | Formatted: {formatted_population}")
            csv_writer.writerow([country, year, population, formatted_population])
            
            # Check if we've reached Zimbabwe
            if country.lower() == "zimbabwe":
                found_zimbabwe = True
                print(f"Reached Zimbabwe at row {row_counter}! Collection complete.")
                break
            
            row_counter += 1
            
        except Exception as e:
            print(f"Error at row {row_counter}: {e}")
            print("Reached end of data or element not found. Stopping...")
            break

# Final summary
total_rows_collected = row_counter - 1

print(f"\n{'='*70}")
print("DATA COLLECTION SUMMARY")
print(f"{'='*70}")
print(f"Target country found: {'Yes' if found_zimbabwe else 'No'}")
print(f"Total rows collected: {total_rows_collected}")
print(f"CSV file saved at: {csv_file_path}")

if found_zimbabwe:
    print(f"🎯 Stopped at: Zimbabwe (Row {row_counter})")
else:
    print(f"⚠️ Zimbabwe was not found. Collected {total_rows_collected} rows before stopping.")

# Show a few examples of the formatted data
print(f"Sample of formatted data:")
print("-" * 70)
print(f"{'Country':<30} {'Population':>15} {'Formatted':>20}")
print("-" * 70)

# Read back the CSV to show examples
try:
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        if len(rows) > 1:
            for i in range(1, min(6, len(rows))):
                row = rows[i]
                print(f"{row[0]:<30} {row[2]:>15} {row[3]:>20}")
        if len(rows) > 6:
            print(f"... and {len(rows) - 6} more rows")
except Exception as e:
    print(f"Could not read CSV for preview: {e}")

driver.close()
print("Browser closed.")