# Annotation Guide: Executable Mathematical Knowledge

This guide is for creating the symbolic evaluation benchmark. Work on one assigned unit at a time and keep each unit in a separate directory.

- **Atom:** one reusable, independently executable mathematical rule.
- **Background operation:** routine exact work used to connect atoms; it is not counted as an atom.
- **Atomic template:** one question testing one atom.
- **Strict composite:** a connected graph in which a later atom consumes an earlier result.

## 1. Targets and sources

**Per unit: target 20–22 selected atoms, two atomic templates per atom, and 34 composite templates.** Do not change atom granularity merely to reach the target.

Official sources:

- [Mathematical Methods](https://v8.australiancurriculum.edu.au/senior-secondary-curriculum/mathematics/mathematical-methods/?unit=Unit+1&unit=Unit+2&unit=Unit+3&unit=Unit+4)
- [Mathematical Methods glossary](https://v8.australiancurriculum.edu.au/media/1188/mathematical-methods-glossary.pdf)
- [Specialist Mathematics](https://v8.australiancurriculum.edu.au/senior-secondary-curriculum/mathematics/specialist-mathematics/?unit=Unit+1&unit=Unit+2&unit=Unit+3&unit=Unit+4)
- [Specialist Mathematics glossary](https://v8.australiancurriculum.edu.au/media/1191/specialist-mathematics-glossary.pdf)

Use `ACMMM...` codes for Methods and `ACMSM...` codes for Specialist. Make a short source table for the whole assigned unit:

```text
source_code | decision | note
ACMMM...    | include  |
ACMMM...    | defer    | valid but not selected
ACMMM...    | exclude  | short reason
```

Use `exclude` for content that is subjective, proof-only, technology-dependent, diagram-dependent, or cannot produce an exact answer. Use `defer` for valid executable content outside the selected atom set.

## 2. Atoms

Treat each official content description as the initial atom candidate.

- Keep it as one atom if one normal question can test it with one procedure and one exact output.
- If it contains independent operations, split only the operations selected for this dataset.
- If it has no exact executable output, defer or exclude it.
- Do not identify every possible sub-atom in the unit.

An atom must have clear inputs, necessary preconditions, one procedure, one exact output, and a directly supporting source code.

Granularity rules:

- Numerical, notation, sign, boundary, and ordinary parameter variations are not new atoms.
- Merge two directions of a simple reversible relation when they use the same procedure.
- Split when the output, theorem, or procedure changes.
- If one rule produces an input needed by another, use two atoms.
- Use only the background operations already provided in `kernel.py`; do not add new ones.
- A mathematical rule containing selected curriculum knowledge must be an atom, not a background operation.
- A point, vector, matrix, complex number, interval, or finite set is one output, not several coordinate atoms.

For example, degree/radian conversion is one reversible atom. Calculating a discriminant and classifying roots from it are two atoms.

Record the atoms selected from the unit in `atoms.jsonl`. Every selected atom needs two atomic templates. Use the shared ID style (`func.*`, `trig.*`, `prob.*`). Ask the lead before adding an atom outside the assigned unit.

```json
{"id":"func.quad_general.axis","unit":"MM1",
 "statement":"The axis of symmetry of y = ax² + bx + c is x = −b/(2a), for a != 0.",
 "source":"ACMMM011"}
```

`statement` is the mathematical rule the function implements; write it from the function, not from a picture of the graph.

## 3. Atomic templates

An atomic template must execute its named atom exactly once. Give every other non-background prerequisite and ask for exactly the atom's output. Create two genuinely different templates per atom: use a different direction, representation, or question form rather than changing only wording or numbers.

```json
{"id":"quad_general_axis","unit":"MM1",
 "atom":"func.quad_general.axis",
 "template":"Find the x-coordinate of the axis of symmetry of y = {qd}.",
 "vars":{"a":{"type":"int","min":-6,"max":6,"exclude":[0]},
         "b":{"type":"int","min":-9,"max":9},
         "c":{"type":"int","min":-9,"max":9}},
 "derive":{"qd":"quad(a,b,c)"},
 "args":{"coeffs":[{"question":"a"},{"question":"b"},{"question":"c"}]}}
```

Required fields are `id`, `unit`, `atom`, `template`, `args`, and either `vars`, `cases`, or both. Use `vars` for independent draws, `cases` for combinations that must stay together, and `derive` for fields computed from earlier values. A field cannot appear in both `vars` and `cases`. Process them in this order: `cases` → `vars` → `derive` → constraints. Keep constraints in the template data.

Questions must read naturally: use `2x-3`, not `2x+-3`, `1x+0`, or `+0`.

An atomic template is a one-node program: `args` binds the atom's parameters the same way a composite node does. Use `{"question":"a"}` for a sampled field and `{"literal":3}` for an exact literal. The answer is the atom's output, so you write no code for a template.

Add `"display"` only when the answer needs a form other than the plain value: `"polynomial"` for a coefficient tuple, `"capitalize"`, or a pattern such as `"x = {}"`.

Each atom ID maps to one function in `atoms.py`, which returns an exact value and never display text. The background operations live in `kernel.py` and must not be edited.

Each function in `atoms.py` must implement only its named atom. If a solution applies the same atom more than once, use one graph node per application. Atomic templates must cover the input forms and ranges in which the atom is used by composites.

## 4. Strict composites

Start from a natural multi-step problem. Use textbooks and past papers only to identify normal problem types; write the question in original wording. Solve it, then identify the atoms used. Do not join unrelated atoms merely to increase depth.

Pure-mathematical and real-world settings are both allowed, but the question must state every fact needed for the mathematics and require no outside factual knowledge.

The graph records one valid reference program, not the only valid solution. Annotate one program only; do not enumerate alternative methods. Rewrite a problem when an obvious shortcut bypasses almost the whole annotated chain.

Store the question in `composite.jsonl` and the reference program in `graphs.jsonl`. A composite row contains `id`, `unit`, `atoms`, `template`, its generation fields, and `example`. Each graph node contains `node_id`, `atom_id`, and `args`; the program names its returned node. Use `{"question":"a_val"}` for a question field, `{"ref":"n1"}` for an earlier node, and `{"literal":3}` for an exact literal.

```json
{"id":"quad_axis_evaluate","unit":"MM1","nodes":[
  {"node_id":"n1","atom_id":"func.quad_general.axis",
   "args":{"coeffs":[{"question":"a_val"},{"question":"b_val"},{"question":"c_val"}]}},
  {"node_id":"n2","atom_id":"func.notation.evaluate",
   "args":{"coeffs":[{"question":"a_val"},{"question":"b_val"},{"question":"c_val"}],
           "x":{"ref":"n1"}}}],
 "return":{"ref":"n2"}}
```

Each graph node calls an existing atom or `kernel.*` function. Do not rewrite atom formulas directly in the graph. A dependency must be mathematically meaningful; matching input and output types alone is not enough.

Record one worked example in `composite.jsonl`: the values you used and the answer you computed by hand.

```json
{"example":{"vars":{"a_val":2,"b_val":-3,"c_val":-8},"answer":"-73/8"}}
```

`check_program.py` runs your program on those values and fails if it does not reproduce your answer. Work the example out by hand before writing the program; one copied from the program's output checks nothing.

A composite is accepted only if:

1. The graph is connected and acyclic, and every node lies on a path to the final answer.
2. At least two different atoms occur on one dependency path, and the later atom consumes the earlier result.
3. Every node is needed in the reference solution.
4. Each node performs only its named atom, consistently across all generated questions.
5. Routine connecting work uses an approved `kernel.*` operation; copying or reformatting is not a node.
6. Every atom has two accepted atomic templates.
7. The prompt is one natural question with one exact answer.
8. No allowed draw makes a step a no-op.
9. The executable reference program returns the exact answer.

**Atom depth** is the longest dependency chain of atom applications. Ignore `kernel.*` operations.

| Atom depth | Composite templates per unit |
|---:|---:|
| 2 | 10 |
| 3 | 8 |
| 4 | 7 |
| 5 | 5 |
| 6 | 4 |
| **Total** | **34** |

Include branched or merged graphs where they arise naturally; there is no separate topology quota.

Every standard atomic and composite template must support at least 128 distinct rendered questions. Ask the lead before using a genuinely finite template.

For composites, also reject a template if one final answer occurs in more than 60% of 200 samples.

Do not submit two composites with the same atom-labeled dependency graph when only the wording or sampled values differ. This structural check does not apply to the two atomic templates for an atom.

## 5. Composite coverage

Counted from atom calls in `graphs.jsonl`, ignoring `kernel.*` operations.

`validate.py` reports these:

- at least 70% of atoms with templates appear in a composite;
- every atom used in composites appears in at least two composites;
- no atom appears in more than 25% of composites.

Do not create an unnatural dependency merely to meet a count.

## 6. Validation and review

```bash
python3 annotate_graphs.py     # after every graph edit
python3 check_program.py <id>  # one composite reference program
python3 validate.py            # the whole unit, plus its atom-spread targets
```

Run all three commands and resolve every reported error. Mathematical correctness and natural wording are checked during cross-review.

At the end you will cross-review another annotator's batch. Instructions for that come separately.

## 7. Time and deliverables

Planning budget per annotator:

| Stage | Time per annotator |
|---|---:|
| Source coverage and atom selection | 6 hours |
| Atomic functions and templates | approximately 16 hours |
| Composite templates and reference programs | 48 hours |
| Cross-review | 7 hours |
| **Total** | **approximately 77 hours** |

Across four annotators, the total annotation budget is approximately 308 hours. The lead performs final acceptance review separately.

Submit:

```text
coverage_<unit>.tsv
atoms.jsonl
templates.jsonl
composite.jsonl
graphs.jsonl
atoms.py
reviews/<annotator_id>.jsonl
```
