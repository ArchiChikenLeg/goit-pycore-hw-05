import sys
import re
from collections import defaultdict

def parse_log_line(line: str) -> dict:
    match = re.match(r'(\S+ \S+) (\S+) (.*)', line)
    if match:
        return {
            'datetime': match.group(1),
            'level': match.group(2),
            'message': match.group(3)
        }
    return None

def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parsed_line = parse_log_line(line.strip())
                if parsed_line:
                    logs.append(parsed_line)
    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        sys.exit(1)
    
    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    return [log for log in logs if log['level'].upper() == level.upper()]

def count_logs_by_level(logs: list) -> dict:
    counts = defaultdict(int)
    for log in logs:
        counts[log['level'].upper()] += 1
    return counts

def display_log_counts(counts: dict):
    print(f"{'Рівень логування':<15}| {'Кількість':<8}")
    print('-' * 25)
    for level, count in counts.items():
        print(f"{level:<15}| {count:<8}")

def main():
    if len(sys.argv) < 2:
        print("Використання: python task3.py <шлях до файлу логів> [рівень]")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    logs = load_logs(log_file_path)
    counts = count_logs_by_level(logs)
    
    display_log_counts(counts)

    if len(sys.argv) == 3:
        level = sys.argv[2].upper()
        filtered_logs = filter_logs_by_level(logs, level)
        if filtered_logs:
            print(f"\nДеталі логів для рівня '{level}':")
            for log in filtered_logs:
                print(f"{log['datetime']} - {log['message']}")
        else:
            print(f"Не знайдено записів для рівня '{level}'.")

if __name__ == "__main__":
    main()
