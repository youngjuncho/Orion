# Review Follow-up Requests

Blocker 분류와 작업 순서는 `blocker_registry.md`를 먼저 참고합니다.

Date: 2026-09-06

이 문서는 `review_v1.zip` 검토 후, 다음 작업을 시작하기 전에 필요한
사용자 결정과 문서 보강 요청을 정리한 체크리스트입니다.

현재 `config/moon.yaml`의 `active_strategies`는 비어 있습니다. 아래 항목이
결정되기 전까지 미확정 투자 방법론은 코드에 구현하거나 활성화하지 않습니다.

---

## 1. ADM — 우선 결정 필요

대상 문서: `docs/03_Research/Moon/ADM/ADM_Orion.md`

- [ ] OI-001: 방어자산 결정 — SGOV / BIL / SHY 중 선택
- [x] OI-002: 12개월 수익률 계산 방식 결정 — D-028에서 adjusted-price total-return proxy로 확정
- [x] OI-003: 배당 처리 책임 결정 — D-028에서 data layer의 adjusted-price normalization으로 확정
  - 데이터 정규화 계층에서 처리
  - ADM 전략 내부에서 처리
- [ ] 평가일, `data_as_of`, 실행일, 결측 데이터 처리 규칙 확정

결정 후 보강할 문서:

- `ADM_Orion.md`
- `Orion_Data_Model.md`
- `Orion_Data_Pipeline.md`
- `Moon_Execution_Mapping.md`
- `Decision_Log.md`

---

## 2. ADM 실행 매핑

- [ ] VTI의 실행자산 결정
- [ ] VEU의 실행자산 결정
- [ ] 방어자산의 신호자산 → 실행자산 매핑 결정

동일 자산을 사용할 경우에도 `VTI → VTI`, `VEU → VEU`처럼 명시적인
매핑으로 기록합니다.

---

## 3. Moon Portfolio 계약

대상 문서: `docs/06_Implementation/Moon_Object_Model.md`

- [x] Current Holdings는 PortfolioSnapshot으로 분리 (D-027)
- [x] Target은 실행자산 mapping 후 PortfolioTarget으로 정의 (D-027)
- [x] RebalancePlan은 target과 snapshot 차이로 정의 (D-027); 상세 필드는 후속 범위
- [x] ExecutionOrder는 실제 주문 단위로 정의 (D-027); brokerage 실행은 MVP 제외
- [x] share count / 금액 / order type은 MVP에서 제외 (D-027)

---

## 4. Core Runtime 계약

- [ ] Persistence 기술 및 저장 위치 결정
- [ ] `OrionEngine` 공개 클래스 계약 확정
- [ ] API 오류 타입 및 외부 오류 응답 형식 확정
- [ ] Event / State replay와 영속화 범위 확정

관련 문서:

- `Orion_Engine.md`
- `Orion_Runtime.md`
- `Orion_API.md`
- `Orion_Service_Model.md`
- `Orion_State_Model.md`
- `Orion_Event_Model.md`

---

## 5. 후속 프레임워크 문서

### Aurora

- [ ] Approved indicator 목록
- [ ] 지표별 계산식·정규화·임계값
- [ ] 데이터 소스와 freshness 규칙

### Supernova

- [ ] analyst-scored 방식 여부 명시
- [ ] 리뷰 점수 입력 방식과 저장 형식
- [ ] 승인·watchlist 전환 규칙

### Phoenix

- [ ] analyst-scored 방식 여부 명시
- [ ] 리뷰 점수 입력 방식과 저장 형식
- [ ] category leadership를 config로 둘지 runtime state로 둘지 결정

---

## 다음 작업 요청 예시

다음 요청에서는 아래처럼 특정 묶음을 지정하면 됩니다.

```text
review/next_requests.md의 1번과 2번을 기준으로
ADM 의사결정 문서와 실행 매핑을 업데이트해줘.
코드 구현은 아직 하지 말고 Decision Log까지 정리해줘.
```
