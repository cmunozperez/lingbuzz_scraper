# lingbuzz_scraper
This is a script designed to scrape data from [lingbuzz.net](https://ling.auf.net/), a linguistic preprint archive, and then save the extracted information into a CSV file. The data can also be retrieved as a Pandas DataFrame.

## Features

- **CSV File Generation:** The primary way to use the script is by running `main.py`. Executing this script generates a CSV file containing the extracted information from Lingbuzz manuscripts.

- **Pandas DataFrame Retrieval:** Alternatively, you can use the `lingbuzz_scrap()` function by importing `main.py`. This function returns the scraped data as a Pandas DataFrame, providing a more programmatic way to work with the extracted information.

- **Manuscript ID Range:** Manuscripts on Lingbuzz are assigned unique ID numbers (e.g., `lingbuzz/001865`). The scraper operates by specifying a range between two of these IDs. For instance, if you provide the IDs `001865` and `002865`, the scraper will gather data for all manuscripts falling within this ID range.

- **Automatic Proxy Handling:** The scraper automatically retrieves free proxies, checks them and uses them to connect to `lingbuzz.net`. Free proxies are slow; their usage is meant to help distribute the load and prevent overloading the server.

- **Processing Time:** Depending on the availability and quality of the free proxies at any given time, the scraping process may vary in speed. Keep this in mind when using the script, as the overall processing time could be longer due to the proxy limitations.

## Scraped Data Format

The scraper returns the data in the form of a Pandas DataFrame with the following columns:

- *Id*: the ID number corresponding to the manuscript
- *Title*: the title of the manuscript
- *Authors*: authors of the paper, separated by commas
- *Keywords*: keywords provided for the manuscript
- *Published_in*: place of publication
- *Date*: date of upload
- *Downloads*: download count for the manuscript
- *Abstract*: the abstract

This DataFrame will have as many rows as the number of papers that were scraped.

A sample CSV file containing all manuscript information in lingbuzz as of August 23 2023 (IDs ranging from `002` to `007537`) is available for download [here](https://github.com/cmunozperez/lingbuzz_scraper/blob/master/lingbuzz%20Aug_23_2023/lingbuzz_002_007537.csv).

## Usage

1. Clone this repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run `main.py` to generate a CSV file with scraped data or import `main.py` to use the `lingbuzz_scrap()` function for DataFrame retrieval.
4. Introduce the manuscript ID range as needed.
5. Remember to respect the scraping etiquette and use responsibly.

Feel free to explore the code and adapt it to your specific needs!

## License

This project is licensed under the [MIT License](license.MD).
