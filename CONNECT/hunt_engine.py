"""THE HUNT — движок игры v3. Чистая логика, без Flask."""
import math
import random
from collections import deque
from functools import lru_cache

SIZE = 31
GUARD_SIGHT = 5
GUARD_SIGHT_SNEAK = 3
TRAIL_LEN = 10
ALARM_EVERY = 45
MAX_GUARDS = 5
CHASE_LOSE = 4          # ходов без контакта, после которых егерь начинает искать
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))

ITEM_NAMES = {"bottle": "бутылка", "smoke": "дымовая шашка", "emp": "ЭМИ-импульс"}


# ---------------------------------------------------------------- карта
@lru_cache(maxsize=32)
def build_maze(seed):
    rng = random.Random(seed)
    n = SIZE
    g = [[1] * n for _ in range(n)]
    g[1][1] = 0
    stack = [(1, 1)]
    while stack:
        x, y = stack[-1]
        nb = [(x + dx * 2, y + dy * 2, dx, dy) for dx, dy in DIRS
              if 0 < x + dx * 2 < n - 1 and 0 < y + dy * 2 < n - 1
              and g[y + dy * 2][x + dx * 2]]
        if nb:
            nx, ny, dx, dy = rng.choice(nb)
            g[y + dy][x + dx] = 0
            g[ny][nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    for _ in range(5):
        rx = rng.randrange(3, n - 5, 2)
        ry = rng.randrange(3, n - 5, 2)
        for yy in range(ry, ry + 3):
            for xx in range(rx, rx + 3):
                g[yy][xx] = 0
        if rng.random() < 0.6:
            g[ry + 1][rx + 1] = 1

    cands = []
    for y in range(1, n - 1):
        for x in range(1, n - 1):
            if g[y][x]:
                h = not g[y][x - 1] and not g[y][x + 1]
                v = not g[y - 1][x] and not g[y + 1][x]
                if h != v:
                    cands.append((x, y))
    rng.shuffle(cands)
    for x, y in cands[:len(cands) // 6]:
        g[y][x] = 0
    return tuple(tuple(r) for r in g)


def is_wall(g, x, y):
    return x < 0 or y < 0 or x >= SIZE or y >= SIZE or g[y][x] == 1


def neighbors(g, x, y):
    return [(x + dx, y + dy) for dx, dy in DIRS if not is_wall(g, x + dx, y + dy)]


def bfs(g, src):
    dist = {src: 0}
    q = deque([src])
    while q:
        c = q.popleft()
        for nb in neighbors(g, *c):
            if nb not in dist:
                dist[nb] = dist[c] + 1
                q.append(nb)
    return dist


def los(g, x0, y0, x1, y1):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while (x, y) != (x1, y1):
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
        if (x, y) == (x1, y1):
            break
        if is_wall(g, x, y):
            return False
    return True


def step_toward(g, src, dst, blocked=()):
    if src == dst:
        return src
    d = bfs(g, dst)
    if src not in d:
        return src
    best, bd = src, d[src]
    for nb in neighbors(g, *src):
        if nb in blocked:
            continue
        if d.get(nb, 999) < bd:
            best, bd = nb, d[nb]
    return best


# ---------------------------------------------------------------- новая игра
def new_game(seed=None):
    seed = seed or random.randrange(1, 10 ** 9)
    rng = random.Random(seed * 7 + 1)
    g = build_maze(seed)
    player = (1, 1)
    dist = bfs(g, player)

    spots = [c for c in dist if dist[c] >= 30 and len(neighbors(g, *c)) >= 2]
    if not spots:
        spots = [c for c in dist if dist[c] >= 20 and len(neighbors(g, *c)) >= 2]
    target = rng.choice(spots)

    far = [c for c in dist if dist[c] >= 14 and c != target]
    rng.shuffle(far)
    picked = []
    for c in far:
        if all(abs(c[0] - p[0]) + abs(c[1] - p[1]) >= 9 for p in picked) \
                and abs(c[0] - target[0]) + abs(c[1] - target[1]) >= 4:
            picked.append(c)
        if len(picked) == 3:
            break

    types = ["patrol", "patrol", "tracker"]
    guards = [{"pos": list(c), "type": types[i], "mode": "patrol",
               "goal": None, "seen": None, "lost": 0, "search": 0,
               "stun": 0, "alert": 0, "distract": 0}
              for i, c in enumerate(picked)]

    # предметы, разбросанные по лабиринту
    used = set(picked) | {target}
    pool = [c for c in dist if dist[c] >= 5 and c not in used]
    rng.shuffle(pool)
    kinds = ["bottle", "bottle", "smoke", "emp", "bottle", "smoke", "emp"]
    pickups = [[c[0], c[1], k] for c, k in zip(pool[:7], kinds)]

    return {
        "seed": seed,
        "player": list(player),
        "facing": [1, 0],
        "target": {"pos": list(target), "mode": "hide", "goal": None,
                   "stamina": 6, "rest": 0},
        "guards": guards,
        "trail": [list(player)],
        "inv": {"bottle": 2, "smoke": 1, "emp": 1},
        "pickups": pickups,
        "smoke": [],
        "corpses": [],
        "kills": 0,
        "turns": 0,
        "status": "playing",
        "sneak": False,
        "events": [["подключение установлено", "g"],
                   ["цель где-то в секторе. она знает, что её ищут", "d"],
                   ["в рюкзаке: 2 бутылки, дымовая, ЭМИ (клавиши 1-2-3)", "d"]],
    }


# ---------------------------------------------------------------- ход
def _throw_target(g, P, facing):
    fx, fy = facing
    L = P
    for _ in range(6):
        n = (L[0] + fx, L[1] + fy)
        if is_wall(g, *n):
            break
        L = n
    return L


def _use_item(g, s, P, use, ev):
    s["inv"][use] -= 1
    if use == "bottle":
        L = _throw_target(g, P, s["facing"])
        dl = bfs(g, L)
        hit = 0
        for gd in s["guards"]:
            G = tuple(gd["pos"])
            if dl.get(G, 99) <= 12:
                gd["mode"] = "search"
                gd["seen"] = list(L)
                gd["goal"] = list(L)
                gd["search"] = 9
                gd["distract"] = 5
                gd["lost"] = 0
                gd["alert"] = 0
                hit += 1
        ev.append(["бутылка разбилась. " + ("егеря идут на шум" if hit else "никто не услышал"), "g" if hit else "d"])
    elif use == "smoke":
        for y in range(P[1] - 3, P[1] + 4):
            for x in range(P[0] - 3, P[0] + 4):
                if not is_wall(g, x, y) and math.hypot(x - P[0], y - P[1]) <= 2.3:
                    s["smoke"] = [c for c in s["smoke"] if (c[0], c[1]) != (x, y)]
                    s["smoke"].append([x, y, 8])
        ev.append(["дымовая шашка. в дыму тебя не видно", "g"])
    elif use == "emp":
        n = 0
        for gd in s["guards"]:
            if math.hypot(gd["pos"][0] - P[0], gd["pos"][1] - P[1]) <= 6.5:
                gd["stun"] = 4
                gd["mode"] = "search"
                gd["seen"] = list(gd["pos"])
                gd["goal"] = None
                gd["alert"] = 0
                n += 1
        ev.append(["ЭМИ: оглушено егерей — %d" % n, "g" if n else "d"])


def step(s, dx, dy, use=None):
    """Один ход. Возвращает False, если ход невозможен и не засчитан."""
    if s["status"] != "playing":
        return False
    g = build_maze(s["seed"])
    px, py = s["player"]
    ev = []

    if use:
        if use not in ITEM_NAMES or s["inv"].get(use, 0) <= 0:
            return False
        if use == "bottle" and _throw_target(g, (px, py), s["facing"]) == (px, py):
            return False
        sneak = True
    else:
        sneak = (dx, dy) == (0, 0)
        if not sneak:
            if abs(dx) + abs(dy) != 1 or is_wall(g, px + dx, py + dy):
                return False
            px, py = px + dx, py + dy
            s["facing"] = [dx, dy]

    s["player"] = [px, py]
    P = (px, py)
    s["sneak"] = sneak
    s["turns"] += 1
    t = s["turns"]
    rng = random.Random(s["seed"] * 1000003 + t)
    s["trail"] = (s["trail"] + [[px, py]])[-TRAIL_LEN:]

    # дым тает
    s["smoke"] = [[x, y, ttl - 1] for x, y, ttl in s["smoke"] if ttl - 1 > 0]

    if use:
        _use_item(g, s, P, use, ev)

    # подобрать предмет
    for pk in list(s["pickups"]):
        if (pk[0], pk[1]) == P:
            s["inv"][pk[2]] = s["inv"].get(pk[2], 0) + 1
            s["pickups"].remove(pk)
            ev.append(["подобрал: " + ITEM_NAMES[pk[2]], "g"])

    # наступил на (не оглушённого) егеря
    if any(tuple(gd["pos"]) == P and gd.get("stun", 0) == 0 for gd in s["guards"]):
        return _finish(s, ev, "caught")

    # дошёл до цели — начинается погоня
    T = tuple(s["target"]["pos"])
    if abs(T[0] - px) + abs(T[1] - py) <= 1:
        return _finish(s, ev, "chase")

    dp = bfs(g, P)
    _target_ai(g, s, P, sneak, dp, rng, ev)

    if _guards_ai(g, s, P, sneak, dp, rng, ev):
        return _finish(s, ev, "caught")

    if t % ALARM_EVERY == 0 and len(s["guards"]) < MAX_GUARDS:
        far = [c for c in dp if dp[c] >= 16]
        if far:
            c = rng.choice(far)
            s["guards"].append({
                "pos": list(c),
                "type": "tracker" if len(s["guards"]) % 2 == 0 else "patrol",
                "mode": "search", "goal": None, "seen": list(P),
                "lost": 0, "search": 8, "stun": 0, "alert": 0, "distract": 0})
            ev.append(["[ТРЕВОГА] на уровень вышел ещё один егерь", "c"])

    s["events"] = ev
    return True


def finish_chase(s, win):
    """Итог забега. win=True -> цель остановлена."""
    if s["status"] != "chase":
        return False
    if win:
        s["status"] = "found"
        s["events"] = [["ЦЕЛЬ ОСТАНОВЛЕНА", "g"]]
    return True

def resolve_duel_win(s):
    """Игрок победил егеря в перестрелке: тело остаётся, игра продолжается."""
    if s["status"] != "caught":
        return False
    P = tuple(s["player"])

    dead = next((g for g in s["guards"]
                 if tuple(g["pos"]) == P and g.get("stun", 0) == 0), None)
    if dead is None and s["guards"]:
        dead = min(s["guards"],
                   key=lambda g: abs(g["pos"][0] - P[0]) + abs(g["pos"][1] - P[1]))
    if dead is not None:
        s["guards"].remove(dead)
        s.setdefault("corpses", []).append(list(dead["pos"]))
    s["kills"] = s.get("kills", 0) + 1

    # выстрелы слышны: остальные, кто гнался, ищут, но не мгновенно бросаются
    for gd in s["guards"]:
        if gd["mode"] == "chase":
            gd.update({"mode": "search", "seen": list(P), "goal": None,
                       "search": 7, "lost": 0, "alert": 2})

    s["status"] = "playing"
    s["events"] = [["егерь убит. тело осталось в лабиринте", "c"],
                   ["выстрелы слышны далеко. будь осторожен", "w"]]
    return True

def _finish(s, ev, status):
    s["status"] = status
    if status == "caught":
        ev.append(["КОНТАКТ С ЕГЕРЕМ. СВЯЗЬ ПОТЕРЯНА", "c"])
    elif status == "chase":
        ev.append(["ЦЕЛЬ ВПЕРЕДИ. ДОГОНИ ЕЁ!", "g"])
    else:
        ev.append(["ЦЕЛЬ ЗАХВАЧЕНА", "g"])
    s["events"] = ev
    return True


# ---------------------------------------------------------------- ИИ цели
def _target_ai(g, s, P, sneak, dp, rng, ev):
    tg = s["target"]
    T = tuple(tg["pos"])
    d = dp.get(T, 99)
    dist_e = math.hypot(T[0] - P[0], T[1] - P[1])
    sees = los(g, P[0], P[1], T[0], T[1]) and dist_e <= (3.5 if sneak else 7)
    hears = d <= (2 if sneak else 5)
    aware = sees or hears

    if tg["mode"] in ("hide", "sneak") and aware:
        tg["mode"] = "flee"
        tg["stamina"] = 6
        tg["rest"] = 0
        if d <= 9:
            ev.append(["рядом кто-то сорвался с места", "w"])

    if tg["mode"] == "flee":
        if not aware and d >= 10:
            tg["mode"] = "sneak"
            tg["goal"] = None
        else:
            if tg["rest"] > 0:
                tg["rest"] -= 1
                if tg["rest"] == 0:
                    tg["stamina"] = 6
                return
            options = [n for n in neighbors(g, *T) if n != P]
            if options:
                def score(n):
                    exits = len(neighbors(g, *n))
                    return (dp.get(n, 0) + rng.random() * 1.6
                            + (exits - 1) * 0.7 - (5 if exits == 1 else 0))
                best = max(options, key=score)
                tg["pos"] = list(best)
                tg["stamina"] -= 1
                if tg["stamina"] <= 0:
                    tg["rest"] = 2
            return

    if tg["mode"] == "sneak":
        if not tg["goal"]:
            dt = bfs(g, T)
            cands = [c for c in dt
                     if len(neighbors(g, *c)) >= 2 and dp.get(c, 0) >= 14 and dt[c] <= 26]
            if not cands:
                cands = [max(dt, key=lambda c: dp.get(c, 0))]
            tg["goal"] = list(rng.choice(cands))
        goal = tuple(tg["goal"])
        nxt = step_toward(g, T, goal, {P})
        tg["pos"] = list(nxt)
        if nxt == goal:
            tg["mode"] = "hide"
            tg["goal"] = None


# ---------------------------------------------------------------- ИИ егерей
def _guards_ai(g, s, P, sneak, dp, rng, ev):
    sight = GUARD_SIGHT_SNEAK if sneak else GUARD_SIGHT
    smoke = {(c[0], c[1]) for c in s["smoke"]}
    p_hidden = P in smoke
    occupied = {tuple(x["pos"]) for x in s["guards"]}
    floors = list(dp.keys())
    spotted = lost_msg = steps_msg = False

    for i, gd in enumerate(s["guards"]):
        G = tuple(gd["pos"])
        occupied.discard(G)

        # оглушён
        if gd.get("stun", 0) > 0:
            gd["stun"] -= 1
            occupied.add(G)
            continue

        dist = math.hypot(G[0] - P[0], G[1] - P[1])
        distracted = gd.get("distract", 0) > 0
        if distracted:
            gd["distract"] -= 1

        sees = (not p_hidden and G not in smoke
                and dist <= sight and los(g, G[0], G[1], P[0], P[1]))
        if distracted and dist > 1.5:
            sees = False

        if sees:
            if gd["mode"] != "chase":
                gd["alert"] = 0 if dist <= 1.5 else 1   # секунда на реакцию
                if not spotted:
                    ev.append(["!!! ТЕБЯ ЗАМЕТИЛИ", "c"])
                    spotted = True
            gd["mode"] = "chase"
            gd["seen"] = list(P)
            gd["lost"] = 0
        elif gd["mode"] == "chase":
            gd["lost"] += 1
            if tuple(gd["seen"]) == G or gd["lost"] >= CHASE_LOSE:
                gd["mode"] = "search"
                gd["search"] = 7
                gd["goal"] = None
                if not lost_msg:
                    ev.append(["егерь потерял след", "w"])
                    lost_msg = True

        steps = 1
        goal = None
        mode = gd["mode"]

        if mode == "chase":
            goal = tuple(gd["seen"])
            if (s["turns"] + i) % 3 == 0:      # егерь медленнее тебя: 2 хода из 3
                steps = 0
        elif mode == "search":
            if not gd["goal"] or tuple(gd["goal"]) == G:
                ds = bfs(g, tuple(gd["seen"] or list(G)))
                near = [c for c in ds if ds[c] <= 4]
                gd["goal"] = list(rng.choice(near)) if near else list(G)
            goal = tuple(gd["goal"])
            gd["search"] -= 1
            if gd["search"] <= 0:
                gd["mode"] = "patrol"
                gd["goal"] = None
        elif gd["type"] == "tracker":
            goal = tuple(s["trail"][0])
            if goal == G and len(s["trail"]) > 1:
                goal = tuple(s["trail"][1])
            if rng.random() < 0.25:
                steps = 0
        else:
            if rng.random() < 0.25:
                steps = 0
            if not gd["goal"] or tuple(gd["goal"]) == G:
                near = [c for c in floors if 4 <= dp[c] <= 14]
                pool = near if (near and rng.random() < 0.5) else floors
                gd["goal"] = list(rng.choice(pool))
            goal = tuple(gd["goal"])

        if gd.get("alert", 0) > 0:
            gd["alert"] -= 1
            steps = 0

        for _ in range(steps):
            if goal is None:
                break
            nxt = step_toward(g, G, goal, occupied)
            if nxt != G:
                G = nxt
                gd["pos"] = list(G)
            if G == P:
                return True

        occupied.add(G)

        if (not steps_msg and gd["mode"] != "chase"
                and math.hypot(G[0] - P[0], G[1] - P[1]) <= 5
                and not los(g, G[0], G[1], P[0], P[1])):
            ev.append(["шаги за стеной", "w"])
            steps_msg = True

    return False


# ---------------------------------------------------------------- для шаблона
def public_view(s):
    g = build_maze(s["seed"])
    walls = [[x, y] for y in range(SIZE) for x in range(SIZE) if g[y][x]]
    labyrinth = {"size": SIZE, "walls": walls}
    game = dict(s)
    game["alarm_in"] = ALARM_EVERY - (s["turns"] % ALARM_EVERY)
    return labyrinth, game