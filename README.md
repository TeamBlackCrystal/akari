# AKARI

このリポジトリはMiPAを学ぶ上で参考になる可能性があります。
また、主にこのプロジェクトの主目標は コントリビューターの sousuke0422にMiPACを使ってもらうことで、不便な所などを発見する一種のユーザーテストも兼ねています。
~~あとsousukeにPythonの苦手意識を克服してもらうため~~

また、このプロジェクトはyupixのクリーンアーキテクチャ学習の場としても使用されています

## 使い方


```bash
# venvを作成する
python -m venv .venv

# venvを有効化する
# OSによって異なるので省略

# 依存関係をインストール
pip install -r requirements.txt

# example-config.iniをconfig.iniに改名してtokenとurlを打つ

# DBのマイグレーションを行う
alembic upgrade +1

# Botを実行
python main.py
```