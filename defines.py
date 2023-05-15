from PIL import Image

DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 800

VERSION = "1.0a"

USED_TAGS = ["culture", "religion", "controller", "owner", "fake_owner", "original_religion", "original_culture"]
PROVINCE_MAP_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Europa Universalis IV\\map\\provinces.bmp"
PATH_TO_PROVINCE_INFO = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Europa Universalis IV\\history\\provinces"
PROVINCE_MAP = Image.open(PROVINCE_MAP_PATH, 'r')
PROVINCE_MAP_WIDTH = PROVINCE_MAP.size[0]
PROVINCE_MAP_HEIGHT = PROVINCE_MAP.size[1]
RATIO = PROVINCE_MAP_HEIGHT / PROVINCE_MAP_WIDTH
PROVINCE_DEFS_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Europa Universalis IV\\map\\definition.csv"
DEFAULT_MAP_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Europa Universalis IV\\map\\default.map"
CLIMATE_DEFS_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Europa Universalis IV\\map\\climate.txt"
PATH_TO_COUNTRIES_FILE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Europa Universalis IV\\common\\country_tags\\00_countries.txt"
PATH_TO_BACKUP_COUNTRIES_FOLDER = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Europa Universalis IV\\history\\countries"
PATH_TO_COUNTRIES_SOURCE = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Europa Universalis IV\\common\\countries"

C_WASTELAND = (0, 0, 0)
C_OCEAN = (160, 220, 240)
C_WHITE = (255, 255, 255)

HELP_TERMS = ["h", "?", "h", "he", "hel", "help", "??", "???",
"-h", "-?", "-h", "-he", "-hel", "-help", "-??", "-???",
"--h", "--?", "--h", "--he", "--hel", "--help", "--??", "--???",]
HELP_TEXT = f"\nehe - EU4 History Explorer [version {VERSION}]" + """

Usage:    python main.py [file path] <options/flags>    OR (when in PATH)
		  ehe [file path] <options/flags>

Example: ehe "C:\\Users\\username\\Documents\\Paradox Interactive\\Europa Universalis IV\\save games\\Tidore_Tall.eu4" -nd 1444.11.11 1481.1.1 interval=2w
		This renders political mapmodes of the savegame [Tidore_Tall.eu4]
		with no date in the bottom-left at intervals of 2 weeks between
		11 November 1444 and 1 January 1481.

ehe will read an EU4 savefile (ending in .eu4, non-ironman, compressed or
uncompressed) and create maps of the file's history at specified points.
It currently supports the following mapmodes:
	Political (colored according to ingame color)
	Control (randomly assigned map colors)
	Religious (randomly assigned map colors)
	Cultural (randomly assigned map colors)

Flags:
	-nd			Generates map images without the date in the bottom-left

Options:
	mode=		Mapmode (accepts political, control, religious, or
				cultural, default is political)
	interval=	Time interval between maps (default 365 days)
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

github page: https://github.com/jontiben/eu4-history-explorer
read the README.md for additional information.
"""

VALID_MODE_INPUTS = {
	"owner": "owner",
	"ownership": "owner",
	"political": "owner",
	"controller": "controller",
	"control": "controller",
	"culture": "culture",
	"cultural": "culture",
	"religious": "religion",
	"religion": "religion"
}
VALID_MODES = ["owner", "controller", "culture", "religion"]

