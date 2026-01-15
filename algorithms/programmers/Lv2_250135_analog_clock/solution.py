"""
Programmers Lv.2 250135 - 아날로그 시계

- 초침이 시침 또는 분침과 겹칠 때마다 알람
- 0시/12시 정각 (3침 동시 겹침)은 1회만 카운트
- 시작 시각 포함
"""

import math

# ======================================================
# ❌ 내가 처음에 작성했던 오답 코드
# ======================================================
"""
문제점 요약
1) solution() 함수가 없어 채점 실패
2) 누적 계산 함수 안에서 구간 계산을 수행 (함수 역할 혼합)
3) h1, m1, s1 같은 외부 변수를 함수 내부에서 참조
4) 0초 포함 여부 및 3침 동시 겹침 중복 처리 미흡
→ 일부 테스트에서 +2 오차 발생
"""

def wrong_count_alarms(h, m, s):
    total_seconds = h * 3600 + m * 60 + s

    # 초침이 시침 추월
    hour_count = math.floor(719 * total_seconds / 43200)

    # 초침이 분침 추월
    minute_count = math.floor(59 * total_seconds / 3600)

    total = hour_count + minute_count

    # 정각 예외 처리 (불완전)
    if (h == 0 or h == 12) and m == 0 and s == 0:
        total -= 1

    # ❌ 함수 내부에서 외부 변수 사용 (구조적 오류)
    if (h1 == 0 or h1 == 12) and m1 == 0 and s1 == 0:
        total += 1

    # ❌ 누적 함수 내부에서 구간 계산
    total = wrong_count_alarms(h2, m2, s2) - wrong_count_alarms(h1, m1, s1)

    return total


# ======================================================
# ✅ 정답 코드
# ======================================================

def count_until(h, m, s):
    """
    0:00:00부터 (h:m:s) 시각까지의 누적 알람 횟수
    """
    t = h * 3600 + m * 60 + s

    # 초침-분침 겹침 (0초 포함)
    minute_meet = math.floor(59 * t / 3600) + 1

    # 초침-시침 겹침 (0초 포함)
    hour_meet = math.floor(719 * t / 43200) + 1

    # 3침 동시 겹침(0시, 12시) 중복 제거
    triple = (t // 43200) + 1

    return minute_meet + hour_meet - triple


def event_at(h, m, s):
    """
    정확히 해당 시각에 알람 이벤트가 발생하면 1
    (분침/시침 중 하나라도 겹치면 1)
    """
    t = h * 3600 + m * 60 + s
    is_minute = (59 * t) % 3600 == 0
    is_hour = (719 * t) % 43200 == 0
    return 1 if (is_minute or is_hour) else 0


def solution(h1, m1, s1, h2, m2, s2):
    """
    [h1:m1:s1, h2:m2:s2] 구간 (시작 시각 포함)
    """
    return (
        count_until(h2, m2, s2)
        - count_until(h1, m1, s1)
        + event_at(h1, m1, s1)
    )
"""
Programmers Lv.2 250135 - 아날로그 시계
"""

import math

# ======================================================
# ❌ 오답 코드 (기록용)
# ======================================================

def wrong_count_alarms(h, m, s):
    total_seconds = h * 3600 + m * 60 + s

    hour_count = math.floor(719 * total_seconds / 43200)
    minute_count = math.floor(59 * total_seconds / 3600)

    total = hour_count + minute_count

    if (h == 0 or h == 12) and m == 0 and s == 0:
        total -= 1

    # ❌ 외부 변수 의존 + 함수 역할 혼합
    total = wrong_count_alarms(h2, m2, s2) - wrong_count_alarms(h1, m1, s1)

    return total


# ======================================================
# ✅ 풀이 1: 수학적 누적 카운팅 (정답)
# ======================================================

def count_until(h, m, s):
    t = h * 3600 + m * 60 + s

    minute_meet = math.floor(59 * t / 3600) + 1
    hour_meet = math.floor(719 * t / 43200) + 1

    triple = (t // 43200) + 1

    return minute_meet + hour_meet - triple


def event_at(h, m, s):
    t = h * 3600 + m * 60 + s
    return 1 if ((59 * t) % 3600 == 0 or (719 * t) % 43200 == 0) else 0


def solution(h1, m1, s1, h2, m2, s2):
    return (
        count_until(h2, m2, s2)
        - count_until(h1, m1, s1)
        + event_at(h1, m1, s1)
    )


# ======================================================
# 🟡 풀이 2: 1초 단위 완전 시뮬레이션
# ======================================================

def solution_simulation(h1, m1, s1, h2, m2, s2):
    t1 = h1 * 3600 + m1 * 60 + s1
    t2 = h2 * 3600 + m2 * 60 + s2

    ans = 0
    for t in range(t1, t2 + 1):
        if (59 * t) % 3600 == 0 or (719 * t) % 43200 == 0:
            ans += 1
    return ans


# ======================================================
# 🟡 풀이 3: 이벤트 시각 병합 시뮬레이션
# ======================================================

def solution_merge(h1, m1, s1, h2, m2, s2):
    t1 = h1 * 3600 + m1 * 60 + s1
    t2 = h2 * 3600 + m2 * 60 + s2

    kM, kH = 0, 0
    last = None
    ans = 0

    while True:
        tM = kM * 3600 / 59
        tH = kH * 43200 / 719
        t = min(tM, tH)

        if t > t2:
            break

        if t >= t1:
            if last is None or abs(t - last) > 1e-12:
                ans += 1
                last = t

        if tM <= tH:
            kM += 1
        if tH <= tM:
            kH += 1

    return ans
