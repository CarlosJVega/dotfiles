# Qtile Config File
# http://www.qtile.org/
import os
import json
from libqtile import hook
from libqtile import bar, layout, widget, extension 
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import subprocess



#-------------------------------------------------------------------------------------------------------------------
#--------------------------------------Colors-----------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

def load_theme():
    theme = 'nord-wave'
    home  = os.path.expanduser('~')
    qtile = os.path.join(home, '.config/qtile/')
    config = os.path.join(qtile, "config.json")
    
    if os.path.isfile(config):
        with open(config) as f:
            theme = json.load(f)["theme"]
    else:
        with open(config, "w") as f:
            f.write(f'{{"theme": "{theme}"}}\n')

    theme_file = os.path.join(qtile, "themes", f'{theme}.json')
    if not os.path.isfile(theme_file):
        raise Exception(f'"{theme_file}" does not exist')

    with open(os.path.join(theme_file)) as f:
        return json.load(f)

colors = load_theme()


#-------------------------------------------------------------------------------------------------------------------
#--------------------------------------Keys-------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
mod = "mod4"

teams = "chromium --app=https://teams.office.com"

keys = [Key(key[0], key[1], *key[2:]) for key in [
    # ------------ Window Configs ------------
    # Switch between windows in current stack pane
    ([mod], "Down", lazy.layout.down()),
    ([mod], "Up", lazy.layout.up()),
    ([mod], "Left", lazy.layout.left()),
    ([mod], "Right", lazy.layout.right()),
    # Toggle floating
    ([mod, "shift"], "f", lazy.window.toggle_floating()),
    # Move windows up or down in current stack
    ([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    ([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    # Toggle between different layouts as defined below
    ([mod], "Tab", lazy.next_layout()),
    ([mod, "shift"], "Tab", lazy.prev_layout()),
    # Kill window
    ([mod], "w", lazy.window.kill()),
    # Switch focus of monitors
    ([mod], "period", lazy.next_screen()),
    ([mod], "comma", lazy.prev_screen()),
    # Restart Qtile
    ([mod, "control"], "r", lazy.restart()),
    # Quit qtile
    ([mod, "control"], "q", lazy.shutdown()),
    # Run 
    ([mod], "r", lazy.spawncmd()),

    # ------------ App Configs ------------
        # Browser
    ([mod], "t", lazy.spawn(teams)),
    # Browser
    ([mod], "f", lazy.spawn("firefox")),
    # File Explorer
    ([mod], "e", lazy.spawn("nautilus")),
    # Terminal
    ([mod], "Return", lazy.spawn("kitty")),
    # Redshift
    ([mod], "r", lazy.spawn("redshift -O 2400")),
    ([mod, "shift"], "r", lazy.spawn("redshift -x")),
    # Screenshot
    ([mod], "s", lazy.spawn("scrot")),
    ([mod, "shift"], "s", lazy.spawn("scrot -s")),
    # ------------ Hardware Configs ------------
    # Volume
    ([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    ([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    ([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),
    # Brightness
    ([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    ([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
]]

#-------------------------------------------------------------------------------------------------------------------
#--------------------------------------Groups-----------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

groups = [Group(i) for i in [
    " 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 ", " 8 ", " 9 ",
]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

#-------------------------------------------------------------------------------------------------------------------
#----------------------------------Layouts and layout rules---------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

layout_conf = {
    'border_focus': colors['focus'][0],
    'border_width': 1,
    'margin': 4
}

layouts = [
    layout.Max(),
    layout.MonadTall(**layout_conf),
    layout.MonadWide(**layout_conf),
    #layout.Bsp(**layout_conf),
    #layout.Matrix(columns=2, **layout_conf),
    #layout.RatioTile(**layout_conf),
    # layout.Columns(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),
        Match(wm_class='makebranch'),
        Match(wm_class='maketag'),
        Match(wm_class='ssh-askpass'),
        Match(title='branchdialog'),
        Match(title='pinentry'),
    ],
    border_focus=colors["color4"][0])

#-------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------Mouse------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position()
    ),
    Drag(
        [mod],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

#-------------------------------------------------------------------------------------------------------------------
#------------------------------------------------Screens------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

widget_defaults = dict(
    font="Hack Nerd Font",
    fontsize=20,
    padding=5,
)
extension_defaults = widget_defaults.copy()

def init_screens():
    return [Screen(
        #bottom=bar.Gap(size=2),
        bottom=bar.Bar(
            [
                widget.CurrentLayoutIcon(),
                #widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.TextBox(text='  '),
                widget.QuickExit( default_text=' '),
            ],
            30,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        top=bar.Gap(size=40),)]

screens= init_screens()

#-------------------------------------------------------------------------------------------------------------------
#-----------------------------------------Main Parameters-----------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------


main = None
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
auto_fullscreen = True
focus_on_window_activation = "smart"
wmname = 'qtile'

autostart = [
    #"setxkbmap es",
    #"~/.config/polybar/launch.sh &",
    "feh --bg-fill -r -z ~/Desktop/castv/wallpapers",
    "picom --no-vsync &",
    #"~/.config/polybar/launch.sh $",
    #"cbatticon -u 5 &",
    #"volumeicon &"
    ]

for x in autostart:
    os.system(x)






