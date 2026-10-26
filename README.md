# Gigatron Ready Check maze solver (DrosGrokBot)
- Slack Socket Mode listener receives the Mothership DM live (5s DM poll backup).
- Parse grid: S start, G goal, # wall, a/b keys, A/B doors.
- BFS over state (row, col, keys held bitmask): doors pass only with matching key -> shortest path.
- Replay moves on the grid to verify validity before sending.
- Run-length encode moves (RRRDD -> R3D2), reply `RC-ID <steps> <moves>` in one DM.
- Solve 2-15 ms; DM-to-answer ~1 s (RC-0089: valid, shortest, 0.9s, Gold Ready).
