# Annotation Guide: Executable Mathematical Knowledge and Strict Compositions

Each annotator is assigned one Mathematical Methods unit and one Specialist Mathematics unit. The project is building a controlled knowledge-and-composition benchmark, not a curriculum inventory with one benchmark item for every source statement.

The distinction below is fundamental:

- The **full atom inventory** records every valid source-derived atom and has no numerical quota.
- The **benchmark atom set** is a smaller, deduplicated, executable set reused across many problems.
- An **atomic template** tests one benchmark atom.
- A **strict composite template** contains a connected dependency graph in which later operations consume earlier results.

For this project, the benchmark should contain more strict composite templates than benchmark atom IDs. Reuse is necessary to distinguish missing knowledge from failure to compose known knowledge.

## 1. Project-wide targets

Targets are global, not targets to multiply independently for every annotator.

| Artifact | Project target |
|---|---:|
| Full source-derived atom inventory | No quota |
| Canonical benchmark atom IDs | 114-128; hard planning ceiling 140 |
| Accepted atomic generator templates | 160-180 |
| Accepted strict composite templates | 240-280; planning midpoint about 260 |

The current expansion assumes an existing corpus of approximately 114 atomic templates and 63 candidate composites. First count the unique canonical atom IDs: 114 atomic templates do not necessarily mean 114 distinct atoms. Re-audit the existing composites under the strict dependency rules in this guide before counting them as accepted. Do not create hundreds of new atom IDs merely to cover every source statement in the executable benchmark.

Assuming four annotators, each annotator should normally be responsible for:

- approximately 25-35 assigned canonical atoms;
- approximately 35-45 accepted atomic templates in total under their responsibility, counting retained existing templates;
- normally 12-20 new or substantially revised atomic templates when the current corpus is retained;
- 55-60 composite drafts or revisions, with at least **50 accepted strict composites** after review;
- one completed cross-review batch.

If the number of annotators changes, the lead reviewer must divide the remaining global gap. Do not multiply the project-wide atom target by the annotator count.

## 2. Source links

- Mathematical Methods: https://v8.australiancurriculum.edu.au/senior-secondary-curriculum/mathematics/mathematical-methods/?unit=Unit+1&unit=Unit+2&unit=Unit+3&unit=Unit+4
- Mathematical Methods glossary: https://v8.australiancurriculum.edu.au/media/1188/mathematical-methods-glossary.pdf
- Specialist Mathematics: https://v8.australiancurriculum.edu.au/senior-secondary-curriculum/mathematics/specialist-mathematics/?unit=Unit+1&unit=Unit+2&unit=Unit+3&unit=Unit+4
- Specialist Mathematics glossary: https://v8.australiancurriculum.edu.au/media/1191/specialist-mathematics-glossary.pdf

Use `ACMMM...` source codes for Mathematical Methods and `ACMSM...` source codes for Specialist Mathematics. The glossaries are references only.

## 3. Source coverage

Create a short coverage table for each assigned unit:

```text
source_code | decision | note
ACMMM...    | include  |
ACMMM...    | exclude  | short reason
```

Use:

- `include` when the content code contains usable exact-symbolic knowledge;
- `exclude` when it is unsuitable, for example because it is subjective, technology-dependent, proof-only, diagram-dependent, or cannot produce an exact answer.

`include` means that valid knowledge should be represented in the full inventory. It does not mean that every inventory atom must enter the current executable benchmark.

## 4. Full atom inventory

Create all valid atoms from the included content codes. Do not remove valid inventory atoms to meet a numerical target.

An atom is one reusable mathematical fact, definition, rule, formula, equivalence, constraint, or procedure.

```json
{"id":"trig.period.tan_linear","statement":"The fundamental period of tan(b*x+c) is pi/abs(b), for b != 0.","source":"ACMMM038"}
```

Use these rules:

1. The atom contains one reusable mathematical statement.
2. It has exactly one primary source code.
3. At least one exact solver-backed question could test it.
4. Numerical instances of the same rule are examples, not separate atoms.
5. If two rules can be known independently, keep them separate in the inventory.
6. If two proposed atoms state the same executable rule in different words, merge them during normalization.

