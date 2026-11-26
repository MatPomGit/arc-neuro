# Ethics, safety, privacy and regulatory considerations

## 1. Scope

ARC-ADHD is intended for research with children, a population requiring heightened safeguards. The research prototype must not be presented as a proven treatment.

## 2. Clinical positioning

The intervention is designed as an adjunct to established care.

It should not:

- diagnose ADHD;
- recommend starting, stopping or changing medication;
- replace psychological, psychiatric, pediatric or school-based care;
- classify a child's emotions as pathological;
- claim therapeutic efficacy before adequate clinical evidence exists.

Any medication changes during a trial must be handled by the child's treating clinician and documented as a study variable.

## 3. Distress and frustration safeguards

Because controlled challenge is part of the mechanism, the protocol must distinguish useful difficulty from distress.

Required safeguards:

- bounded difficulty;
- automatic reduction after repeated failure;
- immediate pause control;
- no loss of earned progress for pausing;
- age-appropriate supportive feedback;
- clear session termination;
- caregiver stop option;
- adverse-event reporting pathway.

The game must never require a child to remain in an aversive state to preserve rewards.

## 4. Reward-system safety

Prohibited for the research build:

- loot boxes;
- paid random rewards;
- advertisements;
- in-app purchases;
- social-pressure streaks;
- public leaderboards;
- deceptive scarcity;
- endless play mechanics.

Reward schedules should support mastery, persistence and recovery rather than compulsive use.

## 5. Child assent and caregiver permission

Research participation requires a procedure approved for the actual legal and ethics classification of the study.

At minimum, the ARC-ADHD programme prepares:

- parent/legal-representative information and permission material;
- age-appropriate child assent;
- clear explanation that participation is voluntary;
- an operational child pause/stop/withdrawal pathway;
- separate information and choices for optional companion modules where required.

The child-facing explanation should use short, literal, age-appropriate language and should verify understanding rather than treat a signature as sufficient evidence of assent.

Research-participation permission/assent and the GDPR legal basis for personal-data processing are separate questions. The controller and data-protection officer must document the actual Article 6 basis and, where relevant, Article 9 condition rather than automatically treating the research-participation form as GDPR consent.

Working templates are maintained in `docs/ethics/`.

## 6. Data minimization

Collect only variables with a defined scientific purpose.

Avoid collecting:

- real names in telemetry;
- exact location;
- contact lists;
- microphone or camera data unless separately justified and approved;
- advertising identifiers;
- unrelated device data.

Use pseudonymous study identifiers.

## 7. Privacy architecture

Preferred research architecture:

- local preprocessing where possible;
- encrypted transport;
- separate identity and research-data stores;
- role-based access;
- documented retention schedule;
- auditable exports;
- deletion/withdrawal workflow consistent with the study protocol and applicable law.

ARC-ADHD project policy requires a documented DPIA before child-participant data collection. This is a conservative governance gate because the study concerns children, health-related information, behavioral telemetry and adaptive digital processing. The final controller/DPO assessment must still document the specific Article 35 rationale for the frozen processing operations.

The working DPIA and data-inventory templates are maintained in `docs/ethics/dpia_template.md` and `docs/ethics/data_inventory_template.md`.

## 8. European regulatory context

Under Regulation (EU) 2017/745, software can qualify as a medical device when the manufacturer gives it a specific medical intended purpose. The June 2025 revision of MDCG 2019-11 provides current EU guidance on qualification and classification of medical-device software and explicitly covers apps regardless of whether they run on a phone, cloud service or another platform.

Therefore:

- a research prototype should use precise non-commercial claims;
- the intended purpose must be frozen before regulatory classification;
- a future claim that ARC-ADHD treats ADHD or provides therapeutic decisions requires a formal MDR qualification and classification analysis;
- Rule 11 and other applicable rules must be assessed against the final intended purpose;
- regulatory classification should not be inferred merely from the word "app" or "game".

This repository does not assign a final MDR class.

## 9. GDPR context

The project should follow GDPR principles including:

- lawfulness, fairness and transparency;
- purpose limitation;
- data minimization;
- accuracy;
- storage limitation;
- integrity and confidentiality;
- accountability.

Article 8 of GDPR contains specific requirements for consent in relation to information-society services offered directly to children, with Member States allowed to set a threshold between 13 and 16 years. The research team must verify the national legal basis applicable to the deployed study rather than relying on a generic age threshold.

For scientific research involving health data, legal basis, special-category processing conditions, ethics approval/determination and institutional data-governance requirements must be established before recruitment.

The programme must also keep child-friendly transparency separate from adult/legal information. The 2026 EDPB scientific-research guidance should be checked for final status at protocol lock rather than cited as final merely because a consultation version exists.


[Continue to part 2](ethics_safety_regulatory-part-2.md)
