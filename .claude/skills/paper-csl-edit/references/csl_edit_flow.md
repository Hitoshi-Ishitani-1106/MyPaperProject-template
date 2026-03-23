# CSL Edit Flow

## 目的
対象誌の投稿規定に記載された参考文献フォーマットに合わせて、既存 CSL（例: `refs/vancouver.csl`）を安全に差分編集するための手順を定める。

## 入力前チェック
- 投稿規定の原文から **公式な引用サンプル** を最低 3 件（原著論文、オンライン先行、書籍章/会議録など）抽出済みか。
- 規則（著者人数、et al. 閾値、タイトルの大小文字、雑誌名の表記、DOI/URL、オンライン先行の書き方など）が箇条書きになっているか。
- テスト用 CSL-JSON（多人数著者、オンライン先行、巻号欠落、書籍章、和文誌、粒子姓など）を作成済みか。

## プロンプトテンプレート
```
@file:skills/paper-csl-edit/references/csl_edit_flow.md を読み込んでください。

以下の仕様リストに完全準拠するよう、`@file:refs/vancouver.csl` を差分編集してください。
- ベースCSL: Vancouver
- 著者: 最大6名を列挙、7名以上で最初の6名 + "et al."
- タイトル: sentence case、末尾ピリオド無し
- 雑誌名: Index Medicus 略称、斜体、末尾ピリオド無し
- 年;巻(号):起-了
- DOI: `doi:10.xxxx/xxxx`、末尾句読点無し
- Online ahead of print: `年 Epub YYYY Mon DD` を年の直後に挿入
- 和文誌: ローマ字表記 + `[in Japanese]`
- 章/会議録: 指定フォーマット ...
(必要に応じ追記)

作業要件:
1. 変更は `<citation>` および `<bibliography>` セクションで必要なノード（`names`, `name`, `text`, `group`, `choose` 等）のみに限定。
2. XML 差分のみを提示し、変更した完全スニペットを含める。
3. 変更理由と対応する仕様項目を短く説明。

検証:
1. `pandoc sample.md --citeproc --bibliography=tests.json --csl=refs/vancouver.csl -o check.docx`
2. 出力が作例と句読点レベルで一致するか確認。差異があれば追加修正を提案。
```

## 追加ガイド
- 著者人数ルールは `et-al-min` と `et-al-use-first` で制御する。
- 雑誌名の斜体は `text` ノードに `font-style="italic"` を付与。
- タイトルの sentence case は `text case="sentence"` を利用。ただし固有名詞保護が必要な場合は `text` ノードに `text-case="title" form="short"` 等を補助。
- DOI/URL 表記は `group` ノードで終端句読点の二重化を防ぐ。
- 和文識別には `choose` / `if variable="language"` を使い `[in Japanese]` を付与。
- オンライン先行や巻号欠落時は `choose` で条件分岐させる。

## 推奨テスト
- `tests.json` に以下を含める：
  - 著者 3 名、7 名
  - Online ahead of print
  - DOI 有/無
  - 書籍章 / 会議録
  - 和文誌
  - 粒子姓（van der ...）

## 出力確認
- 差分は apply_patch 互換の XML ブロック形式（`*** Update File`）または `diff` 形式で提示。
- 変更理由に該当仕様項目への参照（例: 「仕様項目 #3: 雑誌名斜体」）を添える。
