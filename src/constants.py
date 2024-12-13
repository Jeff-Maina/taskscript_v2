from InquirerPy.base.control import Choice


themes = [
    Choice(value="default", name="Default"),
    Choice(value="dark", name="Dark"),
    Choice(value="dracula", name="Dracula"),
    Choice(value="gruvbox", name="Gruvbox"),
    Choice(value="nord", name="Nord"),
    Choice(value="oceanic-next", name="Oceanic Next"),
    Choice(value="solarized", name="Solarized"),
]

pointer_options = [
    Choice(name=" ▶", value=" ▶"),
    Choice(name=" →", value=" →"),
    Choice(name=" ➤", value=" ➤"),
    Choice(name=" ⟿", value=" ⟿"),
    Choice(name=" =>", value=" =>"),
    Choice(name=" >", value=" >"),
    Choice(name=" -->", value=" -->")
]


priority_options = [
    Choice(name="High", value=1),
    Choice(name="Normal", value=2),
    Choice(name="Low", value=3)
]