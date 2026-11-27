# M04: ethics and data-protection preparation

Status: draft for institutional review; no approval, exemption, enrollment or data collection claimed. Supplements `docs/human_research_governance.md`. This human protocol is distinct from synthetic M02 and psychometric M03.

## Scientific justification and proposed population

The M04 bridge would evaluate baseline propensity-to-behavior prediction and measurement limits in adults describing a romantic relationship. Its goal is not diagnosis, therapy or optimization of a partner's behavior. Consent and eligibility are individual; partner participation is optional unless a separately approved dyadic design requires it. Minimum age is proposed as 18. Exact relationship criteria, language requirements and eligibility must be decided before recruitment. Exclusion should follow justified safety/accessibility requirements rather than inferred attachment categories.

The procedure is observational: no induced rejection/conflict, deception, partner-withholding manipulation or instruction to provoke intimacy. Participants report naturally occurring states and actions. No individual controller, disorganization or relationship-quality verdict is returned. A null or ambiguous finding will be reported rather than concealed.

## Risk and mitigation

| Foreseeable risk | Proposed mitigation | Precollection verification |
|---|---|---|
| Emotional discomfort / rumination | Optional questions, pause/stop, neutral wording, no demand for distressing narratives | Cognitive pilot; trained contact and approved response procedure |
| Partner discovers sensitive responses | Private accounts, no shared dashboards, neutral notifications without relational content | Test on locked screens and shared-phone scenarios |
| Coercion by partner or lecturer | Independent individual consent; no grades/employment effects; recruitment outside assessment relationships | Recruitment script and independent contact |
| Prompt burden / distraction | Adjustable safe waking windows, no responding while driving, skip without reminders that disclose participation | Phone tests and empirical burden estimates |
| Misinterpretation as diagnosis | No individual mechanistic labels; explain experimental measurement | Information sheet and debriefing |
| Reidentification through temporal/dyadic data | Separated identifiers, restricted access, aggregate public outputs | Data-flow review and release review |

Do not promise immediate monitoring of questionnaire responses. Before use, specify whether any safety review exists, its hours and response time, and the contact responsible for unsolicited disclosures. If someone reports distress, offer stopping and a private contact; never contact their partner without authorization. Explain any applicable confidentiality limits, particularly immediate safety threats, through an institution-approved procedure. In immediate danger, the participant information refers to emergency help (112), not to the research survey. Support service details must be verified before inserting them.

## Consent, privacy and data flow

Consent to participation is distinct from the legal basis for data processing. The institution/data controller must determine the applicable Article 6 basis and, if special-category data are collected, the relevant Article 9 condition; do not assume a research-purpose label or a checkbox resolves this. Provide finalized Article 13 information before collection. Pseudonymized records remain personal data where linkage is possible. Do not describe them as anonymous.

Proposed separation: contact/consent records and withdrawal lookup in an access-restricted identity store; pseudonymous questionnaire records in a separate approved research store; optional couple linkage in a separate key table; analysts receive only the minimum required pseudonymous extract. Prefer age bands and coarse context variables; omit names, partner identifiers and open narratives from analysis exports. Necessary technical logs, recipients/processors, storage region, backups and any international transfers must be disclosed and approved before selecting a platform.

Access roles, encryption, authenticated access, backup restoration and deletion propagation are operational requirements to test, not assumed features. No participant records, completed consent forms or identifying quotes may be committed to Git, CI artifacts, Pages or uploaded to general AI services. Public reproducibility materials should prioritize code, schemas, synthetic fixtures and safe aggregates. Participant-level sharing requires a separate, documented compatibility and reidentification review.

Retention is unresolved: select justified periods and triggering dates separately for contact lookup, consent, research records and backups. Record destruction/irreversible anonymization procedures and any institution-required archival exceptions. Do not invent a five- or ten-year policy. Evaluate whether a data-protection impact assessment is required with the controller/DPO; its completion is not claimed.

Withdrawal stops future prompts immediately after processing the request. The final notice must state how to request removal of linkable research records, when linking keys are destroyed and what cannot be retrieved after irreversible anonymization or incorporation in published aggregates. Rights and any lawful limits must match the selected legal bases. One person's withdrawal must not reveal their responses to the partner; freeze couple-link and incomplete-dyad analysis rules beforehand.

## Approval dossier and reporting

Prepare: final protocol and analysis plan; recruitment/eligibility scripts; full item versions and permission evidence; information/consent/privacy notice; distress and confidentiality procedure; compensation details; data-flow/access/retention plan; platform and backup evidence; preregistration/freeze and deviation process. Recruitment remains blocked by B01–B09 in `README.md`.

Manuscript reporting must give the institution, decision identifier/date and scope only after verification, plus consent procedure and data-access statement. If a documented institutional determination exempts a synthetic-only study, report that exact determination; do not claim it covers later human collection. Any reused H1 data require an explicit secondary-use compatibility/ethics check and their actual observational status, not new enrollment.

Legal source verified 2026-10-07: Regulation (EU) 2016/679, Articles 5, 6, 9, 13 and 89: https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng. These provisions inform the dossier; this draft does not make institutional legal determinations.

M03 item-development/confirmation approval does not cover this study. Freeze the M04 scale version, ecological schedule, main incremental endpoint and any optional partner module before submission. No scale re-estimation on final M04 outcomes; no H1/H2/H3 claim is duplicated as the primary bridge result.
