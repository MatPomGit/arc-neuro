# Secondary longitudinal dataset screen for H1 and M04

Status: metadata-only feasibility screen; no participant records were requested,
downloaded, opened, or analysed.

Checked: 2026-10-18 against repository `main`
`0151ba7d16302ae54058eb6b75dd51bbbb17b20e`.

Migrated tracking issue: [#76](https://github.com/MatPomGit/arc-neuro/issues/76). Historical screen only; current terms and release metadata require fresh verification.

## Scope and decision rules

This is a bounded candidate screen, not a systematic review of every relationship
dataset. It applies the repository's low-cost evidence strategy: reuse existing data
only when their sampling, constructs, linkage, and access terms preserve the target
estimand. A large panel does not compensate for a missing momentary construct or an
incompatible interval.

For the current H1 comparable-lag question, a primary-use dataset would need all of
the following: repeated observations from eligible couples; separate perceived and
desired relational state; action after the state measurement; actual timestamps that
permit the prespecified same-day 1--4 hour lag; contact/context and missingness
information; and a defensible way to keep development and final evaluation separate.

For the current M04 primary bridge question, a dataset would need a defensible
baseline propensity score (or an explicitly preregistered established-trait fallback),
a later relational-action outcome, opportunity/context, timing and missingness, and
person/couple identifiers that allow whole people and dyads to remain in one split.
Similarity to attachment, satisfaction, stress, or relationship quality is not enough.

Verdicts:

- **GO**: the public documentation establishes the minimum design and construct fit;
  access and a preregistered analysis would still be required.
- **DEFER**: potentially useful for an adjacent or supplementary question, but the
  exact variables, linkage, release, or permissions must be verified first.
- **NO-GO**: the documented timing or construct structure cannot identify the stated
  primary question.

## Provenance-backed feasibility matrix

| Dataset and verified source | Population and timing | Relationship/dyad information established by inspected documentation | Access boundary | H1 primary | M04 primary | Permissible lower-cost use |
|---|---|---|---|---|---|---|
| **pairfam, release 14.2**. [GESIS overview](https://www.gesis.org/en/services/finding-and-accessing-data/selected-german-research-projects/pairfam), [data manual](https://www.pairfam.de/fileadmin/user_upload/redakteur/publis/Dokumentation/Manuals/Data_Manual_pairfam_Release_14.2.pdf), [scales manual](https://www.pairfam.de/fileadmin/user_upload/redakteur/publis/Dokumentation/Manuals/Scales_Manual_pairfam_Release_14.2.pdf) | German multi-actor panel, initially more than 12,000 anchors; annual collection over 14 waves. | Current partners are included. Partner files use corresponding partner variables; the scales manual documents repeated partnership constructs, including partnership instability. This establishes dyadic and longitudinal potential, not ARC construct equivalence. | Scientific Use File with a user contract. “Free of charge” does not mean unrestricted redistribution. Exact current contract and release citation must be accepted before data use. | **NO-GO**: annual spacing cannot recover the prespecified same-day 1--4 hour state-to-action lag; inspected documentation does not establish separate momentary perceived/desired closeness plus intervening actions. | **NO-GO** for the primary later-prompt endpoint. **DEFER** for an adjacent annual couple-level prediction or convergent benchmark after variable-level review. | Highest-priority metadata follow-up. Public codebooks can be screened for a preregistered, clearly adjacent annual relationship question without requesting new participants. |
| **Understanding Society main survey**. [data access guide](https://www.understandingsociety.ac.uk/documentation/mainstage/user-guides/main-survey-user-guide/data-access/), [linking household members](https://www.understandingsociety.ac.uk/documentation/mainstage/user-guides/main-survey-user-guide/linking-datafiles/), [main survey user guide](https://doc.ukdataservice.ac.uk/doc/6614/mrdoc/pdf/6614_main_survey_user_guide.pdf) | UK household panel; people are interviewed annually and can be linked within and across waves. | Whole-household coverage permits linkage of partners when both are respondents. Public documentation supports family/partnership content, but this screen did not verify ARC-equivalent momentary variables. | End User Licence, Special Licence, and Secure Data Access tiers differ. Only the least restrictive tier containing the prespecified variables may be used; no redistribution of licensed microdata. | **NO-GO**: annual measurement is incompatible with the H1 within-day lag and action-reference period. | **NO-GO** for the primary later-prompt endpoint. **DEFER** for an adjacent annual household/couple analysis after release-specific variable and licence checks. | Secondary robustness or external-context analysis only, with an independently stated estimand. It must not be described as a test of H1 or the M04 primary bridge. |
| **MIDUS National Study of Daily Experiences (NSDE)**. [official MIDUS project page](https://midus.wisc.edu/midus2/project2/), [public project README](https://midus-study.github.io/public-documentation/M1P2/M1_P2_README_20211209.pdf), [ICPSR MIDUS 3 daily-diary record](https://www.icpsr.umich.edu/web/NACDA/studies/38529/summary) | Daily telephone diary. MIDUS 1 participants completed up to eight consecutive daily interviews (mean 7.2); MIDUS 2 Project 2 contains 2,022 respondents. | Documentation establishes daily stress, affect, and broader psychosocial linkage. The inspected material does not establish romantic-partner dyads completing matched diaries, separate desired/perceived closeness, or actions measured after state within a day. Twin/sibling structure is not a substitute for romantic dyads. | Data are accessed through the official MIDUS/ICPSR route. Release-specific terms, account requirements, and citation must be checked before use; no data are copied into this repository. | **NO-GO**: one daily interview does not yield the prespecified 1--4 hour within-day sequence, and the required dyadic ARC variables are not documented. | **NO-GO** for the primary propensity-to-later-action endpoint. **DEFER** for methods work on daily missingness/stress reactivity if a separate question is justified. | Useful only as an adjacent daily-process benchmark. It cannot validate ARC, H1, or a relational-control propensity score. |

## Decision

No screened dataset receives GO for the current H1 or M04 primary estimand.
Therefore no existing panel should be forced into an apparently cheaper but invalid
substitute analysis. pairfam is the best next metadata-only candidate for a distinct,
supplementary annual dyadic question; Understanding Society is a second option if its
licence tier and variables are a better fit. MIDUS NSDE is intensive only at the daily
level and is not documented here as a matched romantic-dyad sequence.

This result does **not** authorize ESM recruitment. It only documents why these three
prominent secondary sources do not remove the need for momentary data if the original
H1 or M04 primary hypotheses are retained. All existing precollection, ethics,
instrument, burden, and sample-size gates remain in force.

## Authorized-data-only codebook

Populate release-specific variable names only from the official codebook after the
applicable agreement is accepted. Never infer names from article text or copy licensed
microdata into Git.

| Canonical field | Required meaning | Timing/linkage requirement | Current metadata status |
|---|---|---|---|
| `dataset_release` | Exact study and release/version | Constant for an analysis freeze | Known for pairfam 14.2; unresolved for any future UKHLS or MIDUS extraction |
| `person_id` | Pseudonymous respondent key | Stable across retained waves/days | Expected in all three; exact field intentionally not guessed |
| `dyad_id` | Couple key, with both members kept together | Stable over the analysed relationship spell | Potentially derivable for pairfam/UKHLS; not established for NSDE romantic couples |
| `observation_time` | Actual interview/prompt time, not wave label | Must support the target lag | Annual wave timing fails H1/M04 prompt timing; NSDE daily timing fails H1 1--4 hour timing |
| `perceived_state` | Current perceived closeness/bond | Measured before later action | Exact equivalent not established |
| `desired_state` | Current desired closeness/bond, separate from perceived state | Same source prompt as perceived state | Exact equivalent not established |
| `approach_action` | Approach action since the preceding prompt | Occurs after source state and before outcome | Exact equivalent not established |
| `distancing_action` | Distancing action since the preceding prompt | Kept separate from internal regulation | Exact equivalent not established |
| `contact_opportunity` | Whether meaningful partner contact/action opportunity occurred | Time-aligned with action window | Exact equivalent not established |
| `context_stressor` | Prespecified contextual stressor/impact | Time-aligned; no identifying narrative needed | Adjacent daily stress exists in NSDE; equivalence to H1 context not established |
| `missingness_status` | scheduled/delivered/opened/submitted or best available distinction | Must separate nonadministration, nonresponse, and technical failure | Requires release-specific documentation |
| `baseline_propensity` | Frozen M03 score or preregistered established-trait fallback | Measured before M04 outcome | Not available as the frozen M03 score in the screened sources |

## Staged extraction plan

1. **Metadata gate, no restricted data:** search public questionnaires and codebooks
   for the codebook meanings above. Record exact release, source URL, page/table,
   respondent (anchor/partner), waves, reference period, scale anchors, missing codes,
   and licence tier. Stop if perceived and desired state or temporal order is absent.
2. **Estimand gate:** write a separate supplementary question for any annual panel.
   Do not rename relationship satisfaction, support, strain, or instability as ARC
   discrepancy or action. Keep this question outside the frozen H1/M04 primary tests.
3. **Access gate:** obtain the required user agreement or institutional approval before
   download. Store restricted files only in the approved location; commit neither raw
   nor derived row-level data. Record the release checksum locally when permitted.
4. **Software gate:** implement import/validation against a schema and a fully
   synthetic fixture first. Validate unique keys, dyad membership, wave/time order,
   allowed missing codes, attrition, and relationship-spell changes before analysis.
5. **Analysis gate:** preregister or prospectively freeze the supplementary estimand,
   exclusions, missingness strategy, dependence model, split unit, multiplicity, and
   sensitivity analyses. Keep partners together and do not use a final split to select
   variables or lag definitions.
6. **Output gate:** export only disclosure-safe aggregates permitted by the licence,
   with denominators, uncertainty, provenance, and explicit “adjacent evidence”
   wording. A secondary-data association is not human validation of ARC.

## Cheapest scientifically justified next step

Complete a variable-level metadata crosswalk for **pairfam 14.2** from the public
questionnaires/codebooks. If it lacks a defensible prospective action outcome or
temporal order even for a distinct annual question, record NO-GO and stop before any
data application. This costs no participant burden and does not change a frozen
protocol.

