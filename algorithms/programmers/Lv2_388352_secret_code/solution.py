from itertools import combinations

# --------------------------------------------------
# Version 1
# 기본 구현: 헬퍼 함수로 쿼리 검증 로직 분리
# --------------------------------------------------

def solution_v1(n, q, ans):
    """
    모든 가능한 5개 조합을 생성하고,
    각 조합이 모든 쿼리 조건을 만족하는지 검사한다.
    """

    def check_one_query(code, query, answer):
        return len(set(code) & set(query)) == answer

    count = 0
    for code in combinations(range(1, n + 1), 5):
        valid = True
        for i in range(len(q)):
            if not check_one_query(code, q[i], ans[i]):
                valid = False
                break
        if valid:
            count += 1

    return count


# --------------------------------------------------
# Version 2
# zip을 사용한 간결한 구현
# --------------------------------------------------

def solution_v2(n, q, ans):
    """
    zip(q, ans)을 사용해 쿼리와 응답을 함께 순회한다.
    """

    count = 0
    for code in combinations(range(1, n + 1), 5):
        valid = True
        for query, answer in zip(q, ans):
            if len(set(code) & set(query)) != answer:
                valid = False
                break
        if valid:
            count += 1

    return count


# --------------------------------------------------
# Version 3 (최종 권장)
# set 생성 위치를 최적화한 버전
# --------------------------------------------------

def solution(n, q, ans):
    """
    최종 풀이:
    - q를 미리 set으로 변환
    - code도 후보마다 한 번만 set으로 변환
    """

    q_sets = [set(query) for query in q]
    count = 0

    for code in combinations(range(1, n + 1), 5):
        code_set = set(code)

        for query_set, answer in zip(q_sets, ans):
            if len(code_set & query_set) != answer:
                break
        else:
            # break 없이 모든 쿼리를 통과한 경우
            count += 1

    return count
