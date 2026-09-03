# Annotation Guide: Executable Mathematical Knowledge

You are assigned one Mathematical Methods unit and one Specialist Mathematics unit. Select atoms for both units first. After the lead merges all unit atom lists, complete the remaining work one unit at a time.

- **Atom:** one reusable, independently executable mathematical rule.
- **Background operation:** routine exact work used to connect atoms; it is not counted as an atom.
- **Atomic template:** one question testing one atom.
- **Strict composite:** a connected graph in which a later atom consumes an earlier result.

## 1. Targets and sources

| Item | Per unit | Both units |
|---|---:|---:|
| Selected atoms | 13–18 | 26–36 |
| Atomic templates | 18–23 | 36–46 |
| Composite templates | 32–36 | 64–72 |

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

Record the 13–18 atoms selected from each unit in `atoms.jsonl`. Every new atom needs an atomic template. Use the shared ID style (`func.*`, `trig.*`, `prob.*`). Atom IDs and functions are shared across all units: reuse an existing atom for the same rule and do not create another atomic template for it. Ask the lead before adding a missing cross-unit atom.

```json
{"id":"trig.period.tan_linear",
 "statement":"The fundamental period of tan(b*x+c) is pi/abs(b), for b != 0.",
 "source":"ACMMM038",
 "concept":"tan_period"}
```

The `statement` must describe what the function returns, not a general fact about the graph. `concept` groups atoms that are the same idea, and coverage is counted per concept; give two atoms the same `concept` when they are one rule you had to split. Omit it and the atom is its own concept.

## 3. Atomic templates and solvers

An atomic template must execute its named atom exactly once. Give every other non-background prerequisite and ask for exactly the atom's output. Add a second template only for a different direction or representation.

```json
{"id":"angle_deg_rad",
 "atom":"trig.degree_radian_conversion",
 "template":"Convert {deg} degrees to radians.",
 "vars":{"deg":{"type":"int","min":1,"max":360}},
 "solver":"angle_deg_rad"}
```

Required fields are `id`, `atom`, `template`, `solver`, and either `vars`, `cases`, or both. Use `vars` for independent draws, `cases` for combinations that must stay together, and `derive` for fields computed from earlier values. A field cannot appear in both `vars` and `cases`. Process them in this order: `cases` → `vars` → `derive` → constraints. Keep constraints in the template data.

Questions must read naturally: use `2x-3`, not `2x+-3`, `1x+0`, or `+0`.

Every atomic template names a function in `solver.py`. The solver must:

- match the name in the template;
- accept the sampled values it needs;
- return one exact value, not a float when an exact answer exists;
- reject invalid inputs rather than changing the question.

Each atom ID maps to one reusable function in `atoms.py`. `kernel.py` contains the shared background operations and must not be edited. `solver.py` contains only thin wrappers for atomic templates.

Each function in `atoms.py` must implement only its named atom. If a solution applies the same atom more than once, use one graph node per application.

## 4. Strict composites

Start from a natural multi-step problem. Use textbooks and past papers only to identify normal problem types; write the question in original wording. Solve it, then identify the atoms used. Do not join unrelated atoms merely to increase depth.

The graph records one valid reference program, not the only valid solution. Annotate one program only; do not enumerate alternative methods. Rewrite a problem when an obvious shortcut bypasses almost the whole annotated chain.

Store the question in `composite.jsonl` and the reference program in `graphs.jsonl`. Each node contains `node_id`, `atom_id`, and `args`; the program names its returned node. Use `{"question":"a"}` for a question field, `{"ref":"n1"}` for an earlier node, and `{"literal":3}` for an exact literal.

```json
{"id":"quadratic_root_nature","nodes":[
  {"node_id":"n1","atom_id":"func.quad.discriminant",
   "args":{"a":{"question":"a"},"b":{"question":"b"},"c":{"question":"c"}}},
  {"node_id":"n2","atom_id":"func.quad.root_nature",
   "args":{"D":{"ref":"n1"}}}],
 "return":{"ref":"n2"}}
```

Each graph node calls an existing atom or `kernel.*` function. Do not rewrite atom formulas directly in the graph. The reference program is also the composite solver.

Composites name no solver. Record one worked example in `composite.jsonl`: the values you used and the answer you computed by hand.

```json
"example": {"vars": {"a_val": 1, "b_val": -5, "c_val": 6}, "answer": "-8"}
```

`check_program.py` runs your program on those values and fails if it does not reproduce your answer. Work the example out by hand before writing the program; one copied from the program's output checks nothing.

A composite is accepted only if:

1. The graph is connected and acyclic, and every node lies on a path to the final answer.
2. At least two different atoms occur on one dependency path, and the later atom consumes the earlier result.
3. Every node is needed in the reference solution.
4. Each node performs only its named atom, consistently across all generated questions.
5. Routine connecting work uses an approved `kernel.*` operation; copying or reformatting is not a node.
6. Every atom has an accepted atomic template.
7. The prompt is one natural question with one exact answer.
8. No allowed draw makes a step a no-op.
9. The executable reference program returns the exact answer.

**Atom depth** is the longest dependency chain of atom applications. Ignore `kernel.*` operations.

| Atom depth | Templates per unit |
|---:|---:|
| 2 | 11–12 |
| 3 | 9–10 |
| 4 | 6–7 |
| 5 | 4 |
| 6 | 2–3 |
| **Total** | **32–36** |

Every standard atomic and composite template must produce at least 128 distinct rendered questions among 200 attempts. Deduplicate rendered questions, not parameter assignments. Ask the lead before using a genuinely finite template.

For composites, also reject a template if one final answer occurs in more than 60% of 200 samples.

## 5. Composite coverage

Counted from atom calls in `graphs.jsonl`, ignoring `kernel.*` operations. Atoms sharing a concept count as one: a forward transformation and its inverse are the same concept.

`validate.py` reports these:

- at least 70% of concepts with templates appear in a composite;
- every concept used in composites appears in at least two composites;
- no concept appears in more than 25% of composites.

The lead checks these by hand; no tool enforces them:

- 8–12 central, reusable atoms as focal, each in 6–10 composite templates and at most 40% of the unit;
- every used atom has at least two different direct partner atoms;
- at least 12 atom pairs recur in structurally different composites.

A partner is a directly dependent atom after ignoring intervening `kernel.*` operations. Do not paraphrase one graph merely to increase a count.

## 6. Validation and review

```bash
python3 annotate_graphs.py     # after every graph edit
python3 check_program.py <id>  # one composite reference program
python3 validate.py            # the whole bank, plus your atom-spread targets
```

Run all three commands and resolve every reported error. Mathematical correctness and natural wording are checked during cross-review.

At the end you will cross-review another annotator's batch. Instructions for that come separately.

## 7. Time and deliverables

Time for both assigned units:

| Stage | Time |
|---|---:|
| Source coverage and atom selection | 6 hours |
| Atomic templates and solvers | 9 hours |
| Composite templates and reference programs | 48 hours |
| Cross-review | 7 hours |
| **Total** | **approximately 70 hours** |

The lead performs final acceptance review separately; it is not included in these 70 hours.

Submit:

```text
coverage_<unit>.tsv
atoms.jsonl
templates.jsonl
composite.jsonl
graphs.jsonl
atoms.py
solver.py
reviews/<annotator_id>.jsonl
```
