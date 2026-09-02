# Annotation Guide: Executable Mathematical Knowledge

You are assigned one Mathematical Methods unit and one Specialist Mathematics unit. Complete one unit before starting the next. Existing files show the format only; recheck their mathematics before reuse.

- **Atom:** one reusable, independently executable mathematical rule.
- **Background operation:** routine exact work used to connect atoms; it is not counted as an atom.
- **Atomic template:** one question testing one atom.
- **Strict composite:** a connected graph in which a later atom consumes an earlier result.

## 1. Targets and sources

| Item | Per unit | Both units |
|---|---:|---:|
| Selected atoms | 13–18 | 26–36 |
| Atomic templates | 18–23 | 36–46 |
| Composite templates | 28–32 | 56–64 |

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

An atom must have clear inputs, necessary preconditions, one procedure, one exact semantic output, and a directly supporting source code.

Granularity rules:

- Numerical, notation, sign, boundary, and ordinary parameter variations are not new atoms.
- Merge two directions of a simple reversible relation when they use the same procedure.
- Split when the output, theorem, or procedure changes.
- If one rule produces an input needed by another, use two atoms.
- Only lead-provided exact scalar arithmetic, comparison, and typed construction or access are background operations. Formatting and normalization are automatic, not nodes.
- Every selected transformation, substitution, classification, recurrence rule, or solution method is an atom. Do not replace it with a generic `transform`, `case`, `iterate`, `solve`, or `simplify` operation.
- A point, vector, matrix, complex number, interval, or finite set is one output, not several coordinate atoms.

For example, degree/radian conversion is one reversible atom. Calculating a discriminant and classifying roots from it are two atoms.

Record only the selected 13–18 atoms in `atoms.jsonl`. Every selected atom needs an atomic template. Use the shared ID style (`func.*`, `trig.*`, `prob.*`). IDs must be unique across the combined dataset. Reuse an existing ID only for the same rule.

```json
{"id":"trig.period.tan_linear",
 "statement":"The fundamental period of tan(b*x+c) is pi/abs(b), for b != 0.",
 "source":"ACMMM038"}
```

## 3. Atomic templates and solvers

An atomic template must execute its named atom exactly once. Give every other non-background prerequisite and ask for exactly the atom's output. Add a second template only for a different direction or representation.

```json
{"id":"angle_deg_rad",
 "atom":"trig.degree_radian_conversion",
 "template":"Convert {deg} degrees to radians.",
 "vars":{"deg":{"type":"int","min":1,"max":360}},
 "solver":"angle_deg_rad"}
```

Required fields are `id`, `atom`, `template`, `solver`, and either `vars`, `cases`, or both.

- `vars` contains independently sampled fields.
- `cases` contains complete combinations that must stay together.
- A field must not appear in both `vars` and `cases`.
- Process fields in this order: `cases` → `vars` → `derive` in written order → constraints.
- Expressions may refer only to values already available.
- Put constraints in template data, not in `generate.py`.

Questions must read naturally: use `2x-3`, not `2x+-3`, `1x+0`, or `+0`. Use `term()`, `linfac()`, and `shift()` through `derive` when needed.

Every template names a function in `solver.py`. The solver must:

- match the name in the template;
- accept the sampled values it needs;
- return one exact value, not a float when an exact answer exists;
- reject invalid inputs rather than changing the question.

Each atom ID must map to one reusable function in `common_solvers.py`, with declared input/output types and preconditions. `solver.py` holds only thin wrappers that adapt template parameter names and add the display form.

An atom function may use a code condition only for its one declared rule; it must not choose, call, or hide another atom. If the solution applies a recurrence-step atom more than once, use one DAG node per application.

Use one consistent exact representation for structured values. Before Specialist annotation begins, confirm that the graph runner and checker can pass and compare symbolic expressions, equations, sequences, points, vectors, matrices, complex numbers, intervals, and sets.

## 4. Strict composites

Start from a natural multi-step problem. Use textbooks and past papers only to identify normal problem types; write the question in original wording. Solve it, then identify the atoms used. Do not join unrelated atoms merely to increase depth.

The graph records one valid reference program, not the only valid solution. Annotate one program only; do not enumerate alternative methods. Rewrite a problem when an obvious shortcut bypasses almost the whole annotated chain.

Do not begin composite annotation until the runner supports the format below.

