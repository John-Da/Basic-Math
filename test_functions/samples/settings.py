from gameFile_can_run1 import *

sprites = {}
audioEffect = {}


def load_images():
    path = os.path.join("assets", "images")
    for file in os.listdir(path):
        sprites[file.split('.')[0]] = pygame.image.load(os.path.join(path, file))


def get_sprite(name):
    return sprites[name]


def load_audio():
    path = os.path.join("assets", "audios")
    for file in os.listdir(path):
        audioEffect[file.split('.')[0]] = pygame.mixer.Sound(os.path.join(path, file))


def get_audioEffect(name):
    return audioEffect[name]
