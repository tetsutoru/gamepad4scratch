# gamepad4scratch  ゲームパッド フォー スクラッチ
このプロジェクトは、USB接続のゲームパッドあるいはジョイスティックを（主にRaspberry Piの）Scratch 1.4で使えるようにするものです。Python / pygameがゲームパッドとScratchの間にいて、情報の伝達を行ないます。

このプロジェクトには、PythonとScratchで書かれたゲームパッドテスターのコードが含まれ、ゲームパッドの機能をチェックしたり、Scratchやpygameのコードをどのように書いたら良いかを知ることができるようになっています。


1. Gamepad.desktop：
    デスクトップに置くランチャーアイコンで、(2)を起動します。
2. gamepad_tester.py：
    Python3で書かれたテスターです。ゲームパッドから情報を得てScratch-RSPに流すと同時に画面上にも表示します。
3. GAMEPAD_TEMPLATE.sb：
    Scratch 1.4のテスターと参考用コードで、Scratch-RSP経由で受信したメッセージやセンサー値更新によって各種動作を行ないます。
4. scratchRSP.py：
    Scratch-RSPのサーバーへ送信をするクラスです。今回は使っていませんが、受信機能も含んでいます。
5. send_joystick.py：
    ゲームパッドからの情報を加工してScratch-RSPへ流す仕組み（関数）です。
6. textprint.py：
    ゲームパッドからの情報をpygameウィンドウに表示する仕組み（クラス）です。


(1)によって(2)が起動されます。(3)は、手動で起動してください。
(3)のScratchコード改造からスタートして、ゲームパッドを使えるコードを書くことができます。


# Scratch Remote Sensors Protocol、あるいはScratch-RSPに関する公式情報

Remote Sensors Protocol (Scratch 1.4)
https://en.scratch-wiki.info/wiki/Remote_Sensors_Protocol

Python 2でのサンプルコード
https://en.scratch-wiki.info/wiki/Communicating_to_Scratch_via_Python_with_a_GUI

Python 3でのサンプルコード
https://en.scratch-wiki.info/wiki/Communicating_to_Scratch_via_Python
