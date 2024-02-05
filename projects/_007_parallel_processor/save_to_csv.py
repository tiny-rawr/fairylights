import csv
import json


def save_generated_data_to_csv(filename):
    responses = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            responses.append(data)

    # Create a CSV file for writing
    with open('projects/_007_parallel_processor/output.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write the header row
        csv_writer.writerow(['Original Data', 'Generated Bio'])

        # Iterate through the responses and extract both original data and generated bio
        for response in responses:
            original_data = response[0]["messages"][1]["content"]
            generated_bio = response[1]["choices"][0]["message"]["content"]

            # Write data to the CSV file
            csv_writer.writerow([original_data, generated_bio])

    print("CSV file created successfully.")


if __name__ == "__main__":
    save_generated_data_to_csv('projects/_007_parallel_processor/requests_completed.jsonl')
