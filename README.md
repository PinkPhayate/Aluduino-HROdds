# Aruduino プログラム

## タスク
- wikiに書きました
  https://github.com/PinkPhayate/Aluduino-HROdds/wiki/TODO-task

## 起動準備

### redis起動コマンド
redis-server /usr/local/etc/redis.conf

## リファレンス
http://garretlab.web.fc2.com/arduino/introduction/beginning_with_7segment_led/
http://shirotsuku.sakura.ne.jp/blog/?p=606


## Useage

1. Arduinoを起動

- Arduino IDEからシリアルポートを起動しておく。
- この時に使ったシリアルポート番号をメモしておく。

2. pythonを起動

- sudoでserial_con.pyを起動。

### serial_con.py
 
コマンド引数にtestと加えると、デバックモードになり、2013年の宝塚記念のオッズがひたすら表示される。
何もなしに実行すると、最も近いレースを対象とする。

