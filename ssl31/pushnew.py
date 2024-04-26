import json

# matrix = [[0 for _ in range(6)] for _ in range(6)]/

matrix = [[100, 50, 30, 30, 40, 50],
          [50, 100, 40, 40, 50, 50],
          [30, 40, 100, 70, 80, 70],
          [30, 40, 70, 100, 80, 40],
          [40, 50, 80, 80, 100, 40],
          [50, 50, 70, 40, 40, 100]]

with open("newresults.json", 'w') as f:
    json.dump(matrix, f)
    
with open("newresults.json", 'r') as f:
    print(json.load(f))
