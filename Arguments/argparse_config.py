
import argparse

def get_parser():
    parser = argparse.ArgumentParser(description='LinkedIn Scraper')
    parser.add_argument('--base_url', type=str, help='Base URL for LinkedIn search')
    parser.add_argument('--log', action='store_true', help='Enable logging of results')
    parser.add_argument('--location', type=str, help='Filter results by location')
    parser.add_argument('--lt', action='store_true', help='Filter for less technical positions')
    parser.add_argument('--csv', action='store_true', help='Export results to CSV')
    parser.add_argument('--max_page', type=int, help='Maximum page number to scrape')
    return parser
