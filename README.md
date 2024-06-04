# PRM800K: 一个过程监督数据集

#### [[Blog Post]](https://openai.com/research/improving-mathematical-reasoning-with-process-supervision) [[Paper]](https://arxiv.org/abs/2305.20050)

本资源库随论文[Let&#39;s Verify Step by Step](https://arxiv.org/abs/2305.20050)一起发布，并介绍了其中引入的 PRM800K 数据集。PRM800K 是一个过程监督数据集，包含 [MATH](https://github.com/hendrycks/math)数据集中由模型生成的问题解决方案的 800,000 个步骤级正确性标签。有关 PRM800K 和该项目的更多信息，请参阅论文。

We are releasing the raw labels as well as the instructions we gave labelers during phase 1 and phase 2 of the project. Example labels can be seen in the image below.

<p align="center">
    <img src="prm800k/img/interface.png" height="300"/>
</p>

## 数据

 `data/` 文件夹包含我们的标签，格式为新行分隔的 "json "数据列表。这些数据是通过 [Git LFS](https://git-lfs.com/) 上传的，你需要安装它才能正确克隆版本库。

每一行代表一个完整的解决方案样本，可以包含许多步骤级标签。下面是一行注释：

```javascript
{
  // UUID representing a particular labeler.
  "labeler": "340d89bc-f5b7-45e9-b272-909ba68ee363",

  // The timestamp this trajectory was submitted.
  "timestamp": "2023-01-22T04:34:27.052924",

  // In phase 2, we split our data collection into generations, using our best
  // PRM so far to pick which solutions to score in the next generation.
  // In phase 1, this value should always be null.
  "generation": 9,

  // In each generation, we reserve some solutions for quality control. We serve
  // these solutions to every labeler, and check that they agree with our
  // gold labels.
  "is_quality_control_question": false,

  // generation -1 was reserved for a set of 30 questions we served every
  // labeler in order to screen for base task performance.
  "is_initial_screening_question": false,

  // Metadata about the question this solution is a response to.
  "question": {
    // Text of the MATH problem being solved.
    "problem": "What is the greatest common factor of $20 !$ and $200,\\!000$?  (Reminder: If $n$ is a positive integer, then $n!$ stands for the product $1\\cdot 2\\cdot 3\\cdot \\cdots \\cdot (n-1)\\cdot n$.)",
    // Ground truth solution from the MATH dataset.
    "ground_truth_solution": "The prime factorization of $200,000$ is $2^6 \\cdot 5^5$. Then count the number of factors of $2$ and $5$ in $20!$. Since there are $10$ even numbers, there are more than $6$ factors of $2$. There are $4$ factors of $5$. So the greatest common factor is $2^6 \\cdot 5^4=\\boxed{40,\\!000}$.",
    // Ground truth answer.
    "ground_truth_answer": "40,\\!000",

    // The full steps of the model-generated solution. This is only set for
    // phase 2 where we pre-generated all solutions that we labeled.
    "pre_generated_steps": [
      "I want to find the largest positive integer that divides both $20 !$ and $200,\\!000$ evenly.",
      "One way to do this is to factor both numbers into prime factors and look for the common ones.",
      "I know that $200,\\!000 = 2^5\\cdot 10^4 = 2^9\\cdot 5^4$.",
      "To find the prime factorization of $20 !$, I can use the fact that it is the product of all the positive integers from $1$ to $20$.",
      "For each prime number $p$ between $1$ and $20$, I can count how many multiples of $p$ are in that range.",
      "For example, there are $10$ multiples of $2$ between $1$ and $20$, namely $2, 4, 6, \\dots, 20$.",
      "But there are also $5$ multiples of $4$, which is $2^2$, and $2$ multiples of $8$, which is $2^3$, and $1$ multiple of $16$, which is $2^4$.",
      "So, the total power of $2$ in $20 !$ is $10 + 5 + 2 + 1 = 18$.",
      "Similarly, there are $4$ multiples of $5$, namely $5, 10, 15, 20$, so the power of $5$ in $20 !$ is $4$.",
      "There are $6$ multiples of $3$, namely $3, 6, 9, \\dots, 18$, but there are also $2$ multiples of $9$, which is $3^2$, so the power of $3$ in $20 !$ is $6 + 2 = 8$.",
      "There are $2$ multiples of $7$, namely $7$ and $14$, so the power of $7$ in $20 !$ is $2$.",
      "There are $1$ multiple of each of the other prime numbers $11, 13, 17$, and $19$, so the powers of those primes in $20 !$ are $1$ each.",
      "Therefore, the prime factorization of $20 !$ is $2^{18}\\cdot 3^8\\cdot 5^4\\cdot 7^2\\cdot 11\\cdot 13\\cdot 17\\cdot 19$.",
      "To find the greatest common factor of $20 !$ and $200,\\!000$, I need to take the lowest power of each common prime factor.",
      "The only common prime factors are $2$ and $5$, and the lowest powers are $9$ and $4$, respectively.",
      "So, the greatest common factor is $2^9\\cdot 5^4 = 512\\cdot 625 = 320,\\!000$.\n\n# Answer\n\n320,000"
    ],
    // The answer given as the end of the pre-generated solution. We can see
    // this solution is incorrect.
    "pre_generated_answer": "320,000",
    // The score given by our PRM to this solution. This one isn't rated very
    // highly!
    "pre_generated_verifier_score": 0.010779580529581414
  },

  // The human data we collected for this solution, containing correctness
  // labels for each step of the solution.
  "label": {
    "steps": [
      // Each object here represents labels for one step of the solution.
      {
        // 每个步骤将包含一个或多个完成项。这些是模型在轨迹的这一步输出的候选步骤。在第一阶段，我们经常收集候选步骤的标签，而在第二阶段，我们只收集第一次错误之后的候选步骤的标签，因此大多数补全列表都是单子。
        "completions": [
          {
            // Text of the step.
            "text": "I want to find the largest positive integer that divides both $20 !$ and $200,\\!000$ evenly.",
            // The rating the labeler gave to this step. Can be -1, 0, or +1.
            // This is a 0 because it isn't incorrect, but it does not make
            // any progress.
            "rating": 0,
            // The labeler can flag steps that they don't know how to label.
            // This is rarely used.
            "flagged": null
          }
        ],
        // In phase 1, if all completions were rated -1, we allowed labelers to
        // write their own +1 step. This is null for all steps in phase 2.
        "human_completion": null,
        // The index of the completion "chosen" at this step, or null if the
        // human_completion was used. You can reconstruct the solution
        // trajectory like:
        // [
        //     step["human_completion"] if step["chosen_completion"] is None
        //     else step["completions"][step["chosen_completion"]]["text"]
        //     for step in labeled_solution["label"]["steps"]
        // ]
        "chosen_completion": 0
      },
      {
        "completions": [
          {
            "text": "One way to do this is to factor both numbers into prime factors and look for the common ones.",
            "rating": 0,
            "flagged": null
          }
        ],
        "human_completion": null,
        "chosen_completion": 0
      },
      {
        // Some steps contain multiple alternative completions, and each one
        // gets a rating.
        "completions": [
          {
            "text": "I know that $200,\\!000 = 2^5\\cdot 10^4 = 2^9\\cdot 5^4$.",
            "rating": -1,
            "flagged": null
          },
          {
            "text": "To factor $20 !$, I can use the fact that every factorial is a multiple of every number less than or equal to it.",
            "rating": 0,
            "flagged": false
          },
          {
            "text": "I can use a factor tree to find the prime factors of $200,\\!000$: $200,\\!000 = 2^5\\cdot 10^4 = 2^5\\cdot 2^4\\cdot 5^4 = 2^9\\cdot 5^4$.",
            "rating": -1,
            "flagged": false
          },
          {
            "text": "I can use a factor tree to find the prime factors of $200,\\!000$.",
            "rating": 0,
            "flagged": false
          },
          {
            "text": "To factor $20 !$, I can use the fact that any factorial is divisible by all the primes less than or equal to the input.",
            "rating": 0,
            "flagged": false
          }
        ],
        "human_completion": null,
        "chosen_completion": null
      }
    ],
    // Total time in milliseconds spent on labeling this solution.
    "total_time": 278270,
    // Final result of labeling this solution. Will be one of:
    //   - "found_error": In phase 2 we stop labeling a solution after the
    //                    first error is found.
    //   - "solution": We reached a step that concluded in the correct answer
    //                 to the problem.
    //   - "bad_problem": The labeler reported the problem as broken.
    //   - "give_up": The labeler was stuck (the problem was taking too long,
    //                or the instructions were unclear) and moved onto the
    //                next problem.
    "finish_reason": "found_error"
  }
}
```

## 说明

 `instructions/`文件夹包含我们在项目每个阶段给贴标人员的说明文件。
在项目每个阶段给贴标人员的说明文件。

## 答案评分

`grading/` 文件夹包含了我们用来判断模型输出的答案是否与 Hendrycks 的数学数据集中的真实答案正确匹配的 python 分级逻辑。我们借鉴了 Hendrycks 在 `math_normalize.py` 中的数学归一化逻辑，并在 `grader.py` 中使用 sympy 检查表达式是否相等。我们推荐使用 `grader.grade_answer(model_answer, gt_answer)`
来判断解决方案是否正确。

一般来说，答案分级比较困难。这种分级逻辑的设计是保守的，有时会拒绝正确答案，但这种情况比 MATH 的规范化逻辑要少。我们的逻辑有时可能会接受不正确的答案，不过我们已经努力将这种情况降到最低。

## MATH Splits

正如 Let's Verify Step by Step, 一文中所述，我们使用了非标准的 MATH 训练/测试分割。

> 为了避免在 7500 个 MATH 训练问题上过度拟合的风险，我们将训练集扩展到了 4500 个 MATH 测试问题。因此，我们只在剩余的 500 个被排除的问题上评估我们的模型。我们随机均匀地选择了这 500 个测试问题，我们相信它们能够代表整个测试集。

math_splits/`文件夹包含我们在`train.jsonl `和`test.jsonl` 文件中选择的拆分问题。你需要 [Git LFS](https://git-lfs.com/) 来克隆这些文件。

## 得分样本

我们发布了用于评估大规模 ORM 和 PRM 的所有大规模模型样本，与论文中的图 3 相对应。每个测试问题都有 1860 个得分样本。未能在 1024 个标记内得出答案的解决方案会被丢弃，这导致某些问题的样本少于 1860 个。我们在 "Best-of-N "评估逻辑中考虑到了这一点。

评估 PRM：

```bash
python eval/eval.py --method prm
```

评估 ORM:

```bash
python eval/eval.py --method orm
```

## 引用

请使用以下 BibTeX 条目引用该数据集：

```
@article{lightman2023lets,
      title={Let's Verify Step by Step}, 
      author={Lightman, Hunter and Kosaraju, Vineet and Burda, Yura and Edwards, Harri and Baker, Bowen and Lee, Teddy and Leike, Jan and Schulman, John and Sutskever, Ilya and Cobbe, Karl},
      journal={arXiv preprint arXiv:2305.20050},
      year={2023}
}
```
