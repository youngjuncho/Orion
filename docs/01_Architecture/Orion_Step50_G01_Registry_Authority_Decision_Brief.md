# Orion Step 50 — G-01 Registry Domain and Authority Decision Brief

**Status:** Decision brief only; no authority selected and no production approval granted  
**Date:** 2026-10-14  
**Decision gate:** G-01 — Registry domain and authority  
**Related gates:** G-02, G-03, G-06, G-07, G-09, G-10; PCD-15 and PCD-16

## 1. Purpose and decision boundary

G-01 must establish the exact registry domain, authoritative issuer identity, ownership, and authority to publish or revoke records. This brief lays out the decision that must be made and the viable operating models. It does not select an option, name an issuer, approve a key, close a gate, or authorize Moon/ADM, Runtime, or Supernova integration.

The Step 50 Production Approval Gates document records D-060 as `DEFERRED — BLOCKING`: no registry domain or issuer is selected, and the gate remains blocking rather than waived. Reopen G-01 when a concrete consumer requirement and accountable issuer/operational owner are identified; until then, no production integration is authorized.

## 2. Evidence already in the repository

- `Orion_Step50_Production_Approval_Gates.md` defines G-01 as requiring the exact registry type, issuer identity, ownership, and publish/revoke authority, supported by an approved domain contract and issuer ownership evidence.
- `Moon_ADM_Provider_Contract_Decision_Register.md` keeps PCD-15 open and requires the signal guard to block while authoritative governance binding is unimplemented.
- `Supernova_Approved_Company_Registry_Contract_Proposal.md` describes a possible Supernova approved-company registry, but labels it a proposal and explicitly does not select an authority or key policy.
- `Orion_Step50_Stateless_Data_Path_Audit.md` reports that the SQLite acceptance prototype is not wired into an active Runtime/framework call site and does not establish a current product need for durable registry acceptance.
- D-055 approves Moon's SGOV comparison methodology (PCD-13/PCD-14); it does not approve a governance issuer, signing policy, or runtime integration.

These documents establish implementation options and boundaries, not an approved issuer or registry domain.

## 3. Decisions required from the project owner

The G-01 closure record must answer each item explicitly:

1. **Registry domain:** What exact decision state is being governed? Examples include a Moon/ADM signal-eligibility decision, a Supernova approved-company state, or another specifically named governance domain. Do not combine domains merely because they share an envelope format.
2. **Issuer identity:** What stable, non-ambiguous identifier names the issuer? A file path, hostname, repository name, or display label is not by itself proof of authority.
3. **Issuer owner:** Which accountable role or organization owns that identity and is responsible for its lifecycle?
4. **Publish authority:** Which role(s) may create, approve, and supersede records? Are author and approver the same principal or separate principals?
5. **Revoke authority:** Who can revoke or suspend a record or issuer, and how does a consumer learn about that revocation?
6. **Scope boundary:** Which exact framework, registry type, environment, and decision scope may this issuer govern? What is explicitly out of scope?
7. **Evidence and audit:** What immutable decision reference, approval evidence, and audit history must accompany each published state?
8. **Operational responsibility:** Who responds to mistaken approval, compromised issuer credentials, unavailable publication infrastructure, and disputed records?

G-01 can name the owner and domain while leaving cryptographic details to G-03, but it must not imply that the issuer is cryptographically trusted until G-03 is closed.

## 4. Operating models for consideration

These are alternatives for review, not recommendations already approved.

