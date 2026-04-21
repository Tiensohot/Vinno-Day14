#!/usr/bin/env python3
import json

with open('reports/benchmark_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# Thống kê
total = len(results)
passed = sum(1 for r in results if r['status'] == 'pass')
failed = total - passed

# Metrics
avg_faithfulness = sum(r['ragas']['faithfulness'] for r in results) / total
avg_relevancy = sum(r['ragas']['relevancy'] for r in results) / total
avg_judge_score = sum(r['judge']['final_score'] for r in results) / total

print(f'Tổng số cases: {total}')
print(f'Pass/Fail: {passed}/{failed}')
print(f'Faithfulness: {avg_faithfulness:.2f}')
print(f'Relevancy: {avg_relevancy:.2f}')
print(f'Judge Score: {avg_judge_score:.2f}')
print()
print('Top 3 failed cases:')
for i, r in enumerate(sorted(results, key=lambda x: x['judge']['final_score'])[:3], 1):
    print(f'{i}. {r["test_case"][:60]}... (Score: {r["judge"]["final_score"]})')
