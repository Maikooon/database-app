# データベースアプリケーションプログラミング演習

## デプロイ先
http://user.keio.ac.jp/~ub497656/dm_app

## Python仮想環境の有効化
1. `cd ~/dm_src` コマンドで移動します。
2. `source venv/bin/activate` コマンドで仮想環境を起動します。
    1. ターミナルに(venv)が表示されるようになります。
    2. setup.shを使用した場合、Flaskがすでにインストールされています。
    3. 仮想環境のPythonのバージョンを使用しないとWebサーバー側で動きません！
3. 仮想環境を終了する場合、`deactivate` を実行します。

## テスト環境でのアプリケーション実行
`flask run`を使用してテスト環境でアプリケーションを実行します。

### SSH環境での実行　※TAサポートなし
1. 別のターミナルで、 `ssh -L 5000:127.0.0.1:5000 ubXXXXXX@remoteX.educ.cc.keio.ac.jp` を実行します（ubXXX…は自分のITCアカウント、remoteXをログイン中のサーバ名に変更）
2. appディレクトリで `flask run` を実行します。
3. Webブラウザで [http://127.0.0.1:5000](http://127.0.0.1:5000/) にアクセスします。

### VSCodeでの実行　※TAサポートなし

1. VSCodeにSSH extensionをインストールします。
2. VSCode上でSSHを使用してサーバに接続します。SSH鍵を設定しておくとパスワードの入力が煩雑になりません。
3. VSCode上でディレクトリを開きます。
4. VSCodeのターミナルでappディレクトリで `flask run` を実行します。
5. ポップアップからWebブラウザを表示することができます。

