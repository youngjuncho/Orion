# Orion Blocker Registry

Date: 2026-09-06

이 문서는 현재 작업을 막는 항목과 막지 않는 항목을 분리한 작업 기준표입니다.
막힘의 원인이 해결되면 해당 항목의 상태와 연결된 문서를 함께 갱신합니다.

## 상태 분류

- `D` Decision Required — 사용자의 투자·운영 결정 필요
- `S` Specification Required — 정책은 있으나 구현 계약이 부족함
- `C` Conflict — 문서 간 충돌 또는 기준 문서 불명확
- `I` Implementation — 문서가 충분하며 코드 작업 가능
- `F` Future — 현재 범위 밖

## 현재 Blocker

| ID | 구분 | 항목 | 막히는 작업 | 다음 조치 |
|---|---|---|---|---|
| B-001 | D/S | ADM 방어자산 선택 및 시장관측 입력 규칙 | ADM 시장데이터 계산 | DQ-ADM-001은 signal/execution 분리만 정함. 실제 방어 신호자산·관측일/freshness/missing-data 규칙은 미정 |
| B-002 | D | ADM VTI/VEU 및 방어자산 실행 매핑 | ADM 실행 allocation | 현재 승인 mapping에 VTI/VEU 없음. 구체 mapping 결정을 영구 문서에 기록 |
| B-003 | IMPLEMENT/F | consensus allocation, execution mapping, PortfolioTarget validation | PortfolioSnapshot 기반 rebalance workflow 및 ExecutionOrder는 MVP 범위 밖 | D-027 반영 완료; target 생성 이후 holdings/rebalance는 defer |
| B-004 | I/F | Moon MVP persistence scope | D-030 resolved the MVP boundary; implement in-memory EventStore/StateStore. Persistent storage, replay, and storage technology remain future scope. |
| B-005 | S | OrionEngine 공개 계약 | 전체 Runtime orchestration | 입력·출력·실패 격리 계약 확정 |
| B-006 | S | API 오류 계약 | CLI/API 외부 오류 변환 | 공개 예외와 오류 응답 형식 확정 |
| B-007 | D/S | Aurora 지표·공식·threshold | Aurora scoring/regime 엔진 | Approved indicator와 계산 규칙 결정 |
| B-008 | D/S | Supernova/Phoenix review 입력 경로 | 분석 점수 기반 report | 입력 형식·저장·최신 record 규칙 결정 |
| B-009 | S | Framework별 source/freshness 계약 | 데이터 collector | 프레임워크별 데이터 필드와 freshness 확정 |

## Blocker별 범위

### B-001~B-002 — ADM

현재 ADM은 사전 계산된 momentum 입력으로 선택하는 부분까지만 구현되어
있습니다. D-028에 따라 조정가격 기반 수익률 계산 helper까지 구현했으나,
시장 관측일/freshness/missing-data 계약과 방어자산 선택은 미정입니다.
실제 실행 매핑도 결정 전까지 연결하지 않습니다.

### B-003 — Moon Portfolio

D-027에서 Moon의 Portfolio domain contract를 결정했습니다.

Moon은 다음 개념을 서로 분리하여 관리합니다.

```text
StrategyResult
      ↓
ConsensusAllocation
      ↓
PortfolioTarget
```

현재 Portfolio 상태는 별도로:

```text
PortfolioSnapshot
```

으로 표현하며,

```text
PortfolioTarget + PortfolioSnapshot
            ↓
       RebalancePlan
```

으로 필요한 portfolio changes를 산출할 수 있습니다.

`ExecutionOrder`는 domain concept으로 정의하지만, 실제 broker order
generation 및 execution은 현재 Moon MVP 범위에 포함하지 않습니다.

따라서 현재 구현에서는 consensus allocation, execution mapping,
portfolio target 생성 및 validation까지 진행할 수 있습니다.

**Status:** Resolved by D-027

B-004~B-006 — Core Runtime/API

현재 in-memory EventStore, StateStore, RuntimeSession, API result contracts와
service registry까지가 구현 범위입니다.

D-030에 따라 persistent storage와 event replay는 현재 MVP 범위 밖이며,
구체적인 storage technology와 retention policy는 향후 별도의 Decision으로
결정합니다.

저장소·재생·외부 오류 변환은 각각의 계약이 확정된 후 진행합니다.


### B-007~B-009 — 데이터 의존 프레임워크

Aurora, Supernova, Phoenix의 scoring/leadership 규칙과 source contract가
닫히기 전에는 production 계산을 만들지 않습니다. 모델 검증, report 구조,
입력 계약 문서화, 단위 테스트 인프라는 계속 진행할 수 있습니다.

## 현재 진행 가능한 작업

- 공통 domain model의 strict validation과 immutable contract 보강
- CLI routing 및 실제 configuration validation
- Moon consensus/매핑/portfolio allocation의 순수 함수 테스트
- RuntimeSession, EventStore, StateStore, ServiceRegistry의 in-memory 동작 보강
- framework report 모델과 dashboard read-only 경계 테스트
- 문서의 구현 상태·Python mapping·cross-reference 정리

## 완료 또는 Blocker 아님

- Dashboard presentation-only 경계
- Moon equal-weight consensus
- unmapped execution asset 거부
- 등록 전략과 활성 전략 분리
- 기본 configuration loading/validation
- 현재 source tree와 package 문서 정합성

## 최근 진행 상태

| Blocker | 진행된 범위 | 남은 범위 |
|---|---|---|
| B-004~B-006 | RuntimeSession, ServiceRegistry, RuntimeContext, in-memory snapshots, `build_context()` 연결 | persistence, public OrionEngine, API error contract |
| B-009 | normalized observation/batch contracts와 runtime data handoff | source-specific fields, freshness, collectors |
| B-003 | consensus allocation, execution mapping, PortfolioTarget construction/validation | PortfolioSnapshot/rebalance/order는 MVP 범위 밖 |

현재 구현은 Runtime의 in-memory 조립 경로를 강화한 것이며, 아직 전체
OrionEngine orchestration을 구현한 것은 아닙니다.

## 사용자에게 요청할 결정 묶음

가장 먼저 `B-001`과 `B-002`를 함께 결정하면 ADM vertical slice를 진행할 수
있습니다. `B-003`은 D-027에서 이미 결정되었으므로 추가 사용자 결정은 필요하지
않으며, 정의된 MVP 범위의 Moon portfolio 구현을 진행할 수 있습니다.
Runtime persistence와 Aurora/Supernova/Phoenix 결정은 독립적으로 진행할 수
있습니다.

상세 질문은 `next_requests.md`에 기록합니다.
