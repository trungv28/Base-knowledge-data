# Annotation Guide: Executable Mathematical Knowledge and Strict Compositions

Each annotator is assigned one Mathematical Methods unit and one Specialist Mathematics unit. The project is building a controlled knowledge-and-composition benchmark, not a curriculum inventory with one benchmark item for every source statement.

The distinction below is fundamental:

- The **full atom inventory** records every valid source-derived atom and has no numerical quota.
- The **benchmark atom set** is a smaller, deduplicated, executable set reused across many problems.
- An **atomic template** tests one benchmark atom.
- A **strict composite template** contains a connected dependency graph in which later operations consume earlier results.

For this project, each benchmark atom should appear in several composites. Reuse is necessary to distinguish missing knowledge from failure to compose known knowledge.

## 1. Project-wide targets

Targets are global, not targets to multiply independently for every annotator.

| Artifact | Project target |
|---|---:|
| Full source-derived atom inventory | No quota |
| Canonical benchmark atom IDs | 114-128; hard planning ceiling 140 |
| Accepted atomic generator templates | 160-180 |
| Accepted strict composite templates | 240-280 |

This pack contains 139 atoms, 116 atomic templates and 17 accepted composites. The 17 are what remained after re-auditing 63 candidates under the rules in section 9. Because the retained corpus is that small, nearly all of the composite target must be newly written, and the per-annotator share below is higher than a simple division would suggest. First count the unique canonical atom IDs: 116 atomic templates do not necessarily mean 116 distinct atoms. Do not create hundreds of new atom IDs merely to cover every source statement in the executable benchmark.

Assuming four annotators, each annotator should normally be responsible for:

- approximately 25-35 assigned canonical atoms;
- approximately 35-45 accepted atomic templates in total under their responsibility, counting retained existing templates;
- normally 12-20 new or substantially revised atomic templates when the current corpus is retained;
- about 80 composite drafts or revisions, with at least **59 accepted strict composites** after review;
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

Do not generate forms such as `2x+-3`, `1x+0`, or `+0`. `generate.py` provides `term()`, `linfac()` and `shift()` for this; call them from `derive` to build display placeholders.

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

Example, written as two records. In `composite.jsonl`, the question:

```json
{"id":"repeated_root_third",
 "template":"The cubic p(x) = x³{b_term}{c_term}{d_term} has a repeated root at x = {root_val}. Find its other root.",
 "vars":{"root_val":{"type":"int","min":-6,"max":6,"exclude":[0]},
         "other_val":{"type":"int","min":-6,"max":6,"exclude":[0,"root_val"]}},
 "derive":{"b_val":"-(2*root_val + other_val)","b_term":"term(b_val, \"x²\")"},
 "constraints":["abs(b_val) > 1"],
 "solver":"repeated_root_third"}
```

In `graphs.jsonl`, the steps:

```json
{"id":"repeated_root_third","nodes":[
  {"node_id":"n1","atom_id":"func.poly.repeated_root","expr":"2 * root_val"},
  {"node_id":"n2","atom_id":"func.poly.cubic_repeated_distinct","expr":"str(-b_val - n1)"}]}
```

Write only `node_id`, `atom_id` and `expr`. Running `annotate_graphs.py` derives the wiring from the identifiers each `expr` reads and rewrites the `atoms` list, so wiring cannot drift from behaviour. Never hand-edit either.

Write the solver from your own working, not by transcribing the node expressions. `validate.py` checks that the graph and the solver agree on every draw, and that check only means something if the two were derived independently.

Here `b_val` is derived from the two roots, so the cubic shown really does have that repeated root. When values must be coupled, enforce it through `derive`, `constraints` or valid `cases`; prose alone is not a generation constraint.

### 9.1 Composite acceptance tests

A composite is accepted only when all of the following are true.

**Structure**

1. **Connected and acyclic**, with every step on a path to the final answer.
2. **Every step computes something.** Reading a value off a form counts: `y = a/(x−4)` has asymptote `x = 4`. Copying a number the question states outright does not, and neither does repeating or reformatting an earlier result.
3. **Depth at least two.** Ignoring steps that only copy from the question, the longest chain of steps must be two or more.
4. **At least two different atoms.** Plain arithmetic — adding, multiplying, forming a fraction — is not an atom. Mark those steps `"atom_id":"arithmetic"`; they do not count toward the two.
5. **Every step is needed.** Removing one leaves the solution incomplete.

**Labels**

6. **Label what the step does,** not what the problem is about. A step that computes a vertex is not labelled *y-intercept*. If no atom fits and the step is not arithmetic, the curriculum is missing an atom — report it rather than choosing the nearest one.
7. **Every atom you use needs an atomic template.** Without one, a wrong answer on the composite cannot be separated from simply not knowing the atom, which is the measurement this benchmark exists to make. Validation fails if it is missing.

**The question**

8. **One question, one answer.** Do not ask for two things and return one, and do not bundle independent `(a), (b), (c)` parts.
9. **Naturalness:** mathematically motivated, not a random concatenation of atoms.

**Generation**

10. **Exact and always valid.** The final answer is checkable symbolically, and every sampled instance is a valid question.
11. **Every value a step reads from the question must appear in the question text.** Validation fails otherwise.
12. **No no-op draws.** Exclude values that make a step do nothing: dilation by factor 1, shift by 0 units, a target of 1.
13. **The final answer must vary.** Sample 200 instances and reject if one answer covers more than 60%. A step whose own output never changes is fine when its atom is a constant fact such as `C(n,0) = 1`.

### 9.2 Size and graph representation

