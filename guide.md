# Annotation Guide: Executable Mathematical Knowledge and Strict Compositions

You are assigned one Mathematical Methods unit and one Specialist Mathematics unit. You build the atoms and templates for those units yourself. The files in this pack are one unit's finished work: read them as an example of the format and the standard, not as a bank to draw from.

- An **atom** is one reusable mathematical fact from a source code.
- An **atomic template** tests one atom.
- A **strict composite template** is a connected graph in which later steps consume earlier results.

## 1. Your targets

- approximately 25-35 atoms for your unit;
- approximately 35-45 accepted atomic templates;
- at least **59 accepted composites**, spread over the depths in section 9;
- one completed cross-review batch.

## 2. Source links

- Mathematical Methods: https://v8.australiancurriculum.edu.au/senior-secondary-curriculum/mathematics/mathematical-methods/?unit=Unit+1&unit=Unit+2&unit=Unit+3&unit=Unit+4
- Mathematical Methods glossary: https://v8.australiancurriculum.edu.au/media/1188/mathematical-methods-glossary.pdf
- Specialist Mathematics: https://v8.australiancurriculum.edu.au/senior-secondary-curriculum/mathematics/specialist-mathematics/?unit=Unit+1&unit=Unit+2&unit=Unit+3&unit=Unit+4
- Specialist Mathematics glossary: https://v8.australiancurriculum.edu.au/media/1191/specialist-mathematics-glossary.pdf

Use `ACMMM...` codes for Mathematical Methods and `ACMSM...` for Specialist Mathematics. The glossaries are references only.

## 3. Source coverage

Make a short table for each assigned unit:

```text
source_code | decision | note
ACMMM...    | include  |
ACMMM...    | exclude  | short reason
```

`exclude` when the content is subjective, technology-dependent, proof-only, diagram-dependent, or cannot produce an exact answer.

## 4. Atoms

An atom is one reusable mathematical fact, rule, formula, constraint, or procedure, with one source code.

```json
{"id":"trig.period.tan_linear","statement":"The fundamental period of tan(b*x+c) is pi/abs(b), for b != 0.","source":"ACMMM038"}
```

Record every valid atom from your unit's included codes in `atoms.jsonl`. **Not every atom needs a template.** Only atoms you build on go into the benchmark; the rest stay in the file as inventory.

Name ids in the same style as the example pack (`func.*`, `trig.*`, `prob.*`) so the banks merge cleanly at the end.

- One statement per atom. Numerical instances of the same rule are examples, not new atoms.
- Keep two rules separate if they can be known independently.
- Merge two atoms that state the same rule in different words.

## 5. Atomic templates

One template per atom you build on. Add a second only if it tests a different direction or representation.

```json
{"id":"angle_deg_rad","atom":"trig.degree_radian_conversion",
 "template":"Convert {deg} degrees to radians.",
 "vars":{"deg":{"type":"choice","values":[15,30,45,60,90,120,180]}},
 "solver":"angle_deg_rad"}
```

```text
id        unique template ID
atom      atom ID
template  question text
vars      independently sampled variables
cases     fixed valid combinations, when needed
solver    matching function name
```

A good atomic template tests its atom, has one exact answer, excludes invalid values, reads like a normal question, and can produce enough distinct instances. Do not put answers, splits, traces, or difficulty labels in the record.

## 6. Variables and formatting

Constraints go in the template data, not in `generate.py`.

```json
"vars":{"b":{"type":"int","min":-12,"max":12,"exclude":[0]},
        "c":{"type":"int","min":-6,"max":6}}
```

Use `cases` when values must stay coupled.

Questions must read naturally: `2x-3`, not `2x+-3`, `1x+0` or `+0`. `generate.py` provides `term()`, `linfac()` and `shift()`; call them from `derive`.

## 7. Solvers

Every template names an exact solver function.

```python
def angle_deg_rad(deg):
    return pf(deg, 180)
```

- same name as the template's `solver` field;
- takes the sampled variables it needs;
- returns the exact answer as a string, never a float;
- rejects invalid parameter combinations rather than changing the question.

## 8. Strict composite templates

### 8.1 Finding a composite

**Start from a question, not from atoms.** Take a multi-step problem from your unit's textbook exercises, past papers, or the standard problem types you already know, and adapt it. Solve it, see which atoms it uses, and check it against 8.2. Most of the work is choosing well and adapting, not inventing.

