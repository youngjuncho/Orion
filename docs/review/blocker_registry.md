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
| B-001 | D/S | ADM 방어자산·총수익·배당 방식 | ADM 시장데이터 계산 | 사용자 결정 후 ADM 문서와 Decision Log 갱신 |
| B-002 | D | ADM VTI/VEU 및 방어자산 실행 매핑 | ADM 실행 allocation | 승인된 신호→실행 매핑 추가 |
| B-003 | S/D | Portfolio Target/Snapshot/RebalancePlan/ExecutionOrder 계약 | 포트폴리오 구성·주문 산출 | 수동 추천 목록인지 실제 주문인지 결정 |
| B-004 | D | Persistence 기술·저장 범위 | 이벤트·상태 replay와 영속화 | 저장 기술 및 보존 정책 결정 |
| B-005 | S | OrionEngine 공개 계약 | 전체 Runtime orchestration | 입력·출력·실패 격리 계약 확정 |
| B-006 | S | API 오류 계약 | CLI/API 외부 오류 변환 | 공개 예외와 오류 응답 형식 확정 |
| B-007 | D/S | Aurora 지표·공식·threshold | Aurora scoring/regime 엔진 | Approved indicator와 계산 규칙 결정 |
| B-008 | D/S | Supernova/Phoenix review 입력 경로 | 분석 점수 기반 report | 입력 형식·저장·최신 record 규칙 결정 |
| B-009 | S | Framework별 source/freshness 계약 | 데이터 collector | 프레임워크별 데이터 필드와 freshness 확정 |

## Blocker별 범위

### B-001~B-002 — ADM

현재 ADM은 사전 계산된 momentum 입력으로 선택하는 부분까지만 구현되어
있습니다. 방어자산 선택, total-return 계산, 배당 처리, 실제 실행 매핑은
결정 전까지 구현하지 않습니다.

### B-003 — Moon Portfolio

현재 consensus allocation과 실행 매핑 검증까지 진행할 수 있습니다. 현재
보유수량과 목표수량의 차이, 주문의 의미, broker 연동 여부가 결정되기 전에는
주문 생성이나 Portfolio 확장을 진행하지 않습니다.

### B-004~B-006 — Core Runtime/API

현재 in-memory EventStore, StateStore, RuntimeSession, API result contracts와
서비스 registry까지가 구현 범위입니다. 저장소·재생·외부 오류 변환은 계약
확정 후 진행합니다.

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
| B-003 | consensus allocation과 execution mapping validation | Portfolio target/snapshot/rebalance/order semantics |

현재 구현은 Runtime의 in-memory 조립 경로를 강화한 것이며, 아직 전체
OrionEngine orchestration을 구현한 것은 아닙니다.

## 사용자에게 요청할 결정 묶음

가장 먼저 `B-001`과 `B-002`를 함께 결정하면 ADM vertical slice를 진행할 수
있습니다. 이후 `B-003`을 결정하면 consensus allocation에서 Portfolio target과
rebalance plan으로 확장할 수 있습니다. Runtime persistence와 Aurora/
Supernova/Phoenix 결정은 독립적으로 진행할 수 있습니다.

상세 질문은 `next_requests.md`에 기록합니다.
