"""Ready Check / MAZE DM solver: text -> answer line (or None if no maze). Pure, no network."""
import re
import puzzle_lib as P

ID_RE = re.compile(r'\b(RC-[0-9A-Z]+(?:-[0-9A-Z]+)*|MAZE-\d+)\b')


def grid(t):
    t = P.normalize(t) if hasattr(P, 'normalize') else t
    g = P.parse_grid(t)
    if g:
        return g, t
    rows = [l.strip() for l in t.split('\n')]
    best, cur = [], []
    for r in rows + ['']:
        rr = r.replace(' ', '') if re.match(r'^(\S )+\S$', r) else r
        if rr and re.match(r'^[#.A-Za-z<>^v@*0-9]+$', rr) and '#' in rr:
            cur.append(rr)
        else:
            if len(cur) > len(best):
                best = cur
            cur = []
    if len(best) >= 3 and any('S' in r for r in best):
        return best, t
    return None, t


def replay(g, R, path):
    W = max(len(r) for r in g)
    G = [r.ljust(W, '#') for r in g]
    r, c = next((i, x.index('S')) for i, x in enumerate(G) if 'S' in x)
    keys = set()
    for d in path:
        dr, dc = P.DIRS[d]
        r, c = r + dr, c + dc
        ch = G[r][c]
        if ch in R['wall']:
            return False
        if ch in R['door'] and R['door'][ch] not in keys:
            return False
        if R['arrows'] and ch in P.ARROW and P.ARROW[ch] != d:
            return False
        if ch in R['keys']:
            keys.add(ch)
    return G[r][c] == R['goal']


def answer(text):
    g, t = grid(text or '')
    if not g:
        return None
    R = P.maze_rules(t, g)
    if not any(R['goal'] in r for r in g):
        return None
    path = ''.join(P.maze_bfs(g, R))
    if not replay(g, R, path):
        raise P.Fail('replay failed')
    raw = re.search(r'(?i)(no (?:shorthand|compression|run.?length)|do not (?:shorten|compress)|full (?:move )?string|uncompressed)', t)
    mv = path if raw else P.rle(path)
    m = ID_RE.search(t)
    pre = m.group(1) if m else None
    line = ('%s %d %s' % (pre, len(path), mv)) if pre else ('%d %s' % (len(path), mv))
    return {'line': line, 'id': pre, 'steps': len(path), 'path': path, 'rle': P.rle(path)}


if __name__ == '__main__':
    import sys
    for f in sys.argv[1:]:
        a = answer(open(f).read())
        print(f, a and a['line'][:90], a and a['steps'])
