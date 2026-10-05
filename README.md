# railfence 栅栏密码

终端里的栅栏密码（rail fence cipher）：把明文按**之字形**写在 r 条"栅栏"上，
加密时按栅栏逐行读出，解密时用**周期长度 2(r−1)** 的数学反推回去。

```bash
$ railfence -r 3 enc "WEAREDISCOVEREDFLEEATONCE"
WECRLTEERDSOEEFEAOCAIVDEN

$ railfence -r 3 dec "WECRLTEERDSOEEFEAOCAIVDEN"
WEAREDISCOVEREDFLEEATONCE

$ railfence -r 3 --show-rails enc "WEAREDISCOVEREDFLEEATONCE"
W   E   C   R   L   T   E
 E R D S O E E F E A O C
  A   I   V   D   E   N
--------------------
WECRLTEERDSOEEFEAOCAIVDEN
```

## 参数

| 参数 | 说明 |
|---|---|
| `-r / --rails` | 栅栏条数（默认 3），必须 ≥ 1 |
| `enc` / `dec` | 加密 / 解密 |
| `--show-rails` | 加密时同时打印之字形排布 |

## 设计取舍

- 解密不模拟重写：先用 `pos mod 2(r−1)` 算出每个明文位置所属栅栏，
  再把密文按栅栏分段回填、按原顺序读回。纯数学，一次遍历。
- `rails=1` 时之字形退化成一行，编解码都是恒等变换（会打印提示）。
- 只做字符转置，不改字符本身；大小写、标点、中文都原样保留。

## 已知局限

- **这是古典密码，不是安全加密**：栅栏数很小，暴力尝试即可破解；
  切勿用于保护真实秘密。
- 命令行参数可能被 shell 历史记录下来，敏感文本请用管道输入。
- 不支持多轮/密钥派生等现代特性。

## License

MIT, Copyright (c) 2026 ljiang9