Composite size is the number of steps, not the number of subquestions and not the number of distinct atoms. One atom applied twice is two steps.

Depth is the longest chain of steps, not the step count. A four-step graph in which three steps feed one final step has depth two.

Every intermediate step must produce a single value: an int, a string, or a `Fraction`. A list, tuple or bool cannot round-trip through a model's written answer. Only the final step may return several parts.

### 9.3 Instance support

A standard template should support at least 128 distinct valid question-answer instances. The validation script should attempt 200 generations and confirm at least 128 unique questions.

A mathematically useful template with genuinely finite support may be stored in `data/auxiliary_finite_support.jsonl` and exhaustively enumerated. It does not count toward the standard template quota unless the lead reviewer explicitly approves it.

## 10. Composite size and workload targets

Strict acceptance means a share of drafts do not survive, so plan drafts above the accepted target. Deep graphs are also harder than they look once arithmetic steps stop counting: budget more time for the 5- and 6-step rows than their numbers suggest.

The default accepted-composite target per annotator is:

| Required atom applications | Accepted templates |
|---:|---:|
| 2 | 20 |
| 3 | 16 |
| 4 | 12 |
| 5 | 7 |
| 6 | 4 |
| **Total** | **59** |

Do not pad a problem with extra algebra to raise its step count; arithmetic steps do not count. A larger graph is accepted only when every step passes test 5.

With four annotators this adds approximately 236 accepted composites. Combined with the 17 retained from the re-audit, the expected final total is 240-280 strict composites.

## 11. Reuse and interface coverage

The benchmark requires repeated semantic components, not merely many unique records. Check your own set:

- every atom you use should appear in at least three of your accepted composites;
- every atom you use should interact with at least two different partner atoms;
- deliberately reuse at least 12 directed atom interfaces in two or more structurally different composites.

Do not repeatedly paraphrase the same composition skeleton merely to raise recurrence counts.

## 12. Exclusions

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

## 13. Automated validation and manual QA

Before submission, validation must check:

- unique IDs and valid JSONL;
- every referenced atom exists in the canonical registry;
- every graph is connected and acyclic;
- every edge references existing nodes;
- the atom list and graph nodes agree;
- the solver runs successfully on 100 randomly generated or exhaustively enumerated cases;
- generated questions and answers are deterministic for fixed variables;
- standard templates pass the 128-unique-question support test;
- every step carries an `atom_id`, or `"arithmetic"`;
- every atom used by a composite has a working atomic template;
- no step repeats or only reformats an earlier step;
- every value a step reads from the question appears in the question text.

Run `python3 check.py <id>` on each composite as you write it. It reports tests 1, 2, 3, 4, 7, 10, 11, 12 and 13 for that one template and prints its answer distribution. Tests 5, 6, 8 and 9 are judgement; they stay with you and the cross-reviewer.

Manually inspect:

- three generated outputs per atomic template;
- five generated outputs per composite template;
- every boundary case and every exceptional case such as undefined values or zero denominators.

Automated validity must be 100%. Output targets count accepted records after QA, not first drafts.

## 14. Cross-review

Every accepted strict composite receives independent cross-review. Each annotator reviews one balanced batch from another annotator containing:

- 15 atom-statement/source-code pairs;
- 10 atomic templates with solver output on three generated cases each;
- approximately 30 composite templates with their dependency graphs, solvers, and three generated cases each;
- a few known correct or intentionally incorrect check items supplied by the lead.

Mark each item:

```text
correct
incorrect
uncertain
```

Add a short note for `incorrect` or `uncertain`. The lead reviewer resolves remaining uncertain cases. Every composite with five or more steps also receives lead review. Revisions required by cross-review are part of the annotator's accepted-output target.

## 15. Expected output and time

Expected output per annotator across both assigned units:

- a complete source-coverage table;
- all valid source atoms added to or reconciled with `data/atoms.jsonl`;
- approximately 25-35 assigned canonical benchmark atoms reviewed;
- no more than four proposed new benchmark atoms unless the lead approves an exception;
- approximately 35-45 accepted atomic templates under the annotator's responsibility, counting retained existing templates;
- about 80 strict composite drafts or revisions and at least 59 accepted strict composites;
- exact solver coverage for every submitted template;
- generation code or shared-generator additions needed by those templates;
- one completed cross-review record.

Approximate working time:

| Stage | Time |
|---|---:|
| Source coverage and full-inventory reconciliation | 4 hours |
| Canonical atom normalization and assignment review | 2 hours |
| Atomic templates and solvers | 8 hours |
| Composite planning and dependency graphs | 6 hours |
| Composite templates and solvers | 40 hours |
| Automated generation and manual QA | 5 hours |
| Cross-review, revisions, and final cleanup | 7 hours |
| **Total** | **approximately 72 hours** |

Normal variation of approximately 65-80 hours is expected. No annotator should exceed 90 hours. If natural strict composites cannot be produced within the assigned units and time budget, report the shortfall to the lead rather than padding depth, duplicating templates, or weakening acceptance rules.

## 16. Deliverable files

Submit or update:

```text
coverage_<unit>.tsv
atoms.jsonl
templates.jsonl                         # atomic templates
composite.jsonl                         # composite questions
graphs.jsonl                            # composite steps
solver.py
generate.py
check.py
data/auxiliary_multipart.jsonl          # when applicable
data/auxiliary_finite_support.jsonl     # when applicable
reviews/<annotator_id>.jsonl
```

The final accepted count is taken from validated canonical files after deduplication and review, not from the number of local drafts.