| Model | Description | Advantages | Costs and risks | Evidence needed |
|---|---|---|---|---|
| A. Project-owner-controlled registry | The project owner is the accountable authority; a designated, access-controlled repository or release process publishes versioned decisions. | Minimal new infrastructure; decisions and code changes can be reviewed together; easy to audit in a small project. | Repository write access can become an overly broad trust boundary; author/approver separation and key custody still need explicit policy; repository history alone is not cryptographic authentication. | Named owner and delegates; branch/release permissions; approval workflow; revocation and incident process; immutable/versioned decision references. |
| B. Dedicated governance service | A separately operated service issues signed snapshots and maintains issuer/key lifecycle and revocation state. | Clear separation of duties; central policy enforcement; can serve multiple consumers consistently. | More operational complexity, availability dependencies, deployment and backup obligations; service compromise has broad impact unless scope is tightly limited. | Service owner/SLO; identity and access model; audit retention; threat model; key custody; revocation API/distribution; recovery tests. |
| C. External organizational authority | A named organization or third party owns the registry and publishes decisions under a documented contract. | May fit an existing corporate governance process and independent ownership. | External dependency and contract/process constraints; may be unnecessary for a private research project; access, availability, and change-control responsibilities can be unclear. | Written authorization; named accountable contacts; exact domain/scope; publication and revocation SLA; incident escalation; rights to consume the records. |
| D. No authoritative registry for current MVP | Keep the acceptance prototype isolated and do not bind it to Moon/ADM until a concrete requirement and owner exist. | Avoids inventing a trust model; aligns with the current stateless-path audit; no accidental production authority. | Does not enable authoritative governance binding; PCD-15/PCD-16 and affected production gates remain blocked. | Explicitly record deferred decision, rationale, review trigger/date, and confirmation that fail-closed behavior and inactive strategies remain in place. |

## 5. Evaluation criteria

Evaluate each candidate against the following, without treating a high score as automatic approval:

- accountable human/organizational ownership;
- separation between proposing, approving, publishing, and revoking decisions;
- narrow scope and blast-radius control;
- ability to prove record provenance and detect tampering;
- reliable and timely revocation propagation;
- auditability and incident response;
- recovery and continuity obligations proportional to actual product need;
- operational complexity justified by a concrete consumer requirement.

A registry's storage location does not establish its authority. A valid digest does not establish authenticity. A signature establishes authenticity only when the concrete verifier, key-to-issuer binding, key lifecycle, and permitted scope have been reviewed and approved.

## 6. Dependency order after G-01

1. **G-01:** Approve domain, issuer identity/ownership, publish/revoke powers, and scope.
2. **G-02:** Freeze the versioned payload schema, canonical bytes, exact scope keys, and unknown-field behavior.
3. **G-03:** Select and review the signature scheme, trusted-key source, key rotation/revocation, and compromise response. Implement concrete verifier tests with known-good and known-bad vectors.
4. **G-04/G-05:** Approve freshness/replay and durable anti-rollback/recovery policy.
5. **G-06/G-07/G-08:** Prove acceptance orchestration, consumer idempotency, concurrency, and operational behavior.
6. **G-09/G-10:** Approve one exact consumer and its operational owners.
7. **PCD-15/PCD-16:** Only then design and test the authoritative binding to Moon/ADM, including missing, revoked, stale, wrong-scope, invalid-signature, rollback, and persistence-failure cases.

Closing G-01 alone does not close any downstream gate and does not authorize runtime wiring or strategy activation.

## 7. Required decision record template

Complete this template only after the project owner makes the decision:

- **Outcome:** Approved / Rejected / Deferred
- **Registry domain and exact `registry_type`:**
- **Authoritative issuer identifier:**
- **Accountable owner/role:**
- **Authorized publishers/approvers:**
- **Authorized revoker and revocation propagation mechanism:**
- **Permitted scope and explicit exclusions:**
- **Decision evidence and immutable references:**
- **Audit retention and incident owner:**
- **Dependencies and downstream gates still open:**
- **Residual risks / waiver scope (if any):**
- **Decision owner and approval date:**
- **Review trigger/date:**

If any required item is unknown, record G-01 as `Deferred — BLOCKING`; do not infer approval from silence or from an implemented prototype.

## 8. Current safe disposition

Until G-01 is explicitly decided and its evidence is linked from the authoritative governance record:

- retain G-01 as `DEFERRED — BLOCKING` under D-060; this is not a waiver or approval;
- retain G-03 and the other unresolved Step 50 gates as open;
- retain PCD-15/PCD-16 as open;
- keep `config/moon.yaml` at `active_strategies: []`;
- keep `authoritative_governance_binding_not_implemented` as a blocking reason;
- do not connect the acceptance prototype to Moon/ADM or infer production authority from fixture tests.
