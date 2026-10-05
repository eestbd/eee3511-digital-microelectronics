# Part 2 실용적인 여유 개선

실험·수치 검증 정리 시각: 2026-10-05 13:15:26 KST. 최신 과제 PDF 50~57쪽과 공식 Q&A를 다시 읽고, 12개 후보의 구조·용량·READ·누설을 측정했다. 유망한 2개 후보는 64 ms 보존 후 재읽기로 비교했다. 사용자의 후속 지시에 따라 균형 후보 #19를 선택한 뒤 추가 탐색을 멈췄다. 실험과 수치 검증에 약 77분을 사용했고, 이어 문서와 전체 변경을 검토했다. 전역 최적해 탐색이나 제출 보고서 제작은 수행하지 않았다.

## 결론과 비교

**Part 2 소자의 필수 조건·구조·수치 검증은 로컬 모델에서 PASS다.** Cell retention은 Data 1이 제한하며, 미세 간격 추정치는 **95.198837 ms**다. Data 0는 128 ms까지 실제 통과했다. 기존 추정치 67.203479 ms보다 약 41.66% 증가했다. 64 ms Data 1 마진이 기준 60 mV를 넘는 여유는 0.418→약 3.56 mV로 늘었다.

| 항목 | 과제 기준 | 기존 #11 | 새 #19 기본 | 새 #19 미세 |
|---|---|---:|---:|---:|
| 초기 Data0 READ (mV) | ≥60 @0.5 ns | 127.319535 | 127.806239 | 127.806239 |
| 초기 Data1 READ (mV) | ≥60 @0.5 ns | 67.300905 | 69.463266 | 69.463266 |
| 64 ms Data0 READ (mV) | ≥60 | 117.214382 | 112.955710 | 113.056656 |
| 64 ms Data1 READ (mV) | ≥60 | 60.417968 | 63.557209 | 63.559235 |
| Data1/cell retention (ms) | ≥64 | 67.203479(미세) | 95.190207 | 95.198837 |
| Data0 retention (ms) | ≥64 | ≥72.597648 | ≥128 | ≥128 |
| CSTORE (fF) | ≤20 | 19.824 | 19.281938 | 19.281938 |
| Gate field (MV/cm) | ≤5 | 5.000 | 4.716981 | 4.716981 |
| Capacitor field (MV/cm) | ≤4 | 3.333333 | 2.500 | 2.500 |

- 기본/미세는 retention 최대ΔV=3/1.5 mV이며, 채점 READ는 둘 다10 ps다. 초기READ5 ps는 별도 민감도 검증으로만 사용했다.
- 기본 data1 실패 구간=94.929035 ~ 95.451378 ms, 미세 구간=94.937594 ~ 95.460080 ms. 실제 구간 양끝의 READ가60 mV 통과/실패를 구분한다. Midpoint는 유한 간격·모델에서의 추정값이며 수학적으로 정확한 시간이나 오차의 confidence interval이 아니다.
- 미세 구간 양끝 margin=60.030102 / 59.966779 mV. 기본/미세 estimate 차이=0.008630 ms(0.0091%). Data0 미세128 ms margin=109.821026 mV로data1 구간 상단보다 오래 유지됐다. Data0 자체 최대 retention은 미측정이다.

## 선택한 설계

| 변수 | 기존 | 새 추천 |
|---|---|---|
| Gate / Lg / W | W /0.3 µm/0.1 µm | 동일 |
| Gate SiO2 tox | 5 nm | **5.3 nm** |
| Source / drain 길이 | 각0.2 µm | 동일 |
| xj / tSi | 0.05/0.3 µm | 동일 |
| Background NA | 7e16 cm⁻³ | 동일 |
| Gate 아래 source-side / drain-side NA | 7e16/7e16 | **1e15/1e17 cm⁻³**, Lg의왼쪽/오른쪽 절반 |
| Source / drain ND | 1e19/1e19 | **1e20/1e19 cm⁻³** |
| p+ body tap | 추가acceptor1e19, 두께0.05 µm | 동일 |
| Doping decay x/y | 12.5/5 nm | 동일 |
| Capacitor | ZrO2, h0.96 µm/tdiel3 nm | **ZrO2, h1.245 µm/tdiel4 nm** |
| Pillar width / bottom clearance | 0.1/0.05 µm | 동일 |

Source 쪽의 낮은 채널 도핑과 높은 n+ 도핑으로 READ 성능을 높이고, drain 쪽의 높은 채널 도핑으로 누설을 억제하는 조합을 비교했다. 산화막 두께와 capacitor 치수도 함께 조정해 용량·전계 제한에서 여유를 얻었다. 최종 조합에는 여러 변수의 효과가 섞여 있으므로 각 변수의 효과를 모두 독립적으로 측정한 결과로 해석하지 않는다.

