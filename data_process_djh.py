import json
import os
from tqdm import tqdm

def process_jsonl_files(input_folder, output_file):
    files = [f for f in os.listdir(input_folder) if f.endswith('.jsonl')]
    
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_name in files:
            with open(os.path.join(input_folder, file_name), 'r') as infile:
                for line in tqdm(infile, desc=f"Processing {file_name}"):
                    data = json.loads(line)

                    questions = data["question"]
                    true_solution = questions.get("ground_truth_solution", "")
                    answer = questions.get("answer", "")
                    pre_generated_verifier_score = questions.get("pre_generated_verifier_score", 0)

                    # 转换数据
                    new_data = {
                        "question": data["question"]["problem"],
                        "true_solution": true_solution,
                        "true_answer": answer,
                        "solution": {},
                        "solution_score": pre_generated_verifier_score,
                        "dataset": "PRM800K"
                    }

                    step_number = 1
                    for step in data["label"]["steps"]:
                        completions = step["completions"]
                        if completions and completions[0] is not None:
                            step_content = completions[0]["text"]
                            step_label = completions[0]["rating"]
                            if step_label == -1:
                                step_label = 0

                            new_data["solution"][f"Step {step_number}"] = {
                                "content": step_content,
                                "label": step_label
                            }
                            step_number += 1

                    # 写入新的jsonl文件
                    if len(new_data.get("solution", {})) > 0:
                        json.dump(new_data, outfile, ensure_ascii=False)
                        outfile.write('\n')

# 调用函数，传入文件夹路径和输出文件路径
process_jsonl_files('F://code//github//prm800k//prm800k//data', 'F://code//github//prm800k//prm800k//data2//prm800k.jsonl')
