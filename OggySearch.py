import requests
from bs4 import BeautifulSoup
import ast  # To safely evaluate a string as a Python literal (like a list)
import tkinter as tk
import os
import sys
from io import StringIO
import webbrowser
from tkinter import filedialog
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pyperclip
from dotenv import load_dotenv  # Add this import

# Load environment variables
load_dotenv()

# Capture terminal output for saving
log_output = StringIO()
original_stdout = sys.stdout

# Function to fetch webpage text
def fetch_webpage_text(url):
    """Fetch and return plain text from a webpage, supporting JavaScript-rendered content."""
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Initialize the driver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        # Load the page
        driver.get(url)
        
        # Wait for the content to load (specifically for GSoC page)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(2)  # Additional wait for dynamic content

        # Get the page content
        page_content = driver.page_source
        
        # Clean up
        driver.quit()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # For GSoC pages, focus on relevant content
        if 'summerofcode.withgoogle.com' in url:
            # Get all text content
            text_content = soup.get_text()
            # Clean up the text (remove extra whitespace)
            text_content = ' '.join(text_content.split())
            return text_content
            
        return soup.get_text()
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return ""

# Function to extract names using the same logic as the original code
def extract_names_from_text(text):
    """Send extracted text to Gemini API and return detected names."""
    api_key = os.getenv('GEMINI_API_KEY')  # Get API key from environment variable
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return []
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}

    # Updated prompt for better name extraction
    prompt_text = (
        "Extract all the person names from the given text. "
        "Focus on mentor names, student names, and any other human names mentioned. "
        "Return only a list of names in a clean comma-separated format. "
        "Exclude organization names, project names, and other non-person entities. "
        "If the text is from a Google Summer of Code page, pay special attention to mentor and student names."
    )

    payload = {
        "contents": [{
            "parts": [{"text": f"{prompt_text}\n\n{text}"}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        names = []
        if "candidates" in data:
            for candidate in data["candidates"]:
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "text" in part:
                            # Clean up and deduplicate names
                            names_list = [
                                name.strip() 
                                for name in part["text"].split(",")
                                if name.strip() and len(name.strip().split()) >= 2  # Ensure full names
                            ]
                            names.extend(names_list)

        # Remove duplicates while preserving order
        return list(dict.fromkeys(names))
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return []

# Function to save terminal output to a text file with incremental filenames
def save_output_to_text_file():
    """Save extracted names to a uniquely named CSV file."""
    i = 1
    while os.path.exists(f"names{i}.csv"):
        i += 1

    filename = f"names{i}.csv"
    
    if extracted_names_cache:
        with open(filename, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name"])  # Header
            for name in extracted_names_cache:
                writer.writerow([name.strip()])
        print(f"Names saved to '{filename}'.")
    else:
        print("No names to save.")

def copy_to_clipboard():
    """Copy names to clipboard in CSV format"""
    if extracted_names_cache:
        names_csv = ",".join(extracted_names_cache)
        pyperclip.copy(names_csv)
        print("Names copied to clipboard in CSV format")
    else:
        print("No names to copy")

# Function to handle extraction via GUI button
extracted_names_cache = []

def extract_names():
    global extracted_names_cache
    sys.stdout = log_output  # Redirect print output to log
    try:
        url = url_entry.get().strip()
        if not url:
            print("Please enter a valid URL.")
            return

        webpage_text = fetch_webpage_text(url)

        if not webpage_text.strip():
            print("Failed to extract text from webpage.")
        else:
            extracted_names_cache = extract_names_from_text(webpage_text)

            # Clear and update the names display
            names_display.delete(1.0, tk.END)
            if extracted_names_cache:
                # Display names in CSV format
                names_csv = ",".join(extracted_names_cache)
                names_display.insert(tk.END, names_csv)
                print("\nExtracted Names (CSV format):")
                print(names_csv)
            else:
                names_display.insert(tk.END, "No names extracted.")
                print("No names extracted.")
    finally:
        sys.stdout = original_stdout
        print(log_output.getvalue())

# Function to search names with follow-up query
def search_names():
    followup = followup_entry.get().strip()
    names_input = names_input_entry.get().strip()
    if not followup or not names_input:
        print("Please enter both names and follow-up query.")
        return

    names = names_input.split(',')
    for name in names:
        name = name.strip()
        query = f"{name} {followup}"
        webbrowser.open(f"https://www.google.com/search?q={query}")

def upload_csv():
    """Upload and read names from a CSV file."""
    global extracted_names_cache
    
    filename = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if filename:
        try:
            extracted_names_cache = []
            with open(filename, mode='r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader, None)  # Skip header row
                for row in csv_reader:
                    if row:  # Check if row is not empty
                        extracted_names_cache.append(row[0].strip())
            
            # Clear and update the names display
            names_display.delete(1.0, tk.END)
            names_csv = ",".join(extracted_names_cache)
            names_display.insert(tk.END, names_csv)
                
            # Display the loaded names
            print("\nLoaded Names (CSV format):")
            print(names_csv)
                
            # Update the names input entry with loaded names
            names_input_entry.delete(0, tk.END)
            names_input_entry.insert(0, names_csv)
            
        except Exception as e:
            print(f"Error reading CSV file: {e}")

# Create the main window
root = tk.Tk()
root.title("OggySearch")
root.geometry("600x800")  # Made taller to accommodate the display area

# Create input field for URL
tk.Label(root, text="Enter URL:", font=("Roboto", 14)).pack(pady=10)
url_entry = tk.Entry(root, width=60, font=("Roboto", 12))
url_entry.pack(pady=10)

# Input fields for follow-up and names
tk.Label(root, text="Enter Follow-up Query:", font=("Roboto", 14)).pack(pady=10)
followup_entry = tk.Entry(root, width=60, font=("Roboto", 12))
followup_entry.pack(pady=10)

# Input for names
tk.Label(root, text="Enter Names (comma-separated):", font=("Roboto", 14)).pack(pady=10)
names_input_entry = tk.Entry(root, width=60, font=("Roboto", 12))
names_input_entry.pack(pady=10)

# Create text widget for displaying extracted names
tk.Label(root, text="Extracted Names:", font=("Roboto", 14)).pack(pady=10)
names_display = tk.Text(root, height=10, width=50, font=("Roboto", 12))
names_display.pack(pady=10)

# Create frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create button to extract names
extract_button = tk.Button(
    button_frame, 
    text="Extract Names", 
    command=extract_names, 
    font=("Roboto", 14), 
    bg="#3498db", 
    fg="white"
)
extract_button.pack(side=tk.LEFT, padx=5)

# Create button to copy to clipboard
copy_button = tk.Button(
    button_frame, 
    text="Copy to Clipboard", 
    command=copy_to_clipboard, 
    font=("Roboto", 14), 
    bg="#e74c3c", 
    fg="white"
)
copy_button.pack(side=tk.LEFT, padx=5)

# Create button to save terminal output to a text file
save_button = tk.Button(
    button_frame, 
    text="Save in CSV", 
    command=save_output_to_text_file, 
    font=("Roboto", 14), 
    bg="#2ecc71", 
    fg="white"
)
save_button.pack(side=tk.LEFT, padx=5)

# Create button to upload CSV
upload_button = tk.Button(
    button_frame, 
    text="Upload CSV", 
    command=upload_csv, 
    font=("Roboto", 14), 
    bg="#9b59b6", 
    fg="white"
)
upload_button.pack(side=tk.LEFT, padx=5)

# Search button
search_button = tk.Button(
    button_frame, 
    text="Search Names", 
    command=search_names, 
    font=("Roboto", 14), 
    bg="#f39c12", 
    fg="white"
)
search_button.pack(side=tk.LEFT, padx=5)

# Run the GUI loop
root.mainloop()