A question built by bolting atoms together usually reads like it. `Express C(n,0) + C(n,n) + C(n,1) as a fraction of C(n,r)` chains three atoms correctly and no exam would ever ask it; it fails test 9.

**When nothing comes to mind,** or when you need a specific depth for section 9, work from the atoms instead. Write down what each atom in your unit needs and what it gives:

```text
func.hyperbola.vertical_asymptote   needs  a/(x−b)       gives  an x-value
func.quad_general.axis              needs  an axis, a    gives  b
func.notation.evaluate              needs  f and an x    gives  a number
```

Two atoms compose when one gives what the other needs. Keep going while something needs what the last one gave:

```text
asymptote gives x = p   ->   axis rule turns p into b   ->   evaluate the quadratic at p
```

That run is the spine of `asymptote_vertex_y`. Two atoms is the minimum: the deeper rows in section 9 are this same move continued. If neither atom needs what the other gives, only arithmetic joins them and the composite fails test 4.

Either way, the rest is the same.

**Step 1. Write the smallest question that needs the whole run.** Prefer a chain, where each step feeds the next, over a merge, where the steps are joined only at the end.

Patterns that work, each naming a template in this pack you can read:

| Pattern | Example |
|---|---|
| A property of one object becomes a parameter of another | `asymptote_vertex_y` |
| Test a condition, then act on the result | `cubic_factor_quotient` |
| Recover a parameter from a final or expanded form | `repeated_root_third` |
| Rewrite with an identity, then evaluate the simpler thing | `combination_sum_adjacent` |
| Transform an object, then evaluate or invert it | `transform_reverse_find_original` |
| Two rules each give part of one answer | `binom_specific_term_value` |
| Two constructions compared | `cubic_compare_forms` |

**Step 2. Solve it by hand.**

**Step 3. Write two records.** The question in `composite.jsonl`:

```json
{"id":"asymptote_vertex_y",
 "template":"The hyperbola y = {a_val}/(x−{b_val}){d_term} has vertical asymptote x = p and horizontal asymptote y = q. The quadratic y = {a_quad}x² + bx + q has axis of symmetry x = p. Find the y-coordinate of its vertex.",
 "vars":{"a_val":{"type":"int","min":1,"max":9},
         "b_val":{"type":"int","min":1,"max":6},
         "d_val":{"type":"int","min":-4,"max":4,"exclude":[0]},
         "a_quad":{"type":"int","min":2,"max":3}},
 "derive":{"d_term":"term(d_val)"},
 "solver":"asymptote_vertex_y"}
```

One step per atom application, in `graphs.jsonl`:

```json
{"id":"asymptote_vertex_y","nodes":[
  {"node_id":"n1","atom_id":"func.hyperbola.vertical_asymptote","expr":"b_val"},
  {"node_id":"n2","atom_id":"func.hyperbola.horizontal_asymptote","expr":"d_val"},
  {"node_id":"n3","atom_id":"func.quad_general.axis","expr":"-2 * a_quad * n1"},
  {"node_id":"n4","atom_id":"func.notation.evaluate","expr":"str(a_quad*n1**2 + n3*n1 + n2)"}]}
```

A step names earlier steps by `node_id`, so `n3` reads `n1` and `n4` reads all three. Write only `node_id`, `atom_id` and `expr`; `annotate_graphs.py` fills in the rest.

`d_val` is excluded from 0 so the hyperbola always shows a real horizontal asymptote, and `term()` prints it as `− 3` rather than `+ -3`. Couple values through `derive`, `constraints` or `cases`; saying it in the question text does not constrain generation.

**Step 4. Add the solver** to `solver.py`, under the name the template's `solver` field gives.

**Step 5. Run `python3 check.py <id>`.**

### 8.2 Composite acceptance tests

A composite is accepted only when all of the following are true.

**Structure**

1. **Connected and acyclic**, with every step on a path to the final answer.
2. **Every step computes something.** Reading a value off a form counts: `y = a/(x−4)` has asymptote `x = 4`. Copying a number the question states outright does not, and neither does repeating or reformatting an earlier result.
3. **Depth at least two.** Ignoring steps that only copy from the question, the longest chain of steps must be two or more.
4. **At least two different atoms.** Plain arithmetic — adding, multiplying, forming a fraction — is not an atom. Mark those steps `"atom_id":"arithmetic"`; they do not count toward the two.
5. **Every step is needed.** Removing one leaves the solution incomplete.

**Labels**

