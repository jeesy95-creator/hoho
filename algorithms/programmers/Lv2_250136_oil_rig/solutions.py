
from collections import deque

def solution(land):
    n = len(land)  # 세로 길이
    m = len(land[0])  # 가로 길이
    
    # 각 석유 덩어리의 크기를 저장
    oil_size = {}
    # 각 위치가 어느 덩어리에 속하는지 저장 (-1: 빈 땅)
    oil_id = [[-1] * m for _ in range(n)]
    
    current_id = 0  # 덩어리 고유 번호
    
    # BFS로 석유 덩어리 탐색
    def bfs(start_r, start_c):
        nonlocal current_id
        queue = deque([(start_r, start_c)])
        oil_id[start_r][start_c] = current_id
        size = 1
        
        # 상하좌우 이동
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        
        while queue:
            r, c = queue.popleft()
            
            # 4방향 탐색
            for i in range(4):
                nr, nc = r + dx[i], c + dy[i]
                
                # 범위 체크
                if 0 <= nr < n and 0 <= nc < m:
                    # 석유이고 아직 방문하지 않았으면
                    if land[nr][nc] == 1 and oil_id[nr][nc] == -1:
                        oil_id[nr][nc] = current_id
                        queue.append((nr, nc))
                        size += 1
        
        return size
    
    # 모든 석유 덩어리 찾기
    for i in range(n):
        for j in range(m):
            if land[i][j] == 1 and oil_id[i][j] == -1:
                size = bfs(i, j)
                oil_size[current_id] = size
                current_id += 1
    
    # 각 열마다 획득할 수 있는 석유량 계산
    max_oil = 0
    
    for col in range(m):
        # 이 열에서 만나는 석유 덩어리들 (중복 제거)
        oil_set = set()
        
        for row in range(n):
            if oil_id[row][col] != -1:
                oil_set.add(oil_id[row][col])
        
        # 이 열의 총 석유량
        total = sum(oil_size[oid] for oid in oil_set)
        max_oil = max(max_oil, total)
    
    return max_oil


#-----------------------------------------
#version 2
# 1: oil_info 방식 효율성 떨어짐 
#열별 계산 시 모든 덩어리를 확인해야 함 (O(m × 덩어리 개수))

from collections import deque

def solution(land):
    n = len(land)
    m = len(land[0])
    visited = [[False] * m for _ in range(n)]
    
    def find_oil_cluster(start_row, start_col):
        """BFS로 석유 덩어리를 찾고 크기와 지나는 열 정보 반환"""
        queue = deque([(start_row, start_col)])
        visited[start_row][start_col] = True
        
        size = 1
        cols = set()  # 이 덩어리가 지나는 열들
        cols.add(start_col)
        
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        
        while queue:
            row, col = queue.popleft()
            
            for i in range(4):
                new_row = row + dx[i]
                new_col = col + dy[i]
                
                if 0 <= new_row < n and 0 <= new_col < m:
                    if land[new_row][new_col] == 1 and not visited[new_row][new_col]:
                        visited[new_row][new_col] = True
                        queue.append((new_row, new_col))
                        size += 1
                        cols.add(new_col)
        
        return size, cols
    
    # 모든 석유 덩어리 정보 수집
    oil_info = []  # [(크기, {지나는 열들}), ...]
    
    for i in range(n):
        for j in range(m):
            if land[i][j] == 1 and not visited[i][j]:
                size, cols = find_oil_cluster(i, j)
                oil_info.append((size, cols))
    
    # 각 열마다 석유량 계산
    max_oil = 0
    
    for col in range(m):
        total = 0
        
        # 모든 덩어리를 확인하며 이 열을 지나는지 체크
        for size, cols in oil_info:
            if col in cols:
                total += size
        
        max_oil = max(max_oil, total)
    
    return max_oil

#-----------------------------------------
#version 3
# 2: 열별로 석유 덩어리 매핑 
#장점:

#BFS 과정에서 바로 열 매핑 구축
#열별 계산이 매우 빠름 (이미 매핑된 정보 사용)
#효율성 테스트 통과 가능

#단점:

#defaultdict 추가 사용
#oil_id 방식보다 메모리 사용량 약간 더 많음
from collections import deque, defaultdict

def solution(land):
    n = len(land)
    m = len(land[0])
    visited = [[False] * m for _ in range(n)]
    
    # 각 열에 어떤 덩어리들이 있는지 매핑
    col_to_clusters = defaultdict(set)  # {열: {덩어리ID들}}
    cluster_sizes = {}  # {덩어리ID: 크기}
    cluster_id = 0
    
    def bfs(start_row, start_col, cid):
        """BFS로 석유 덩어리 탐색하며 열 정보 수집"""
        queue = deque([(start_row, start_col)])
        visited[start_row][start_col] = True
        
        size = 1
        cols_in_cluster = set()
        cols_in_cluster.add(start_col)
        
        dx = [-1, 1, 0, 0]
        dy = [0, 0, -1, 1]
        
        while queue:
            row, col = queue.popleft()
            
            for i in range(4):
                new_row = row + dx[i]
                new_col = col + dy[i]
                
                if 0 <= new_row < n and 0 <= new_col < m:
                    if land[new_row][new_col] == 1 and not visited[new_row][new_col]:
                        visited[new_row][new_col] = True
                        queue.append((new_row, new_col))
                        size += 1
                        cols_in_cluster.add(new_col)
        
        # 이 덩어리가 지나는 모든 열에 덩어리 ID 추가
        for col in cols_in_cluster:
            col_to_clusters[col].add(cid)
        
        return size
    
    # 모든 석유 덩어리 찾기
    for i in range(n):
        for j in range(m):
            if land[i][j] == 1 and not visited[i][j]:
                size = bfs(i, j, cluster_id)
                cluster_sizes[cluster_id] = size
                cluster_id += 1
    
    # 각 열의 석유량 계산
    max_oil = 0
    
    for col in range(m):
        total = sum(cluster_sizes[cid] for cid in col_to_clusters[col])
        max_oil = max(max_oil, total)
    
    return max_oil