Store the full inventory in `data/atoms.jsonl`.

## 5. Canonical benchmark atoms

The lead reviewer maintains one project-wide canonical registry in `data/selected_atoms.json`. Annotators must use existing canonical IDs whenever possible.

For each assigned unit pair:

1. Map the unit inventory to existing canonical atoms.
2. Identify genuine ontology gaps.
3. Propose a new benchmark atom only when no existing atom can support the required exact solver behavior.
4. Obtain lead approval before adding it to `selected_atoms.json`.

An annotator should normally propose no more than four new canonical atoms. This is a ceiling, not a quota. A valid source atom may remain inventory-only.

The selected set should:

- cover both assigned units;
- contain the major exact formulas, constraints, and procedures;
- contain every atom used by an accepted composite;
- remain small enough that atoms recur across structurally different composites.

## 6. Atomic templates

Every canonical atom needs at least one clean atomic template somewhere in the project. Add a second template only when it tests a genuinely different direction, representation, or use. Central atoms may receive a third template when it is structurally distinct.

```json
{
  "id":"angle_deg_rad",
  "atom":"trig.degree_radian_conversion",
  "template":"Convert {deg} degrees to radians.",
  "vars":{"deg":{"type":"choice","values":[15,30,45,60,90,120,180]}},
  "solver":"angle_deg_rad"
}
```

An atomic template contains:

```text
id        unique template ID
atom      canonical atom ID
template  question text
vars      independently sampled variables
cases     fixed valid combinations, when needed
solver    matching function name
```

Use `vars`, `cases`, or both. Do not add answers, train/test splits, free-form traces, or subjective difficulty labels to template records.

A good atomic template:

- primarily tests its assigned atom;
- has one exact final answer;
- excludes invalid parameter values;
- reads like a normal mathematics question;
- has enough support to avoid trivial repetition, or is explicitly routed to the auxiliary finite-support set.

## 7. Variables and formatting

Put generation constraints in template data, not inside `generate.py`.

```json
"vars":{
  "b":{"type":"int","min":-12,"max":12,"exclude":[0]},
  "c":{"type":"int","min":-6,"max":6}
}
```

Use `cases` when values must remain coupled.

The generator must format expressions naturally:

```text
2x-3
2x+3
2x
-x+3
```

Do not generate forms such as `2x+-3`, `1x+0`, or `+0`. Shared formatter functions in `generate.py` may create derived display placeholders.

## 8. Solvers and generation

Every template must point to an exact solver function.

A solver should:

- use the same name as the template's `solver` field;
- accept the sampled variables it needs;
- return the exact final answer as a string or a fixed machine-checkable structure;
- avoid floating-point approximations;
- reject invalid parameter combinations rather than silently changing the question.

```python
def angle_deg_rad(deg):
    return pf(deg, 180)
```

`generate.py` should read the JSONL files, sample valid values, call the solver, and write generated examples. Do not hard-code atom or template records inside the generator.

Generated examples should remain minimal:

```json
{"id":"atom_0001","template_id":"angle_deg_rad","question":"Convert 90 degrees to radians.","answer":"pi/2"}
```

## 9. Strict composite templates

Create composites problem-first:

1. Write one natural mathematical objective.
2. Solve it completely.
3. Identify the indispensable major atom applications.
4. Draw the dependency graph.
5. Confirm that later nodes consume earlier outputs.
6. Add safe variables or cases.
7. Implement an exact solver.

Example:

```json
{
  "id":"exponential_rate_time",
  "atoms":[
    "calculus.derivative.exponential_linear",
    "algebra.exponential_equation.logarithm"
  ],
  "template":"Let f(t)={A}*exp({k}*t), where {A}>0 and {k}>0. Find the exact value of t for which f'(t)={A}*{k}*{M}.",
  "vars":{
    "A":{"type":"int","min":1,"max":9},
    "k":{"type":"int","min":1,"max":6},
    "M":{"type":"int","min":2,"max":12}
  },
  "composition":{
    "nodes":[
      {"id":"n1","atom":"calculus.derivative.exponential_linear"},
      {"id":"n2","atom":"algebra.exponential_equation.logarithm"}
    ],
    "edges":[["n1","n2"]]
  },
  "solver":"exponential_rate_time"
}
```

