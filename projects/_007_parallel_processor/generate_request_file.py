import json
import csv

def csv_to_array(csv_file_path):
    data = []
    with open(csv_file_path, "r") as input_file:
        csv_reader = csv.reader(input_file)
        for row in csv_reader:
            if row:
                data.append(row[0])
    return data

def generate_chat_completion_requests(csv_file_path, prompt, model_name="gpt-3.5-turbo-16k"):
    with open("projects/_007_parallel_processor/requests.jsonl", "w") as f:
        data_array = csv_to_array(csv_file_path)
        for data in data_array:
            # Create a list of messages for each request
            messages = [
                {"role": "system", "content": f"{prompt}"},
                {"role": "user", "content": str(data)}
            ]

            # Write the messages to the JSONL file
            json_string = json.dumps({"model": model_name, "messages": messages})
            f.write(json_string + "\n")