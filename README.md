# grimedit

Grab image from a Wayland compositor using [grim] and [slurp].

Draw simple shapes or add text on the image with grimedit. Save to ~/Pictures/ScreenShots/ or copy to clipboard.

![](https://github.com/gniuk/grimedit/blob/master/demo/demo.gif)

## Dependencies

* Python3
* PyQT5
* [grim]
* [slurp]
* [wl-clipboard]

Just search and install them with your package manager.

## How to use

```sh
git clone https://github.com/gniuk/grimedit
cd grimedit
sudo make install
```

```sh
grim -g "$(slurp)" - | grimedit
```

To make it more convenient:

Bind a shortcut in your window manager config, e.g. ~/.config/sway/config if you use sway, and make the window floating.

```
bindsym $mod+Shift+a exec grim -g "$(slurp)" - | grimedit
for_window [title="Grimedit"] floating enable
```

## TODO

1. More color options, currently only red.
2. Mosaic.
3. Text edit is not perfect, and no font and font size to choose from, but currently it's enough for me.

## Notes

* The save button automatically saves the screenshot in ~/Pictures/ScreenShots as YMD-h-m-s.png, and a copy to the clipboard.

* The escape key can quit the program with nothing saved.

* The drawed shapes or text cann't be adjust after commit.


Though it is enough for me to work.

The lacking feature maybe added when I keep learning QT5 and PyQT5.

Patches and Contributes are welcome!

## 中文

找了很久，发现 Linux Wayland (Sway) 下面没有可用类似桌面端微信或QQ的截图工具。

试了一下deepin-screenshot，发现截出来的图是黑的，看了下issue，不适用于wayland。

于是用了几天业余时间和周末，学习了一下QT5和PyQT5。

写了这个目前还算能用的类似桌面微信截图的截图工具(实际上只是图片编辑部分)。

希望能帮助到同样有需要的人。

欢迎Patch。

[grim]: https://github.com/emersion/grim
[slurp]: https://github.com/emersion/slurp
[wl-clipboard]: https://github.com/bugaevc/wl-clipboard