Store the question in `composite.jsonl` and the reference program in `graphs.jsonl`. Each node contains `node_id`, `atom_id`, and `args`; the program names its returned node. Use `{"question":"a"}` for a question field, `{"ref":"n1"}` for an earlier node, and `{"literal":3}` for an exact literal.

```json
{"id":"quadratic_root_nature","nodes":[
  {"node_id":"n1","atom_id":"func.quad.discriminant",
   "args":{"a":{"question":"a"},"b":{"question":"b"},"c":{"question":"c"}}},
  {"node_id":"n2","atom_id":"func.quad.root_nature",
   "args":{"D":{"ref":"n1"}}}],
 "return":{"ref":"n2"}}
```

Reuse registered functions; do not rewrite formulas in the graph. The reference program is a finite DAG and the composite solver. Use only lead-provided `kernel.*` operations; do not add model-visible case, loop, or recursion syntax.

A composite is accepted only if:

1. The graph is connected and acyclic, and every node lies on a path to the final answer.
2. At least two different atoms occur on one dependency path, and the later atom consumes the earlier result.
3. Every node is needed in the reference solution.
4. Each node performs exactly its named atom and performs the same operation for every generated case.
5. One node does not hide another atom or the problem's main transformation.
6. Routine connecting work uses an approved `kernel.*` operation; copying or reformatting is not a node.
7. Every atom has an accepted atomic template.
8. The prompt is one natural question with one exact semantic answer.
9. No allowed draw makes a step a no-op.
10. The executable reference program returns the exact answer.

Each node returns one semantic value. A structured mathematical object counts as one value.

**Atom depth** is the longest dependency chain of atom applications. Ignore `kernel.*` operations.

| Atom depth | Templates per unit |
|---:|---:|
| 2 | 9–11 |
| 3 | 7–9 |
| 4 | 5–7 |
| 5 | 3–4 |
| 6 | 2–3 |
| **Total** | **28–32** |

Every standard atomic and composite template must produce at least 128 distinct rendered questions among 200 attempts. Deduplicate rendered questions, not parameter assignments. Ask the lead before using a genuinely finite template.

For composites, also reject a template if one final answer occurs in more than 60% of 200 samples.

## 5. Composite coverage

`validate.py` reports this; it counts atom calls in `graphs.jsonl` and ignores `kernel.*` operations:

- at least 70% of atoms with templates appear in a composite;
- every atom used in composites appears in at least two composites;
- focal atoms appear in 6–10 composite templates and at most 40% of the unit; other atoms appear in at most 25%;
- every used atom has at least two different direct partner atoms;
- at least 12 atom pairs recur in structurally different composites.

A partner is a directly dependent atom after ignoring intervening `kernel.*` operations. Do not paraphrase one graph merely to increase a count.

## 6. Exclusions

Do not create templates requiring subjective judgement, open-ended modelling, proof writing, diagram interpretation, technology-only solutions, inexact checking, several independent questions, or a tiny repeated case set.

## 7. Validation and review

```bash
python3 annotate_graphs.py     # after every graph edit
python3 check_program.py <id>  # one composite reference program
python3 validate.py            # the whole bank, plus your atom-spread targets
python3 audit.py               # answers re-derived with sympy, independently
```

The audits re-derive answers independently of the atom functions, so they catch wrong mathematics. They still cannot tell you whether a node carries the right atom label, whether every node is needed, or whether the question is natural: two atoms with the same arithmetic pass either way. Read every composite yourself. Do not rely on the exit code alone; resolve every reported problem.

Cross-review one other annotator's batch: 15 atom statements, 10 atomic templates with three cases each, and approximately 30 composites with reference programs and three cases each. Mark each item `correct`, `incorrect`, or `uncertain`, with a short note for the last two.

## 8. Time and deliverables

| Stage | Time |
|---|---:|
| Source coverage and atom selection | 6 hours |
| Atomic templates and solvers, including routine runs | 10 hours |
| Composite templates and reference programs, including routine runs | 49 hours |
| Cross-review | 7 hours |
| **Total** | **approximately 72 hours** |

The lead performs final acceptance review separately; it is not included in these 72 hours.

Submit:

```text
coverage_<unit>.tsv
atoms.jsonl
templates.jsonl
composite.jsonl
graphs.jsonl
common_solvers.py
solver.py
generate.py
reviews/<annotator_id>.jsonl
```
