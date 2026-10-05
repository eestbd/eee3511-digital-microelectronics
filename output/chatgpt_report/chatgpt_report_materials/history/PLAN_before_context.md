# PLAN.md

현재 작업: Part 1·2 구현 완료와 보고서 외 제출 준비 확인.
상태: 완료. 과제 제출 페이지·최종 측정 근거·학번 파일·보고서 초안을 대조했다. 새 실험이나 소자 변경은 하지 않았다.

## Goal

Part 1·2 설계가 끝났는지, 보고서 작성 외에 필수 준비가 남았는지 실제 파일과 과제 요구사항으로 판단한다.

## Current State

- Part 1 최종 #10: 공식 모델·128비트·ramp0.1 V에서 동일 소자 8/8 PASS. 최종 fine metrics는 `project1/results/official_20261004_155839/part1/candidate_10/fine/metrics.json`이다.
- Part 1 학번 구조 `project1/part1_2022142233.devsim`은 실제 존재하며 측정 구조 SHA256=41c6f8f6ff5782c8ec3ecbc98d39bd264149ec076630f8bad0c9c98d6f06d07c와 같다. `results/submission_check_20261004_231707/validation.json`의 checker OK·singleton·physics 부재 검증이 있다.
- Part 2 새 추천 #19는 `project1/part2_robust.yaml`과 `project1/results/part2_robust_search_20261005_115807/selected/part2_2022142233.devsim`이다. 구조 SHA256=376b392d2a81e9016f89c811f382a8f2d81e065dbeff9eef6072eab052753c11. 최종 validation의 모든 필수 조건 로컬 PASS다.
- 새 셀 retention estimate95.198837 ms, Data1 64 ms 마진63.559235 mV, Data0는128 ms까지 PASS. CSTORE19.281938 fF/Eox4.716981/Ecap2.5 MV/cm. 기본·미세 결과 차이와 전류/전하 보존·fresh checker·NetDoping 검증을 통과했다.
- 루트 `project1/part2_2022142233.devsim`은 보존된 이전 #11이다. 새 #19 제출 파일과 혼동하지 않는다. Part1/HW1·기존 code/physics·결과는 변경하지 않았다.
- `output/pdf/part1_report_draft.pdf`는 7쪽 Part 1 초안이다. 학번 미확인·Part2 미완료라는 과거 문구가 남아 있으므로 최종 보고서로 그대로 제출하지 않는다. 두 소자의 실제 OK 화면 캡처는 미완료다.

## Requirements

- 최신 PDF와 공식 Q&A의 설계·제출 조건을 구분하고 로컬 PASS와 조교 채점 PASS를 구분한다.
- 이번 범위는 확인·문서 기록이다. 재최적화·실험·보고서 제작·소자 교체·제출 업로드는 수행하지 않는다.
- 과제 제출물은 약12쪽 PDF, 학번 이름의 두 .devsim, 두 실제 self-check OK 화면이다. 보고서에 지정된 Part-1-(a)~(c), Part-2-(a)~(d)를 포함한다.

## Assumptions

- 알려진 모델·수치 조건의 로컬 검증을 소자 설계 완료의 근거로 삼되 조교 evaluator 통과를 보장하지 않는다.
- 독립 mesh 연구와 Data0 자체 최대 retention 측정은 별도 필수 제출 항목이 아니다. 두 상태의64 ms 판정은 이미 검증했으므로 보고서 작성 전 필수 추가 탐색으로 편입하지 않는다.
- 오래된 audit 문서는 당시 상태의 기록이다. 당시 학번 파일 미완료·#11 최종이라는 내용은 후속 검증·#19 결과로 갱신된 현재 상태와 구분한다.

## Plan

- [x] 최근 PLAN/log와 기존 completion audit 확인.
- [x] PDF 제출 페이지의 실제 텍스트·화면, 공식 Q&A 대조.
- [x] Part1 fine 8항목·Part2 최종 validation·실제 세 구조 파일 hash 확인.
- [x] 현재 PDF 초안과 제출 요구를 비교해 남은 준비를 구체화.
- [x] 최종 문서 검토·UTF-8·diff 및 append-only log 확인.

## Validation

- 기존 로컬 pypdf 모듈 경로를 사용해 최신 PDF 실제57쪽과 7쪽 보고서의 첫 페이지를 직접 읽었고, 제출 페이지 렌더도 확인했다. 환경에 새 의존성을 설치하지 않았다.
- `.conda/python.exe -B`로 Part1 fine metrics 8개 status=PASS, Part2 `validation.json`의 passed/all_minimum_specs_pass=true, 학번 구조 SHA256 세 개를 확인했다.
- 실제 파일의 hash가 기존 fresh checker·측정 검증과 일치하므로 TCAD와 구조 checker를 반복하지 않았다. 구조 OK와 전기적 PASS를 구분했다.
- 문서 strict UTF-8·실제 한글·대체문자 부재, 이전 로그 byte prefix 보존, `git diff --check` 최종 확인 PASS.

## Progress / Discoveries

- 과제는 Part1과 Part2다. 슬라이드의 장 번호3~6은 별도 Part3/4가 아니다.
- Part1 학번 파일은 과거 audit 작성 후 생성·검증됐다. 새 Part2는 별도 selected 경로이므로 제출 묶음을 만들 때 그 파일을 선택해야 한다.
- 보고서에 Part1 물리·탐색·one-knob ablation, Part2 구조/CSTORE·양 상태 READ 곡선·탐색·최종 결과와 근거를 넣어야 한다. 결과 데이터와 이력은 준비됐고 최종 그림·곡선·표의 PDF 편집은 남았다.
- 단순히 보고서 글만 작성하면 끝나는 상태는 아니다. 두 실제 checker OK 화면 확보와 올바른 두 학번 파일의 제출 묶음 확인도 필요하다.

## Final Review

- 소자 구현·설계 및 필수 조건의 로컬 검증은 Part1/2 모두 완료됐다. 추가 최적화가 필수라고 판단할 근거는 없다.
- 최종 제출 준비는 미완료: 통합 보고서 PDF·두 실제 OK 화면·새 #19를 포함한 정확한 제출 파일 묶음. LearnUs 업로드는 사용자 작업이며 이번에는 수행하지 않았다.
- 조교 재실행·독립 mesh 검증은 미확인이다. 보고서 초안의 과거 상태 문구를 반드시 갱신해야 한다.
- 현재 확인 요청 완료. 다음 요청 전 실험·보고서 제작·파일 교체를 자동 진행하지 않는다.
