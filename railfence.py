"""railfence: 栅栏密码(之字形)编解码器。

加密: 把明文按之字形写在 r 条"栅栏"上, 然后按栅栏顺序逐行读出。
解密: 先用周期长度算出每个明文位置属于哪条栅栏,
     再把密文按栅栏逐行回填, 最后按之字形顺序读回明文。
"""
import argparse
import sys


def rail_of(pos, rails):
    """明文位置 pos 在 rails 条栅栏下的之字形行号。"""
    if rails <= 1:
        return 0
    cycle = 2 * (rails - 1)
    k = pos % cycle
    return k if k < rails else cycle - k


def encrypt(text, rails):
    """加密。rails=1 时是恒等变换(直接返回原文)。"""
    if rails <= 1:
        return text
    rows = [""] * rails
    for i, ch in enumerate(text):
        rows[rail_of(i, rails)] += ch
    return "".join(rows)


def decrypt(text, rails):
    """解密: 周期长度数学, 不模拟重写。rails=1 时恒等。"""
    n = len(text)
    if rails <= 1 or n == 0:
        return text
    # 每个明文位置属于哪条栅栏
    which = [rail_of(i, rails) for i in range(n)]
    # 密文是按栅栏顺序拼接的: 算每条栅栏占多少字符
    counts = [0] * rails
    for r in which:
        counts[r] += 1
    # 切出每条栅栏的密文段
    segs, off = [], 0
    for r in range(rails):
        segs.append(list(text[off:off + counts[r]]))
        off += counts[r]
    # 按原之字形顺序取回
    idx = [0] * rails
    out = []
    for r in which:
        out.append(segs[r][idx[r]])
        idx[r] += 1
    return "".join(out)


def show_rails(text, rails):
    """把明文按之字形排成栅栏, 用 ~ 标记。"""
    if rails <= 1:
        return text
    n = len(text)
    grid = [[" "] * n for _ in range(rails)]
    for i, ch in enumerate(text):
        grid[rail_of(i, rails)][i] = ch
    return "\n".join("".join(row).rstrip() for row in grid)


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        prog="railfence",
        description="栅栏密码(rail fence cipher): 之字形转置加密/解密。")
    p.add_argument("-r", "--rails", type=int, default=3,
                   help="栅栏条数 (默认 3)")
    p.add_argument("--show-rails", action="store_true",
                   help="加密时同时打印之字形排布")
    p.add_argument("mode", choices=["enc", "dec"],
                   help="enc=加密, dec=解密")
    p.add_argument("text", help="要处理的文本")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.rails < 1:
        print(f"error: 栅栏数必须 >= 1, 得到 {args.rails}", file=sys.stderr)
        return 2
    if args.rails == 1:
        print("注: rails=1 时之字形退化成一行, 编解码都是恒等变换。",
              file=sys.stderr)
    if args.mode == "enc":
        out = encrypt(args.text, args.rails)
        if args.show_rails:
            print(show_rails(args.text, args.rails))
            print("-" * 20)
        print(out)
    else:
        print(decrypt(args.text, args.rails))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
