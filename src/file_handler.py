import csv
import os
import ast
from typing import Dict, List, Union
from multiprocessing import Pool


class FileReader:
    def read_csv(self, file_path: str, file_name: str) -> List[Dict[str, str]]:
        raise NotImplementedError("Subclasses must implement read_csv method")


class CSVFileReader(FileReader):

    def read_csv(self, file_path: str, file_name: str) -> Union[Dict[str, str], None]:
        try:
            with open(file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    yield row
        except FileNotFoundError:
            print(f"File '{file_name}' not found.")

        except PermissionError:
            print(f"No permission to read file '{file_name}'.")

    def read_csv_parallel(self, file_paths: List[str], file_names: List[str]) -> List[Dict[str, str]]:
        with Pool() as pool:
            results = pool.starmap(self.read_csv, zip(file_paths, file_names))
        return results

    def _extract_key(self, file_name):
        pass


class TicketFileReader(CSVFileReader):

    @staticmethod
    def _extract_key(file_name: str, **kwargs) -> str:
        return file_name.split('.csv')[0]


class WinningNumbersFileReader(CSVFileReader):

    @staticmethod
    def _extract_key(file_name: str, **kwargs) -> str:
        return file_name.split('_result.csv')[0]


class FileWriter:

    def __init__(self, file_name: str, write_content: dict, directory: str) -> None:
        self.file_name = file_name
        self.write_content = write_content
        self.directory = directory
        self.file_path = f"{directory}/{file_name}"

    def write(self) -> None:
        self._check_directory_exists()

        try:
            # Set to store unique ticket IDs
            unique_ticket_ids = set()

            # Check if the file exists and read existing records
            existing_records = []
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as file:
                    for line in file:
                        record_dict = ast.literal_eval(
                            line.strip())  # Safely evaluate the string as a Python expression
                        ticket_id = record_dict.get('ticket_id')
                        if ticket_id:
                            unique_ticket_ids.add(ticket_id)
                            existing_records.append(record_dict)

            # Open the file in write mode
            with open(self.file_path, 'w') as file:
                # Write existing records back to the file
                for record in existing_records:
                    file.write(str(record) + '\n')

                # Write new records if they have unique ticket IDs
                if 'ticket_id' in self.write_content and self.write_content['ticket_id'] not in unique_ticket_ids:
                    file.write(str(self.write_content) + '\n')
        except Exception as e:
            print(f"Could not write to file with error message: {e}")

    def _check_directory_exists(self) -> None:
        if not os.path.exists(self.directory):
            try:
                os.makedirs(self.directory)
            except Exception as e:
                print(f"Could not create directory at {self.directory} with error message: {e}")