6. **Label what the step does,** not what the problem is about. A step that computes a vertex is not labelled *y-intercept*. If no atom fits and the step is not arithmetic, the curriculum is missing an atom — report it rather than choosing the nearest one.
7. **Every atom you use needs an atomic template.** Validation fails if one is missing.

**The question**

8. **One question, one answer.** Do not ask for two things and return one, and do not bundle independent `(a), (b), (c)` parts.
9. **Naturalness:** a real question, not a concatenation of atoms.

**Generation**

10. **No no-op draws.** Exclude values that make a step do nothing: dilation by factor 1, shift by 0 units, a target of 1.
11. **The final answer must vary.** Sample 200 instances and reject if one answer covers more than 60%. A step whose own output never changes is fine when its atom is a constant fact such as `C(n,0) = 1`.

### 8.3 Size and graph representation

Composite size is the number of steps, not the number of subquestions and not the number of distinct atoms. One atom applied twice is two steps.

Depth is the longest chain of steps, not the step count. A four-step graph in which three steps feed one final step has depth two.

Every intermediate step must produce a single value: an int, a string, or a `Fraction`, never a list, tuple or bool. Only the final step may return several parts.

### 8.4 Instance support

A standard template should support at least 128 distinct valid question-answer instances. The validation script should attempt 200 generations and confirm at least 128 unique questions.

A template with genuinely finite support can be enumerated exhaustively instead, but flag it to the lead; it does not count toward the target unless approved.

## 9. Composite size

Your accepted-composite target:

| Longest chain of steps | Accepted templates |
|---:|---:|
| 2 | 20 |
| 3 | 16 |
| 4 | 12 |
| 5 | 7 |
| 6 | 4 |
| **Total** | **59** |

The row is set by depth, not step count: six steps merging into one final node is depth 2 and belongs in the first row. `check.py` prints the depth.

Expect to write more than 59 and discard some; the time in section 14 allows for that. Allow extra time for the deep rows, and do not pad a problem with algebra to raise its step count.

## 10. Coverage and reuse

Composites must spread across your unit, not cluster on the few atoms that chain
most easily. Run `python3 coverage.py`:

- at least 70% of the atoms you wrote a template for appear in some composite;
- every atom you use appears in at least two composites;
- no single atom appears in more than a quarter of them.

The last one is the trap. Atoms like "evaluate f at a point" fit into almost any
chain, so they accumulate while whole topics get none. Check the list of atoms
with a template but no composite and work from it.

Also, by hand:

- every atom you use should pair with at least two different partner atoms;
- reuse at least 12 atom pairs across structurally different composites.

Do not paraphrase the same skeleton to raise the counts.

## 11. Exclusions

Do not build templates that need:

- subjective judgement;
- open-ended modelling choices;
- technology as the only way to get the answer;
- a graph drawing as the final output;
- long proof writing;
- diagram-dependent reasoning;
- answers that cannot be checked exactly;
- several independent questions presented as one composite;
- a tiny finite set of repeated cases.

## 12. Validation and QA

```bash
python3 annotate_graphs.py     # after editing graphs.jsonl
python3 check.py <id>          # one composite, against the tests in 8.2
python3 validate.py            # everything
```

`check.py` covers tests 1, 2, 3, 4, 7, 10, 11, 12 and 13. Tests 5, 6, 8 and 9 are judgement.

Then read:

- three generated outputs per atomic template;
- five per composite;
- every boundary case, such as undefined values or zero denominators.

Everything must pass before you submit.

## 13. Cross-review

Review one batch from another annotator:

- 15 atom statements with their source codes;
- 10 atomic templates with three generated cases each;
- about 30 composites with their graphs, solvers, and three generated cases each.

Mark each `correct`, `incorrect` or `uncertain`, with a short note for the last two. The lead resolves uncertain cases and reviews every composite with five or more steps.

## 14. Time

| Stage | Time |
|---|---:|
| Source coverage | 4 hours |
| Atom bank | 2 hours |
| Atomic templates and solvers | 8 hours |
| Composite planning | 6 hours |
| Composite templates and solvers | 40 hours |
| Generation and manual QA | 5 hours |
| Cross-review and cleanup | 7 hours |
| **Total** | **approximately 72 hours** |

## 15. Deliverable files

```text
coverage_<unit>.tsv
atoms.jsonl
templates.jsonl                         # atomic templates
composite.jsonl                         # composite questions
graphs.jsonl                            # composite steps
solver.py
generate.py
reviews/<annotator_id>.jsonl
```
