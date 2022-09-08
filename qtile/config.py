# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, DropDown, Group, KeyChord, Key, Match, ScratchPad, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import Callable, List  # noqa: F401from typing import List  # noqa: F401
from libqtile.extension.window_list import WindowList
from libqtile.extension.command_set import CommandSet
# import layout objects
from libqtile.layout.columns import Columns
from libqtile.layout.xmonad import MonadTall, MonadWide
from libqtile.layout.stack import Stack
from libqtile.layout.floating import Floating


mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"      # My terminal of choice
myBrowser = "librewolf" # My browser of choice
myCalendar = "when"

keys = [
         ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([mod], "d",
             lazy.spawn("rofi -show drun -show-icons"),
             desc='Run Launcher'
             ),
         Key([mod, "mod1"], "q",
             lazy.spawn(myBrowser),
             desc='Qutebrowser'
             ),
         Key([mod], "space",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod], "q",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         Key([mod], "e",
             lazy.spawn("pcmanfm -n"),
             desc='File Manager'
             ),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Window controls
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "shift"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
          Key([mod], "Tab",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
]

groups = [Group("", layout='monadtall'),
          Group("", layout='monadtall'),
          Group("", matches=[Match(wm_class="zoom")], layout="stack"),
          Group("一", layout='monadtall'),
          Group("二", layout='monadtall'),
          Group("三", layout='monadtall'),
          Group("四", layout='monadtall'),
          Group("五", layout='monadtall'),
          Group("六", layout='monadtall')]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {"border_width": 3,
                "margin": 8,
                "border_focus": "d65d08",
                "border_normal": "282828"
                }

# Append scratchpad with dropdowns to groups
groups.append(ScratchPad('scratchpad', [
    DropDown('term', myTerm, width=0.4, height=0.5, x=0.3, y=0.1, opacity=1),
    DropDown('mixer', 'pavucontrol', width=0.4, height=0.6, x=0.3, y=0.1, opacity=1),
    DropDown('when', 'alacritty when', x=0.3, y=0.1, opacity=1),
    DropDown('bitwarden', 'bitwarden-desktop', width=0.4, height=0.6, x=0.3, y=0.1, opacity=1),
]))
# extend keys list with keybinding for scratchpad
keys.extend([
    Key(["control"], "1", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key(["control"], "2", lazy.group['scratchpad'].dropdown_toggle('mixer')),
    Key(["control"], "3", lazy.group['scratchpad'].dropdown_toggle('when')),
    Key(["control"], "4", lazy.group['scratchpad'].dropdown_toggle('bitwarden')),
])

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.Floating(**layout_theme)
]

colors = [["#282828", "#282828"], # Black
          ["#d79921", "#d79921"], # Yellow
          ["#ebdbb2", "#ebdbb2"], # White
          ["#fb4934", "#fb4934"], # Red
          ["#98971a", "#98971a"], # Green
          ["#d65d0e", "#d65d0e"], # Orange
          ["#458588", "#458588"], # Blue
          ["#b16286", "#b16286"], # Purple
          ["#689d6a", "#689d6a"], # Aqua
          ["#928374", "#928374"]] # Gray

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="JetBrains Mono Nerd Font",
    fontsize = 16,
    padding = 0,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Image(
                       filename = "~/.config/qtile/icons/tux-white.png",
                       scale = "True",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("sh /home/dave/.config/rofi/launchers/colorful/launcher.sh")},
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.GroupBox(
                       font = "JetBrains Mono Nerd Font Bold",
                       fontsize = 18,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[3],
                       inactive = colors[2],
                       rounded = False,
                       highlight_color = colors[0],
                       highlight_method = "line",
                       this_current_screen_border = colors[6],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.TextBox(
                       text = '|',
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 18
                       ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[2],
                       background = colors[0],
                       padding = 0,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = colors[2],
                       background = colors[0],
                       padding = 5
                       ),
             widget.TextBox(
                       text = '|',
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 18
                       ),
              widget.WindowName(
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0
                       ),
              widget.Spacer(
                      background = colors[0]
                       ),
              widget.TextBox(
                       text = ' ',
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = colors[8],
                       padding = 2,
                       fontsize = 18
                       ),
              widget.Clock(
                       foreground = colors[2],
                       background = colors[0],
                       format = "%A, %B %d - %I:%M %p ",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e calcurse')},
                       padding = 5,
                       ),
              widget.Spacer(
                      background = colors[0]
                       ),
             widget.TextBox(
                       text = '',
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = '474747',
                       padding = 0,
                       fontsize = 85
                       ),
              widget.TextBox(
                       text = ' ﯱ',
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = colors[8],
                       padding = 0,
                       fontsize = 18,
                       ),
              widget.Net(
                       background = colors[0],
                       foreground = colors[2],
                       samples = 60,
                       prefix='M',
                       ),
             widget.TextBox(
                       text = '',
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 85
                       ),
              widget.TextBox(
                       text = ' ',
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = colors[8],
                       padding = 0,
                       fontsize = 18
                       ),
              widget.CPU(
                       background = colors[0],
                       foreground = colors[2],
                       samples = 60,
                       ),
             widget.TextBox(
                       text = '',
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 85
                       ),
              widget.TextBox(
                       text = ' ',
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = colors[8],
                       padding = 0,
                       fontsize = 18
                       ),
              widget.Memory(
                       background = colors[0],
                       foreground = colors[2],
                       measure_mem='G',
                       ),
             widget.TextBox(
                       text = '',
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 85
                       ),
              widget.TextBox(
                       text=' ',
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = colors[8],
                       padding = 0,
                       fontsize = 18
                       ),
              widget.CheckUpdates(
                       update_interval = 60,
                       distro = "Arch",
                       display_format = "Updates: {updates} ",
                       no_update_string='No updates',
                       foreground = colors[2],
                       colour_have_updates = colors[3],
                       colour_no_updates = colors[2],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu && paru -Syu')},
                       padding = 5,
                       background = colors[0],
                       ),
             widget.TextBox(
                       text = '',
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 85
                       ),
              widget.TextBox(
                       text = ' ',
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = colors[8],
                       padding = 0,
                       fontsize = 18
                       ),
              widget.PulseVolume(
                       foreground = colors[2],
                       background = colors[0],
                       fmt = 'Vol: {}',
                       padding = 5
                       ),
             widget.TextBox(
                       text = '',
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 85
                       ),
              widget.Systray(
                       background = colors[0],
                       padding = 5
                       ),
             widget.TextBox(
                       text = '|',
                       font = "JetBrains Mono Nerd Font",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 18,
                       ),
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[28:32]               # Slicing removes unwanted widgets (systray) on Monitors 2
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_widgets_screen3():
    widgets_screen3 = init_widgets_list()
    del widgets_screen3[10:32]               # Slicing removes unwanted widgets on Monitors 3
    return widgets_screen3                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=25)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=25)),
            Screen(top=bar.Bar(widgets=init_widgets_screen3(), opacity=1.0, size=25))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()
    widgets_screen3 = init_widgets_screen3()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

#dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    subprocess.call(['/home/dave/.config/qtile/scripts/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
