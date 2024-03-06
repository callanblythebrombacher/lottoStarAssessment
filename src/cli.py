import click
from src.csv_processor import CSVProcessor


@click.command()
def main():
    csv_processor = CSVProcessor()
    csv_processor.process_csv_files()



# Instantiate the CSVProcessor class and run the process_csv_files method
if __name__ == "__main__":
    main()
