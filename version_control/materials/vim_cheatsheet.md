# Vim Cheatsheet

If you have not set git's default text editor, it will probably default to Vi/Vim, which is a text editor that can be used directly from the command-line interface. You navigate it only using your keyboard and there are no graphical buttons. When you first use Vim it can be a challenge to even just exit it again. For the purpose of this Git workshop you mostly need to use Vim to type single-line commit messages. To achieve this you will need to know only the handful of keys that we have listed for you here:

### Vim Modes

Vim has a mode for inserting text and several modes for editing text. For us, only two modes will be important:

* **Command mode** is the default mode of Vim. It provides a library of keyboard-based commands to edit text. Pressing the escape key switches back to this mode.

* **Insert mode** allows for the insertion of text. This is the functionality most users associate with text editors. Pressing the i key in command mode switches to insert mode.

### Navigating vim

* **Navigate** the cursor through the arrow keys on your keyboard. This is possible in any mode.

* **Exiting** Vim is possible from Command mode (ESC key) by typing ```:x``` to save and exit or ```:q!``` to force exit without saving. Press enter to submit your command.

&nbsp;

##### In case you would like to know more...

* Type ```vimtutor``` into your terminal for more commands.

* Learn using Vim through this game: [https://vim-adventures.com/](https://vim-adventures.com/).
