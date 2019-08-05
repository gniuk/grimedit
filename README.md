# grimedit

Grab image from a Wayland compositor using [grim] and [slurp].

Draw simple shapes or add text on the image with grimedit.

![](https://github.com/gniuk/grimedit/demo/demo.gif)

## Dependencies

* Python3
* PyQT5
* [grim]
* [slurp]
* [wl-clipboard]

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

Bind a shotcut in your .config/sway/config, and make the window floating.

```sh
bindsym $mod+Shift+a exec grim -g "$(slurp)" - | grimedit
for_window [title="Grimedit"] floating enable
```

## TODO

1. Color choose is not implemented yet.
2. Text edit is not perfect, and no font and font size to choose from, but it's enough to work.
3. Mosaic is not implemented yet.
4. Brush is not implemented yet.

## Notes

* The save button automatically saves the screenshot in ~/Picture/ScreenShot as YMD-h-m-s.png, and a copy to the clipboard.

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
