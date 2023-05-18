### ehe - EU4 History Explorer [version 1.0a]

![image](https://github.com/jontiben/eu4-history-explorer/assets/25780026/4e65acc9-790a-4a62-8ccb-9cb50c49caa1)

![image](https://github.com/jontiben/eu4-history-explorer/assets/25780026/90b6f448-aa12-441d-bb72-b9e59a3cab90)

Usage:    `python main.py [file path] <options/flags>` OR (when built and installed in PATH) `ehe [file path] <options/flags>`

Example: `ehe "C:\Users\user name\Documents\Paradox Interactive\Europa Universalis IV\save games\Tidore_Tall.eu4" -nd 1444.11.11 1481.1.1 interval=2w`

(This renders political mapmodes of the savegame [Tidore_Tall.eu4] with no date in the bottom-left at intervals of 2 weeks between 11 November 1444 and 1 January 1481.)

ehe will read an EU4 savefile (ending in .eu4, non-ironman, compressed or uncompressed) and create maps of the file's history at specified points.
It currently supports the following mapmodes:
- Political (colored according to ingame color)
- Control (colored according to ingame color)
- Combined (colored according to ingame color, combination of political and control)
- Religious (randomly assigned map colors)
- Cultural (randomly assigned map colors)

Flags:

        -nd                     Generates map images without the date in the bottom-left

Options:

        mode=           Mapmode (accepts political, control, combined, religious, or
                                cultural, default is political)
        interval=       Time interval between maps (default 365 days)
                                Give it a number followed by, optionally, an interval
                                size: w or week for 7 days, m or month for 30, and y
                                or year for 365. If no interval size is given it will
                                default to days. the argument "35" will be interpreted
                                as "35 days," the argument "6m" will be interpreted as
                                180 days, "2year" will be interpreted as "730 days," etc.

        If you give it a date formatted YYYY.M(M).D(D) (e.g 1444.11.11) then
        it will render a single map at that date. Without a date it will
        default to the savefile's current date. If you give it two, it will
        render every map at [interval] between those two dates.

Maps are saved to the directory `saved_maps`.

Running either `mp4maker.py` or `gifmaker.py` will generate an mp4 or gif video out of every image in the `saved_maps` directory and save it to `saved_videos`. They currently take no arguments in the command-line, they'll be made nicer to work with soon. I'm additionally planning to add more graceful error messaging, at the moment an incorrectly formatted command will give you a python error.

Run ehe with no arguments, or with an argument that seems like it should generate a help page to see a help page.

The ehe is developed under the MIT license. It's written entirely in Python, using PIL for image generation and imageio for video generation.
