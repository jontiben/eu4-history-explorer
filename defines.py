from PIL import Image

DEFAULT_WIDTH = 1200
DEFAULT_HEIGHT = 800

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