The target on the right is constructed so that every sampled case is valid. When a different template needs coupled inequalities, enforce them through valid `cases` or a supported constraint mechanism; prose alone is not a generation constraint.

### 9.1 Composite acceptance tests

A composite is accepted only when all of the following are true:

1. **Connected dependency:** its graph is connected and acyclic.
2. **Consumption:** at least one later node consumes an earlier node's result.
3. **Indispensability:** removing any listed node makes the intended solution incomplete.
4. **Non-redundancy:** no listed atom merely restates another listed atom.
5. **Unified objective:** independent `(a), (b), (c)` question bundles are not strict composites unless their branches feed a shared final result.
6. **Exact verification:** the final output can be checked symbolically.
7. **Naturalness:** the problem is mathematically motivated, not a random concatenation of atoms.
8. **Parameter validity:** every generated instance is valid under the solver's assumptions.

Parallel branches are allowed only when they converge into a shared downstream node. A list of independently answerable features, such as amplitude, period, and midline, is an auxiliary multipart task rather than a strict composite.

Move useful rejected bundles to `data/auxiliary_multipart.jsonl`; do not count them toward the strict-composite target.

### 9.2 Atom count and graph representation

The composite size is the number of indispensable atom-application nodes, not the number of subquestions and not necessarily the number of unique atom IDs. If one atom is applied twice, it creates two graph nodes.

The `atoms` list and `composition.nodes` must agree. `composition.edges` records which intermediate results are consumed downstream. Do not infer a dependency merely from the order of prose.

The validation pipeline computes three different structural quantities:

- `node_count`: number of indispensable atom-application nodes;
- `dependency_depth`: number of nodes on the longest directed path;
- `topology`: chain, branch, merge, or mixed.

Do not call `node_count` the dependency depth. A four-node merge graph may have dependency depth three.

### 9.3 Instance support

A standard training template should support at least 128 distinct valid question-answer instances. The validation script should attempt 200 generations and confirm at least 128 unique questions.

A mathematically useful template with genuinely finite support may be stored in `data/auxiliary_finite_support.jsonl` and exhaustively enumerated. It does not count toward the standard training-template quota unless the lead reviewer explicitly approves it.

## 10. Composite size and workload targets

The default accepted-composite planning target per annotator is:

| Required atom applications | Accepted templates |
|---:|---:|
| 2 | 16 |
| 3 | 13 |
| 4 | 9 |
| 5 | 6 |
| 6 | 4 |
| 7 | 2 |
| **Total** | **50** |

These are team-planning quotas, not permission to create artificial long problems. Annotators may exchange size responsibilities with lead approval when one unit naturally supports more large connected compositions than another.

Do not pad a problem with unnecessary algebra to increase its atom count. A larger node count is accepted only when every node passes the indispensability test.

With four annotators, this plan adds approximately 200 accepted composites. Combined with the re-audited current corpus, the expected final total is approximately 240-280 strict composites.

## 11. Reuse and interface coverage

The benchmark requires repeated semantic components, not merely many unique records.

Use these project-level checks:

- every composition-core atom should appear in at least three accepted training composites;
- the median composition-core atom should appear in at least four accepted composites;
- central atoms should appear in six or more structurally different composites;
- every composition-core atom should interact with at least two different partner atoms;
- each annotator should deliberately reuse at least 12 directed atom interfaces in two or more structurally different composites;
- an interface labelled as seen should occur in at least two distinct training templates;
- at least 70% of training edge occurrences should belong to repeated interface types;
- all atoms used in held-out composites must have atomic exposure;
- template splits are assigned centrally after annotation, using graph structure rather than random generated instances.

Do not repeatedly paraphrase the same composition skeleton merely to raise recurrence counts.

## 12. Central split after annotation

Annotators do not assign splits. After deduplication and QA, the lead creates graph-structural splits. At a final total near 260 strict composites, the planning allocation is:

