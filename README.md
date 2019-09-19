# gamepad4scratch  ゲームパッド フォー スクラッチ([日本語はこちら](./README-ja.md))
This project is to add gamepad / joystick support for Scratch 1.4 mainly on Raspberry Pi. Python / pygame is in between the gamepad and Scratch to transfer information via Scratch-RSP or Scratch Remote Sensors Protocol.


This project contains gamepad tester code in Python and Scratch, which will work together for you to check your gamepad controls and to know how to use them in your code in Scratch or pygame.


1. Gamepad.desktop: 
    Launcher icon to place on the desktop, which will launch (2).
2.  gamepad_tester.py: 
    Tester code in Python3. Get information from gamepads and display it on the screen while transfering it via Scratch-RSP.
3.  GAMEPAD_TEMPLATE.sb: 
    Tester/example code in Scratch 1.4 to makes actions by broadcast messages and sensor value updates received via Scratch-RSP.
4.  scratchRSP.py: 
    Scratch-RSP class to talk to the server. It contains listener function, too.
5.  send_joystick.py: 
    Contains a function to send processed gamepad information via Scratch-RSP.
6.  textprint.py: 
    Contains a function to display processed gamepad information on the pygame window.

(1) launches (2), then please launch (3) by yourself.
You can start by tinkering with (3), Scratch code template to make your own code playable with gamepads.


# Reference to Scratch Remote Sensors Protocol

Remote Sensors Protocol (Scratch 1.4)
https://en.scratch-wiki.info/wiki/Remote_Sensors_Protocol

Code in Python 2
https://en.scratch-wiki.info/wiki/Communicating_to_Scratch_via_Python_with_a_GUI

Code in Python 3
https://en.scratch-wiki.info/wiki/Communicating_to_Scratch_via_Python
