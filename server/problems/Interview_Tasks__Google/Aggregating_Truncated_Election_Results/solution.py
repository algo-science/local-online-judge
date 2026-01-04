import sys
from collections import defaultdict

def solve():
    try:
        # Read K and N
        line1 = sys.stdin.read().split()
        if not line1:
            return
            
        iterator = iter(line1)
        
        try:
            K = int(next(iterator))
            N = int(next(iterator))
        except StopIteration:
            return

        min_scores = defaultdict(int)
        seen_in_district = defaultdict(set)
        district_thresholds = []

        total_threshold_sum = 0

        for i in range(K):
            try:
                M = int(next(iterator))
            except StopIteration:
                break
                
            last_votes = 0
            
            for _ in range(M):
                name = next(iterator)
                votes = int(next(iterator))
                
                min_scores[name] += votes
                seen_in_district[name].add(i)
                last_votes = votes # detailed list assumes sorted desc, but last one is simply the M-th
            
            # Threshold logic
            # If M < N, the list is complete, meaning all other candidates got 0. Threshold = 0.
            # If M >= N, the list is truncated. The unseen candidates got at most 'last_votes'.
            threshold = last_votes if M >= N else 0
            district_thresholds.append(threshold)
            total_threshold_sum += threshold

        # Check for winner
        # To win, MinScore(W) > MaxScore(Others)
        # MaxScore(C) = MinScore(C) + Sum(Thresholds where C not seen)
        
        # Also consider "Outsider"
        # MaxScore(Outsider) = Sum(All Thresholds)
        
        # Optimization:
        # MaxScore(C) = MinScore(C) + (TotalThreshold - Sum(Thresholds where C seen))
        
        candidates = list(min_scores.keys())
        potential_winners = []
        
        # Max possible score of any purely unknown candidate
        outsider_max = total_threshold_sum 
        
        # Calculate MaxScores for all known candidates
        max_scores = {}
        for c in candidates:
            seen_threshold_sum = sum(district_thresholds[i] for i in seen_in_district[c])
            missing_threshold_sum = total_threshold_sum - seen_threshold_sum
            max_scores[c] = min_scores[c] + missing_threshold_sum

        # Ideally, we find the candidate with the highest MinScore
        # If their MinScore > MaxScore of everyone else (including Outsider), they win
        
        best_candidate = None
        best_min = -1
        
        for c in candidates:
            if min_scores[c] > best_min:
                best_min = min_scores[c]
                best_candidate = c
            elif min_scores[c] == best_min:
                best_candidate = None # Tie for lead requires checking, but usually means no definitive unique high min

        if not best_candidate:
            # If no unique leader in MinScore, tough for them to beat MaxScores, but let's check properly
            # Actually, the logic is: Exists W such that for all O != W: Min(W) > Max(O)
            pass

        # Robust Check:
        # Check every candidate to see if they are a specific winner
        definitive_winner = None
        
        for cand in candidates:
            # Can 'cand' win?
            # Must beat outsider
            if min_scores[cand] <= outsider_max:
                continue
                
            # Must beat all other known candidates
            can_win = True
            for opponent in candidates:
                if cand == opponent:
                    continue
                if min_scores[cand] <= max_scores[opponent]:
                    can_win = False
                    break
            
            if can_win:
                if definitive_winner is None:
                    definitive_winner = cand
                else:
                    # Multiple winners? Should be impossible by logic (if A > B_max and B > A_max -> A > B_min + gap and B > A_min + gap)
                    # Use stricter logic: Min(A) > Max(B) => A definitely beats B
                    definitive_winner = "Impossible"
                    break
        
        if definitive_winner and definitive_winner != "Impossible":
            print(definitive_winner)
        else:
            print("Impossible")

    except Exception as e:
        # print(e) # Debug
        print("Impossible")

if __name__ == '__main__':
    solve()