| Split | Templates | Purpose |
|---|---:|---|
| Train | 170 | Learn composition over exposed atoms and interfaces |
| Development | 20 | Model selection and curriculum thresholds |
| Same-size structural test | 40 | Held-out combinations or graph motifs at familiar sizes |
| Deeper/interface stress test | 30 | Longer paths and deliberately held-out interfaces |
| **Total** | **260** | |

All test-composite atoms must receive atomic exposure. For a held-out interface, both endpoint atoms must occur in at least three training composites with other partners. Generated instances from one template never cross splits.

## 13. Exclusions

Do not create strict benchmark templates that require:

- subjective judgement;
- open-ended modelling choices;
- technology as the only way to obtain the answer;
- graph drawing as the final output;
- long proof writing;
- diagram-dependent reasoning that cannot be represented symbolically;
- answers that cannot be checked exactly;
- several independent questions presented as one composite;
- redundant atoms that allow one listed atom to bypass the intended dependency;
- a tiny finite set of repeated semantic cases without auxiliary routing.

## 14. Automated validation and manual QA

Before submission, validation must check:

- unique IDs and valid JSONL;
- every referenced atom exists in the canonical registry;
- every graph is connected and acyclic;
- every edge references existing nodes;
- the atom list and graph nodes agree;
- the solver runs successfully on 100 randomly generated or exhaustively enumerated cases;
- generated questions and answers are deterministic for fixed variables;
- standard templates pass the 128-unique-question support test;
- no train/test split information is embedded in the template record.

Manually inspect:

- three generated outputs per atomic template;
- five generated outputs per composite template;
- every boundary case and every exceptional case such as undefined values or zero denominators.

Automated validity must be 100%. Output targets count accepted records after QA, not first drafts.

## 15. Cross-review

Every accepted strict composite receives independent cross-review. Each annotator reviews one balanced batch from another annotator containing:

- 15 atom-statement/source-code pairs;
- 10 atomic templates with solver output on three generated cases each;
- approximately 50 composite templates with their dependency graphs, solvers, and three generated cases each;
- a few known correct or intentionally incorrect check items supplied by the lead.

Mark each item:

```text
correct
incorrect
uncertain
```

Add a short note for `incorrect` or `uncertain`. The lead reviewer resolves remaining uncertain cases. Every composite with five or more nodes also receives lead review. Revisions required by cross-review are part of the annotator's accepted-output target.

## 16. Expected output and time

Expected output per annotator across both assigned units:

- a complete source-coverage table;
- all valid source atoms added to or reconciled with `data/atoms.jsonl`;
- approximately 25-35 assigned canonical benchmark atoms reviewed;
- no more than four proposed new benchmark atoms unless the lead approves an exception;
- approximately 35-45 accepted atomic templates under the annotator's responsibility, counting retained existing templates;
- 55-60 strict composite drafts or revisions and at least 50 accepted strict composites;
- exact solver coverage for every submitted template;
- generation code or shared-generator additions needed by those templates;
- one completed cross-review record.

Approximate working time:

| Stage | Time |
|---|---:|
| Source coverage and full-inventory reconciliation | 4 hours |
| Canonical atom normalization and assignment review | 2 hours |
| Atomic templates and solvers | 8 hours |
| Composite planning and dependency graphs | 5 hours |
| Composite templates and solvers | 30 hours |
| Automated generation and manual QA | 5 hours |
| Cross-review, revisions, and final cleanup | 6 hours |
| **Total** | **approximately 60 hours** |

Normal variation of approximately 55-65 hours is expected. No annotator should exceed 80 hours. If natural strict composites cannot be produced within the assigned units and time budget, report the shortfall to the lead rather than padding depth, duplicating templates, or weakening acceptance rules.

## 17. Deliverable files

Submit or update:

```text
data/coverage_<unit>.tsv
data/atoms.jsonl
data/selected_atoms.json
data/atom_templates.jsonl
data/composite_templates.jsonl
data/auxiliary_multipart.jsonl          # when applicable
data/auxiliary_finite_support.jsonl     # when applicable
solvers.py
generate.py
validation_report.json
reviews/<annotator_id>.jsonl
```

The final accepted count is taken from validated canonical files after deduplication and review, not from the number of local drafts.
