
class WinningNumbersFinder:
    def __init__(self, winning_numbers):
        self._winning_numbers = winning_numbers

    def find_winning_tickets(self, ticket_entry):
        winning_tickets = {}

        try:
            return self._is_winning_ticket(ticket_entry)
        except Exception as e:
            print(f"An error occurred while processing tickets: {e}")

    @staticmethod
    def _flatten_entries(entries):
        return [entry for sublist in entries for entry in sublist.values()]

    def _is_winning_ticket(self, ticket_entry):
        try:
            file_name, ticket_id, ticket_main_balls, ticket_sub1, ticket_sub2 = self._parse_ticket_entry(ticket_entry)
            winning_numbers_entry = self._winning_numbers
            winning_main_balls, winning_sub1, winning_sub2 = self._parse_winning_numbers(winning_numbers_entry)

            result = self._check_match_count(
                ticket_main_balls,
                ticket_sub1,
                ticket_sub2,
                winning_main_balls,
                winning_sub1,
                winning_sub2
            )
            result['ticket_id'] = ticket_id
            return result
        except Exception as e:
            print(f"An error occurred while processing winning ticket: {e}")

    @staticmethod
    def _parse_winning_numbers(winning_numbers_entry):
        winning_numbers_entry_list = winning_numbers_entry['mainballs;sub1;sub2'].split(';')
        main_balls = winning_numbers_entry_list[0]
        sub1 = winning_numbers_entry_list[1]
        sub2 = winning_numbers_entry_list[2]

        winning_main_balls = list(map(int, main_balls.split(':')))
        winning_sub1 = int(sub1) if sub1 else None
        winning_sub2 = int(sub2) if sub2 else None
        return winning_main_balls, winning_sub1, winning_sub2

    @staticmethod
    def _parse_ticket_entry(ticket_entry):
        ticket_id = ticket_entry['ticket_id;mainballs;sub1;sub2'].split(';')[0]
        main_balls = ticket_entry['ticket_id;mainballs;sub1;sub2'].split(';')[1]
        sub1 = ticket_entry['ticket_id;mainballs;sub1;sub2'].split(';')[2]
        sub2 = ticket_entry['ticket_id;mainballs;sub1;sub2'].split(';')[3]
        file_name = ticket_entry['file_name']

        ticket_main_balls = list(map(int, main_balls.split(':')))

        ticket_sub1 = int(sub1) if sub1 else None
        ticket_sub2 = int(sub2) if sub2 else None

        return file_name, ticket_id, ticket_main_balls, ticket_sub1, ticket_sub2

    @staticmethod
    def _check_match_count(main_balls, sub1, sub2, winning_main_balls, winning_sub1, winning_sub2):
        main_ball_match_count = sum(1 for ball in main_balls if ball in winning_main_balls)

        sub_ball_match_count = 0
        if sub1 == winning_sub1 and winning_sub1:
            sub_ball_match_count += 1

        if sub2 == winning_sub2 and winning_sub2:
            sub_ball_match_count += 1

        is_jackpot = (main_ball_match_count == len(main_balls)
                      and sub_ball_match_count == (2 if winning_sub2 and winning_sub1 else 1))

        return {
            'main_balls_match_count': main_ball_match_count,
            'sub_balls_match_count': sub_ball_match_count,
            'is_jackpot': is_jackpot
        }
