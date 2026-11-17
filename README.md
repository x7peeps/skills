# skills.x7peeps.com

x7peeps 技能库宣传页。静态单页，无构建依赖。

- `index.html` — 生成产物，直接部署
- `data.json` — 70 个技能的结构化数据（分类、描述、渠道）
- `build.py` — 生成器：读 data.json 渲染出 index.html

改内容只动 `data.json`，然后 `python3 build.py`。

技能本体在私有仓库维护；这里是展示层。
