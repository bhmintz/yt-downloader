import tools

color_font_title = "brwhite"
color_font_square = "brcyan"
color_font_version = "blue"
color_font_dev = "pink"
color_font_x = "brpink"

def title():
    a, b, c, d, e = tools.color(color_font_square, 2), tools.color(color_font_title, 2), tools.color(color_font_version, 2), tools.color(color_font_dev, 2), tools.color(color_font_x, 2)

    tools.Console().print(f"[bold {a}]    ┌────────────────────────────────────┐                                                               [/bold {a}][bold {d}]Dev: BHmint[/bold {d}]")
    tools.Console().print(f"[bold {a}]    │[/bold {a}]      [bold {e}]✗[/bold {e}]    [bold {b}]Youtube Downloader[/bold {b}]    [bold {e}]✗[/bold {e}]      [bold {a}]│                                                               [/bold {a}][bold {c}]Version: {tools.version}[/bold {c}]")
    tools.Console().print(f"[bold {a}]    └────────────────────────────────────┘                                                           [/bold {a}][bold {d}] [/bold {d}]")
    print("")

if __name__ == "__main__":
    pass