치수/농도/재료 범위는 실제 constructor 및 fresh 저장 구조로 확인했다. Lg는 고정값, source/drain 길이와tSi는 허용 최솟값, drain-side NA는 허용 상한값이다. 모든 설계 변수가 범위의 내부에 있는 것은 아니다. Gate·cap field와CSTORE의 필수 상한은 여유 있게 만족한다.

## 탐색 판단과 한계

- NA1e17·tox5.5 nm 단독 후보와sourceND1e21/drainND1e18 조합은 초기Data1 READ58.929/59.899/51.168 mV로 FAIL했다. 원시 결과와실패를 보존했다.
- TaN과source-side NA 저하만 적용하면 초기Data1 마진은 좋아지지만 누설이 커졌다. 초기누설만으로 retention을 판정하지 않았으며, 우선순위가 낮은 후보의 미측정 retention을 FAIL로 꾸미지 않는다.
- #10은64 ms Data1 65.280 mV로 #19보다 READ가 좋지만 C19.824 fF/Eox5 MV/cm가 상한에 가까웠다. #19는64 ms63.557 mV/C19.282 fF/Eox4.717 MV/cm의 균형 때문에 골랐다. #21의 저농도 구간 축소는초기READ63.182 mV로 떨어져 우선순위를 낮췄다.
- 최초 희망값은 초기 마진≥75 mV, 64 ms 마진≥65 mV, retention≥96 ms, CSTORE≤19 fF였다. 이후 조기 종료를 고려해 64 ms 마진≥64 mV를 참고했으나, 이 값들은 과제의 필수 기준이 아니다. 새 후보는 일부 희망값을 채우지 못했지만 과제의 60 mV·64 ms·20 fF 조건은 통과했다. 사용자가 극한 탐색을 원하지 않아 약 95.2 ms 보존 시간과 용량·전계 여유를 검증하고 마무리했다.
- 독립 mesh 민감도·조교 evaluator·제출용 통합 보고서/OK 화면 캡처는 미완료다. 조교 재실행 결과가 최종 채점 기준이다. 기존 Part1/HW1·source/physics·과거 결과·기존 root Part2 파일을 보존했고 commit/push·제출은 수행하지 않았다.

## 파일과 재현

- 새 추천 [설정](part2_robust.yaml), [학번 구조](results/part2_robust_search_20261005_115807/selected/part2_2022142233.devsim).
- 기존 `part2_final.yaml`과root `part2_2022142233.devsim`은 #11로 보존했다. 새 추천 파일은 위 경로다.
- [실험별 matrix](results/part2_robust_search_20261005_115807/results_matrix.csv), [최종 결과 JSON](results/part2_robust_search_20261005_115807/result_summary.json), [raw audit](results/part2_robust_search_20261005_115807/validation.json), [보호 검증](results/part2_robust_search_20261005_115807/preservation.json).
- [선택 구조 geometry/NetDoping](results/part2_robust_search_20261005_115807/selected_geometry/validation.json). 최종 구조 SHA256=376b392d2a81e9016f89c811f382a8f2d81e065dbeff9eef6072eab052753c11. 단일 device/physics 부재·naming·plate C·399 source/42 drain donor plateau·NetDoping 검증 PASS.
- 실제 실행은새 run의 `launch.py`로 `screen`, `endpoint1`, `verify0/1`, `fine0/1`을 호출했다. `verify_candidate.py`는 기존공식 cell READ/retention과직전검증된 continuation을 재사용한다. 각 process의 command/시간/exitcode와native log를 보존했다. 준비만 하고실행하지 않은 후보는matrix에서 `not_run`이다.

루트 PowerShell에서 PATH/PYTHONIOENCODING을 AGENTS대로 준비한 뒤, 최종 64 ms 재현은 다음 명령으로 수행한다. 이 설계는 비균일 도핑과 tap을 포함하므로 **반드시 저장 구조를 reload한다**. `part2.py`에서 구조를 새로 만드는 경로는 선택적 profile/tap을 생성하지 않는다.

```powershell
& .\.conda\python.exe -B .\project1\part2.py --config .\project1\part2_robust.yaml --reload-structure .\project1\results\part2_robust_search_20261005_115807\selected\part2_2022142233.devsim --output-dir .\project1\tmp\robust_replay
& .\.conda\python.exe -B .\project1\check_structure_file.py .\project1\results\part2_robust_search_20261005_115807\selected\part2_2022142233.devsim
```

`robust_replay`는새 빈디렉터리여야한다. 공식T398 K/VB−0.5 V·extended3종=true·ramp0.1 V·READ10 ps/0.5 ns를 유지했다. 이동도/ni/SRH/게이트식을 바꾸지 않았고 실제 native μn202.969896/μp107.387566 cm²/(V·s), ni=n1=p1=4.757304e12 cm⁻³를 대조했다.
