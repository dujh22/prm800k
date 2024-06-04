import json
import random
from collections import defaultdict


def select_data_balanced(datas, sample_size=6000, tolerance=0.01, max_steps=9, min_steps=3):
    assert sample_size <= len(datas), "Sample size exceeds the total available data"

    # Step 1: Calculate total number of 0s and 1s in the entire dataset
    total_0, total_1 = 0, 0
    for data in datas:
        labels = [step["label"] for step in data["solution"].values()]
        total_0 += labels.count(0)
        total_1 += labels.count(1)

    print(f"Total 0s: {total_0}; Total 1s: {total_1}")

    selected_data = []
    selected_0, selected_1 = 0, 0
    length_distribution = defaultdict(int)

    # If not enough data is selected, adjust the tolerance dynamically
    while len(selected_data) < sample_size:
        # Randomly shuffle the original data to add randomness
        random.shuffle(datas)
        for data in datas:
            if len(selected_data) >= sample_size:
                break

            if data in selected_data:
                continue

            labels = [step["label"] for step in data["solution"].values()]
            count_0 = labels.count(0)
            count_1 = labels.count(1)
            data_length = len(labels)
            if data_length > max_steps or data_length < min_steps:
                continue
            # Compute preliminary counts if the data were to be added
            new_selected_0 = selected_0 + count_0
            new_selected_1 = selected_1 + count_1

            # Relax the tolerance and check again
            if abs(new_selected_0 - new_selected_1) <= tolerance * (new_selected_0 + new_selected_1):
                selected_data.append(data)
                selected_0, selected_1 = new_selected_0, new_selected_1
                length_distribution[data_length] += 1

    # Verify the counts
    final_0, final_1 = 0, 0
    for _data in selected_data:
        labels = [step["label"] for step in _data["solution"].values()]

        final_0 += labels.count(0)
        final_1 += labels.count(1)

    print(f"Selected data count for 0: {final_0}; Selected data count for 1: {final_1}")
    print(f"Final selected data size: {len(selected_data)}")
    print(f"Length distribution of selected data: {dict(length_distribution)}")

    # Write the selected data to a new JSONL file
    with open(f"prm800k_balanced{sample_size}.jsonl", "w", encoding="utf-8") as f:
        for _data in selected_data:
            for step_key, step in _data["solution"].items():
                if step["label"] == 0:
                    _data["solution"][step_key]["label"] = -1
            f.write(json.dumps(_data) + "\n")


if __name__ == "__main__":
    with open("prm800k.jsonl", "r", encoding="utf-8") as f:
        lines = f.readlines()
        datas = []
        for line in lines:
            data = json.loads(line)
            if data["true_solution"] != '':
                datas.append(data)

        select_data_balanced(datas)