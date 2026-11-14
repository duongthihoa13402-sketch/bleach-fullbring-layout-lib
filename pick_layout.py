"""Pick a layout page from the library and print panel rects for the target canvas.

Usage:
  python pick_layout.py --n 4                  # 4 格，随机
  python pick_layout.py --n 6 --seed 42        # 可复现
  python pick_layout.py --page c326/p007       # 指定页
  python pick_layout.py --n 4 --canvas 1800x1200 --margin 20
"""
import argparse
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
INDEX_JSON = os.path.join(HERE, "report/fullbring-layout-index.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0, help="需要的格数（=素材张数）")
    ap.add_argument("--page", default="", help="指定页，如 c326/p007")
    ap.add_argument("--canvas", default="1800x1200")
    ap.add_argument("--margin", type=int, default=20)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--index", default=INDEX_JSON)
    a = ap.parse_args()

    W, H = [int(x) for x in a.canvas.lower().split("x")]
    data = json.load(open(a.index, encoding="utf-8"))
    if not data:
        sys.exit("index 为空：先跑 index_layout.py")

    if a.page:
        key = a.page.replace("\\", "/").replace("/", "_")
        if not key.startswith("c"):
            sys.exit("页参数格式应为 c326/p007")
        key = key.replace("_p", "_p")
        if key not in data:
            sys.exit("索引里没有这一页：%s" % a.page)
        pick = key
    else:
        if not a.n:
            sys.exit("给 --n（素材张数）或 --page")

        def usable(v):
            """过滤掉有超薄格/超长条的页——那种页排出来没法用。"""
            pw, ph = v["size"]
            for r in v["rows"]:
                if (r["y1"] - r["y0"]) / ph < 0.055:
                    return False
                for b in r["boxes"]:
                    w = b[3] - b[2]
                    h = b[1] - b[0]
                    if w / pw < 0.06 or h / ph < 0.055:
                        return False
                    if w / max(h, 1) > 7 or h / max(w, 1) > 6:
                        return False
            return True

        pool = [k for k, v in data.items() if v["n"] == a.n and usable(v)]
        if not pool:
            near = sorted({v["n"] for v in data.values()})
            sys.exit("库里没有可用的 %d 格页；现有格数：%s" % (a.n, near))
        if a.seed is not None:
            random.seed(a.seed)
        pick = random.choice(sorted(pool))

    v = data[pick]
    pw, ph = v["size"]
    print("版式取自 %s/p%03d，共 %d 格（库中 %d 格的页共若干）" % (v["ch"], v["page"], v["n"], v["n"]))
    print("原页尺寸 %dx%d" % (pw, ph))

    # 归一化后用 margin + norm*(canvas-2m) 映射：保留原页的相对格缝，不拉伸错位
    cw, chh = W - 2 * a.margin, H - 2 * a.margin
    rects = []
    i = 0
    for r in v["rows"]:
        y0 = a.margin + int(round(r["y0"] / ph * chh))
        y1 = a.margin + int(round(r["y1"] / ph * chh))
        for b in sorted(r["boxes"], key=lambda b: b[2]):
            i += 1
            x0 = a.margin + int(round(b[2] / pw * cw))
            x1 = a.margin + int(round(b[3] / pw * cw))
            rects.append((i, x0, y0, x1, y1))

    print("\n各格坐标（%dx%d，margin %d）" % (W, H, a.margin))
    for n, x0, y0, x1, y1 in rects:
        print("- P%d：(%d,%d)-(%d,%d)｜%dx%d" % (n, x0, y0, x1, y1, x1 - x0, y1 - y0))

    print("\n纵向分段：%s" % "/".join("%.3f" % ((r["y1"] - r["y0"]) / ph) for r in v["rows"]))
    print("每行格数：%s" % "/".join(str(len(r["boxes"])) for r in v["rows"]))
    print("\n可直接粘进提示词：")
    print("版式取自 %s/p%03d，共 %d 格；纵向分段 %s；每行格数 %s" % (
        v["ch"], v["page"], v["n"],
        "/".join("%.3f" % ((r["y1"] - r["y0"]) / ph) for r in v["rows"]),
        "/".join(str(len(r["boxes"])) for r in v["rows"])))


if __name__ == "__main__":
    main()
