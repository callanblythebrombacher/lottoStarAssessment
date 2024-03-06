import os

from src.file_handler import TicketFileReader, WinningNumbersFileReader, FileWriter
from src.winning_numbers_finder import WinningNumbersFinder


class CSVProcessor:
    def __init__(self):
        user_input_ticket_entries_dir = input("Please enter the directory path of your ticket entries csv files: ")
        user_input_winning_numbers_dir = input("Please enter the directory path of your winning number csv files: ")
        user_input_file_directory = input("Please enter the directory path that your output csv files must save to: ")

        self.ticket_entries_dir = user_input_ticket_entries_dir
        self.winning_numbers_dir = user_input_winning_numbers_dir
        self.output_dir = user_input_file_directory
        self.ticket_file_reader = TicketFileReader()
        self.winning_numbers_file_reader = WinningNumbersFileReader()
        self.winning_numbers_finder = WinningNumbersFinder

    def process_csv_files(self):
        for ticket_file_name in os.listdir(self.ticket_entries_dir):
            if ticket_file_name.endswith(".csv"):
                winning_number_file_name = ticket_file_name.replace(".csv", "_result.csv")
                ticket_file_path = os.path.join(self.ticket_entries_dir, ticket_file_name)
                winning_number_file_path = os.path.join(self.winning_numbers_dir, winning_number_file_name)

                ticket_records_generator = self.ticket_file_reader.read_csv(ticket_file_path, ticket_file_name)
                winning_number_records = self.winning_numbers_file_reader.read_csv(
                    winning_number_file_path,
                    winning_number_file_name,
                )

                # Convert generators to lists
                ticket_records = list(ticket_records_generator)
                winning_number_record = list(winning_number_records)[0]

                for ticket_record in ticket_records:
                    ticket_record['file_name'] = ticket_file_name
                    self.process_winning_numbers(ticket_record, winning_number_record)
        print('complete')

    def process_winning_numbers(self, ticket_record, winning_number_record):
        result = self.winning_numbers_finder(winning_number_record).find_winning_tickets(ticket_record)
        file_name = ticket_record['file_name'].replace('.csv', '_lottery_results.csv')
        file_writer = FileWriter(file_name, result, self.output_dir)
        file_writer.write()
