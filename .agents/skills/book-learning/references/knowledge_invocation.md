# Knowledge Invocation

Knowledge invocation is the process of using method cards in real tasks.

The Agent should not repeat the method card. It should transform the method card into task-specific analysis.

## Index Boundary

`book-learning-skill` outputs index-ready metadata, but it does not require a vector database.

- Text scent indexing is the baseline capability.
- Vector indexing is optional enhancement.
- `.cache/book-learning/{book_slug}/run_manifest.json` is the bridge file for indexers and routing systems.
- If `knowledge_root` exists, update the configured scent index path or `{knowledge_root}/气味索引.md`.
- If no `knowledge_root` exists, set `index_status` to `no_knowledge_root` and report that scent indexing was skipped.
- External vector search / embedding skills may read `run_manifest.json` and index the canonical reading notes.
- If no vector system exists, update the text scent index or tell the user vector indexing can be done later.

## Invocation Flow

1. Identify the user task type.
2. Decide whether the cognitive toolbox is needed.
3. Query the scene trigger index.
4. Use task semantics and scent to select 1-3 method cards.
5. Load the selected method cards.
6. Do not restate the method cards.
7. Convert method cards into analysis actions for the current task.
8. Complete the user task.
9. Self-check whether the selected cards were useful and appropriate.

## Invocation Rules

- Simple Q&A does not need method card invocation.
- Complex judgment, plan evaluation, decision advice, retrospective analysis, and structured writing should consider invocation.
- Call at most 3 method cards.
- Do not mechanically repeat book content.
- Do not turn the answer into reading notes.
- Method cards must serve the current task.
- If no method card fits, complete the task directly and note that a future card may be useful.

## Quality Check

After answering, check:

- Did the invocation improve the output?
- Did the method card serve the actual task?
- Was any selected card unnecessary?
- Is a new card needed for future similar tasks?
