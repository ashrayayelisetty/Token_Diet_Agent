# Token-Diet Agent Design Doc

## 1. Objective
To reduce LLM API costs by routing simple queries to cheap models and pruning context semantically.

## 2. The Logic Flow (The Graph)
1. **START** -> [Router Node]
2. [Router Node] -> decides "gpt-4o-mini" vs "gpt-4o"
3. [Router Node] -> [Pruner Node]
4. [Pruner Node] -> removes "fluff" from context
5. [Pruner Node] -> [LLM Executor]
6. [LLM Executor] -> [Judge Node]
7. [Judge Node] -> If Quality < Threshold -> RE-RUN with gpt-4o -> [LLM Executor]
8. [Judge Node] -> If Quality is Good -> **END**