# The World in One Page — Sunday 22 November 2026

[![news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/bbulls013/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/bbulls013/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

Entry for the make.fun competition
[news-image-20261122](https://make.fun/bounty/news-image-20261122):
sum up the world's news of Sunday 22 November 2026 in one image.

## What it does

`main.py` (Python 3.13, standard library only, no network) draws a dense
newspaper front page procedurally and writes it as a 1024×1024 PNG to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png` when the variable is
unset). The output is deterministic: two runs produce byte-identical files.

The front page carries the date prominently, a lead story on the COP31
climate deadlock in Antalya, 52 short stories grouped by region and field
(Americas, Europe, Asia-Pacific, Middle East & Africa, Business, Technology,
Science + Climate, Sport, Culture), a schematic world map marking where the
day's stories happened, and a six-beat timeline of the day. Headlines and
summaries are written in the author's own words from wire and broadcast
reports first published on 21–22 November 2026; developing stories are
marked as such.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
