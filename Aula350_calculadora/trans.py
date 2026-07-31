from PIL import Image
from pathlib import Path

ROOT_DIR = Path(__file__).parent
FILES_DIR = ROOT_DIR / 'files'
FILES_DIR.mkdir(exist_ok=True)  # cria a pasta se não existir

WINDOW_ICON_PATH = FILES_DIR / 'ICON.png'

# Abre o PNG
img = Image.open(WINDOW_ICON_PATH)

# Converte para ICO (tamanho 256x256 é recomendado)
ICO_PATH = FILES_DIR / 'ICON.ico'
img.save("ICON.ico", sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])

from PIL import Image

