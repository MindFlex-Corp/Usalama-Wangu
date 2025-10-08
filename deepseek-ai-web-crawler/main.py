import asyncio
from datetime import datetime
import os

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from utils.data_utils import (
    save_incidents_to_csv,
)
from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
)

load_dotenv()


async def crawl_incidents():
    """
    Main function to crawl incident data from the website.
    """
    # Initialize configurations
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "incident_crawl_session"

    # Initialize state variables
    page_number = 1
    all_incidents = []
    seen_names = set()

    # Start the web crawler context
    # https://docs.crawl4ai.com/api/async-webcrawler/#asyncwebcrawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        while True:
            # Fetch and process data from the current page
            incidents, no_results_found = await fetch_and_process_page(
                crawler,
                page_number,
                BASE_URL,
                CSS_SELECTOR,
                llm_strategy,
                session_id,
                REQUIRED_KEYS,
                seen_names,
            )

            if no_results_found:
                print("No more incidents found. Ending crawl.")
                break  # Stop crawling when "No Results Found" message appears

            if not incidents:
                print(f"No incidents extracted from page {page_number}.")
                break  # Stop if no incidents are extracted

            # Add the incidents from this page to the total list
            all_incidents.extend(incidents)
            page_number += 1  # Move to the next page

            # Pause between requests to be polite and avoid rate limits
            await asyncio.sleep(2)  # Adjust sleep time as needed

    # Save the collected incidents to a CSV file
    if all_incidents:
        # Create a timestamp (e.g., 2025-10-08_21-34-55)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Ensure the outputs directory exists
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)

        # Build the full path to the CSV file
        filename = f"complete_incidents_{timestamp}.csv"
        filepath = os.path.join(output_dir, filename)

        # Save the file
        save_incidents_to_csv(all_incidents, filepath)
        print(f"Saved {len(all_incidents)} incidents to '{filepath}'.")
    else:
        print("No incidents were found during the crawl.")

    # Display usage statistics for the LLM strategy
    llm_strategy.show_usage()


async def main():
    """
    Entry point of the script.
    """
    await crawl_incidents()


if __name__ == "__main__":
    strategy = get_llm_strategy()
    asyncio.run(main())
