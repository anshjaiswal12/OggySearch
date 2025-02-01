# OggySearch 🔍

A powerful GUI tool for extracting and processing names from web pages, with special optimization for Google Summer of Code (GSoC) pages. OggySearch makes it easy to extract mentor and student names, manage them, and perform batch searches.

![OggySearch Interface](screenshot.png)

## 🌟 Features

- **Smart Name Extraction**
  - Extracts names from any webpage using Gemini AI
  - Specially optimized for GSoC pages
  - Supports JavaScript-rendered content

- **User-Friendly Interface**
  - Clean and intuitive GUI
  - Real-time name display
  - Easy-to-use controls

- **Data Management**
  - Export names to CSV files
  - Import names from CSV files
  - Copy names to clipboard
  - Batch processing support

- **Search Integration**
  - Perform batch Google searches
  - Customizable follow-up queries
  - Direct browser integration

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Google Chrome Browser
- Gemini API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/anshjaiswal12/OggySearch.git
   cd OggySearch
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment:
   - Create a `.env` file in the project root
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

### Usage

1. Launch the application:
   ```bash
   python OggySearch.py
   ```

2. Enter a webpage URL in the input field

3. Click "Extract Names" to process the page

4. Use additional features:
   - Save extracted names using "Save in CSV"
   - Copy names using "Copy to Clipboard"
   - Upload existing CSV files
   - Perform batch searches with custom queries

## 🛠️ Technical Details

### Key Components

- **Web Scraping**: Selenium WebDriver for JavaScript support
- **AI Processing**: Google's Gemini AI for name extraction
- **GUI**: Tkinter for the user interface
- **Data Handling**: CSV support for import/export

### Dependencies

- requests
- beautifulsoup4
- selenium
- webdriver_manager
- python-dotenv
- pyperclip

## 📝 Notes

- Ensure Chrome WebDriver is properly installed
- Keep your API key secure and never share it
- For GSoC pages, allow sufficient time for content loading

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a new branch
3. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for name extraction capabilities
- Selenium for web scraping functionality
- All contributors and users of OggySearch

## 📧 Contact

Ansh Jaiswal - [GitHub](https://github.com/anshjaiswal12)

Project Link: [https://github.com/anshjaiswal12/OggySearch](https://github.com/anshjaiswal12/OggySearch)
