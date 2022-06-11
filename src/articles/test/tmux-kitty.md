---
title: "Migrating from tmux to Kitty"
description: ".txt config files should rule all"
publish: true
---

# Migrating from Tmux to Kitty
So sitting at my workdesk waiting for my local changes to compile and deploy, I often find my mind wandering towards the world of [Unix ricing](https://www.reddit.com/r/unixporn/). Some people do it for beauty, others do it for maximizing their productivity. Regardless of the reason, before I go into any of this, let me preface the article by saying that all this is completely unnecessary. Pretty much any terminal will do the trick. But once again, I'm twiddling my thumbs waiting for deployment, so I need _something_ to do. Why not finally migrate my terminal work from ==[tmux](#TODO)== in ==[iTerm2](#TODO)== to ==[Kitty](#TODO)==?

If you haven't heard of Kitty, first of all, I commend you for not wasting as much time as I do reading about development tools instead of actually working! Kitty is a modern GPU-accelerated terminal emulator available for Linux and macOS. It's written in C and python, and it's pretty extensible. It has ==[support for plugins](#TODO)== called kittens, and comes with some default ones like a theme-switcher and ssh utility.

Kitty offers much of the functionality of tmux - things like pane management, custom keybindings, remote control. _But_, Kitty does have some distinct advantages in my mind. For one, Kitty is a terminal _emulator_. Tmux is only a terminal _multiplexer_, and thus also requires a terminal emulator. I'd prefer to simplify the number of tools I use for my work. Kitty can replace both tmux and iTerm2, and adds some features on top like the cool cat that it is. Already mentioned is plugin support, which iTerm2 does technically support, but I always got confused trying to configure it.

Next and most exciting is the inline native image support. Now some terminals support something called ==[sixel graphics](#TODO)==, which I'll admit is pretty neat. Sixel to me is a bandage fix for graphic representation in the terminal because it's not representing imgages as native images, but rather performing some computation to build images out of special ASCII symbols, which means when you try to translate or transform the image in any way, things get weird. Why deal with that when kitty has your back? It can even render GIFs!
```
kitty +kitten icat ~/Downloads/kitten_falling.gif
```
![[animation.gif|"Kitty terminal output with the icat plugin"]]

Another reason I think Kitty is great is that it's text file configurable, which makes it _way_ easier to share configurations between my work and personal computer. You can find an up-to-date copy of my kitten config file in [my dotfiles repository](https://github.com/momja/dotfiles/blob/master/kitty/kitty.conf)

## Reproducing my tmux configuration in Kitty
I'd changed all the keybindings in tmux to match how I navigate everything else. And since I use vim keybindings in all my editors, I thought it would be nice to keep "HJKL" in use with tmux for navigating between panes and windows. I wanted to navigate between panes by simply pressing `ctrl-[HJKL]` to jump between windows vertically and horizontally, and if I wanted to create a new window, I'd press my tmux prefixer, followed by a directional key to specify where I wanted to add that new split. Kitty as far as I know doesn't have prefix keys like tmux, so I wasn't able to keep that around, but I'm OK with that. Instead, I just added another modifier key. So when I want to create a new pane, just press `ctrl-opt-[HJKL]`
<br>

```
# Create a new window splitting the space used by the existing one so that
# the two windows are placed one above the other
map ctrl+alt+k launch --location=hsplit --cwd=current

# Create a new window splitting the space used by the existing one so that
# the two windows are placed side by side
map ctrl+alt+l launch --location=vsplit --cwd=current

# Rotate the current split, chaging its split axis from vertical to
# horizontal or vice versa
map ctrl+shift+r layout_action rotate

# Move the active window in the indicated direction
map ctrl+shift+h move_window left
map ctrl+shift+l move_window right
map ctrl+shift+k move_window up
map ctrl+shift+j move_window down

# Switch focus to the neighboring window in the indicated direction
map ctrl+h neighboring_window left
map ctrl+l neighboring_window right
map ctrl+k neighboring_window up
map ctrl+j neighboring_window down

# Switch tabs
map ctrl+cmd+l next_tab
map ctrl+cmd+h previous_tab

enabled_layouts splits:split_axis=horizontal
```