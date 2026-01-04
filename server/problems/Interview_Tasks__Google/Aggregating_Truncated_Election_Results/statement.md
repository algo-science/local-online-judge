# Aggregating Truncated Election Results: Concepts & Logic

## 🗳️ Problem Statement

There is an election going on, and there is a single central authority (which gives the results) and two voting districts.

Each district collects and counts its votes, ranks the results (effectively, running a single-district version of the elections), and sends them up to the central authority for the final results.

**The Trick:** The results from the voting districts are truncated. Specifically: only the **Top N** (e.g., N=5) ranked candidates get sent to the central authority (along with their vote counts).

**The Task:** Implement the central authority algorithm, which is to designate the winner or declare that it is impossible to do that.

---

## 📝 Example Scenarios

### Scenario 1: The "Impossible" Case (Close Race)
In this case, the hidden votes create enough uncertainty that we cannot be sure who won.

**District A (Threshold A = 3)**
- `aa`: 10
- `bb`: 9
- `cc`: 9
- `dd`: 8
- `jj`: 3

**District B (Threshold B = 4)**
- `mm`: 11
- `nn`: 9
- `oo`: 8
- `jj`: 7
- `dd`: 4

**Result:** `Impossible`  
*(Candidate 'aa' might have won, or 'mm', or 'dd'. The range of uncertainty overlaps).*

### Scenario 2: The "Possible" Case (Clear Winner)
In this case, the winner's lead is larger than the maximum possible hidden votes.

**District A (Threshold A = 2)**
- `Alice`: 100
- `Bob`: 10
- `Charlie`: 5
- `Dave`: 5
- `Eve`: 2 

**District B (Threshold B = 5)**
- `Alice`: 80
- `Frank`: 8
- `George`: 8
- `Harry`: 7
- `Ivy`: 5 

**Result:** `Alice`

**Logic:**
- Alice Min: 100 + 80 = 180.
- Bob Max: 10 + 5 (Max hidden in B) = 15.
- Outsider Max: 2 (Threshold A) + 5 (Threshold B) = 7.
- Since 180 > 15, Alice is the definitive winner.

---

## 1. The Core Logic: Range Analysis
Since we receive partial data, we cannot calculate a single exact score for every candidate. We must calculate a score range `[Min, Max]`.

### 📉 Lower Bound (MinScore)
This is the "Guaranteed" score.
- **Principle:** Sum the votes we explicitly see in the Top N lists.
- **Missing Data:** If a candidate is missing from a district's Top N, we assume they got **0 votes** in that district.
- **Formula:** `MinScore(C) = Sum(Votes Explicitly Seen)`

### 📈 Upper Bound (MaxScore)
This is the "Potential" score.
- **Principle:** We must give the candidate the maximum benefit of the doubt.
- **The Threshold Rule:** The vote count of the N-th (last visible) person in a district is the **Threshold (T)**. If a candidate is missing from that district, they could have received any number of votes up to T.
- **Formula:** `MaxScore(C) = MinScore(C) + Sum(Thresholds of districts where C is missing)`

### 🏆 The Condition for Victory
To declare a definitive winner, one candidate must be mathematically "untouchable." Candidate W is the winner if and only if:
`MinScore(W) > MaxScore(Others)` for all other candidates O.

---

## 3. Extension: Handling N-Districts
If there are K districts instead of 2, the logic remains linear `O(K * N)`.

1.  Precompute `thresholds[i]` for all districts `i = 0...K-1`.
2.  Start with `MinScore` (sum of visible votes).
3.  Iterate through all districts. If the candidate is missing from district `i`, add `thresholds[i]` to calculate the `MaxScore`.

---

## 📥 Input Format
- First line: Two integers `K` (number of districts) and `N` (Top N truncation).
- Then `K` blocks follow. Each block represents a district:
    - First line of block: Integer `M` (number of candidates reported).
    - Next `M` lines: A string `Name` and an integer `Votes`.

## 📤 Output Format
- Print the name of the definitive winner.
- If no definitive winner can be determined, print `Impossible`.

## 🛑 Constraints
- `1 <= K <= 100`
- `1 <= N <= 1000`
- Names are alphanumeric strings.

