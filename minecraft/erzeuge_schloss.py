#!/usr/bin/python
# --------------------------------------
#
#     Minecraft Python API
#        Schloss Bauer
#
# Dieses Skript erzeugt eine Schloss mit Graben und Turm
#
# Autor : Matt Hawkins
# Betragender: Andreas Steffan
#
# Date   : 07/06/2014
#
# http://www.raspberrypi-spy.co.uk/
#
# --------------------------------------

# Import Minecraft libraries
import mcpi.minecraft as minecraft_api
import mcpi.block as block

minecraft = minecraft_api.Minecraft.create()

minecraft.postToChat("Erzeuge ein Schloss!")


# --------------------------------------
# Definiere Funktionen
# --------------------------------------

def erzeuge_waende(groesse, basis_hoehe, hoehe, material, zinnen, gehweg):
    # Erzeuge 4 Waende mit Breite, Hoehe und Material.
    # Zinnen und Gehwege koennen an den Oberkanten hinzufuegt werden.

    minecraft.setBlocks(-groesse, basis_hoehe + 1, -groesse, groesse, basis_hoehe + hoehe, -groesse, material)
    minecraft.setBlocks(-groesse, basis_hoehe + 1, -groesse, -groesse, basis_hoehe + hoehe, groesse, material)
    minecraft.setBlocks(groesse, basis_hoehe + 1, groesse, -groesse, basis_hoehe + hoehe, groesse, material)
    minecraft.setBlocks(groesse, basis_hoehe + 1, groesse, groesse, basis_hoehe + hoehe, -groesse, material)

    # Fuege der Oberkante Zinnen hinzu
    if zinnen == True:
        for x in range(0, (2 * groesse) + 1, 2):
            minecraft.setBlock(groesse, basis_hoehe + hoehe + 1, (x - groesse), material)
            minecraft.setBlock(-groesse, basis_hoehe + hoehe + 1, (x - groesse), material)
            minecraft.setBlock((x - groesse), basis_hoehe + hoehe + 1, groesse, material)
            minecraft.setBlock((x - groesse), basis_hoehe + hoehe + 1, -groesse, material)

    # Fuege Holzwege hinzu
    if gehweg == True:
        minecraft.setBlocks(-groesse + 1, basis_hoehe + hoehe - 1, groesse - 1, groesse - 1, basis_hoehe + hoehe - 1, groesse - 1,
                            block.WOOD_PLANKS)
        minecraft.setBlocks(-groesse + 1, basis_hoehe + hoehe - 1, -groesse + 1, groesse - 1, basis_hoehe + hoehe - 1, -groesse + 1,
                            block.WOOD_PLANKS)
        minecraft.setBlocks(-groesse + 1, basis_hoehe + hoehe - 1, -groesse + 1, -groesse + 1, basis_hoehe + hoehe - 1, groesse - 1,
                            block.WOOD_PLANKS)
        minecraft.setBlocks(groesse - 1, basis_hoehe + hoehe - 1, -groesse + 1, groesse - 1, basis_hoehe + hoehe - 1, groesse - 1,
                            block.WOOD_PLANKS)


def erzeuge_landschaft(graben_breite, graben_tiefe, insel_breite):
    # Mache obere Haelfte Luft
    minecraft.setBlocks(-128, 1, -128, 128, 128, 128, block.AIR)
    # Mache untere Haelfte Dreck mit einer Schicht Gras
    minecraft.setBlocks(-128, -1, -128, 128, -128, 128, block.DIRT)
    minecraft.setBlocks(-128, 0, -128, 128, 0, 128, block.GRASS)
    # Erzeuge Wassergraben
    minecraft.setBlocks(-graben_breite, 0, -graben_breite, graben_breite, -graben_tiefe, graben_breite, block.WATER)
    # Erzeuge Insel und Graben
    minecraft.setBlocks(-insel_breite, 0, -insel_breite, insel_breite, 1, insel_breite, block.GRASS)


def erzeuge_turm(groesse, basis_hoehe, ebenen):
    # Erzeuge einen Turm Anzahl von Ebenen und Dach
    hoehe = (ebenen * 5) + 5

    erzeuge_waende(groesse, basis_hoehe, hoehe, block.STONE_BRICK, True, True)

    # Boden
    for level in range(1, ebenen + 1):
        minecraft.setBlocks(-groesse + 1, (level * 5) + basis_hoehe, -groesse + 1, groesse - 1, (level * 5) + basis_hoehe, groesse - 1,
                            block.WOOD_PLANKS)

    # Fenster
    for level in range(1, ebenen + 1):
        erzeuge_fenster(0, (level * 5) + basis_hoehe + 2, groesse, "N")
        erzeuge_fenster(0, (level * 5) + basis_hoehe + 2, -groesse, "S")
        erzeuge_fenster(-groesse, (level * 5) + basis_hoehe + 2, 0, "W")
        erzeuge_fenster(groesse, (level * 5) + basis_hoehe + 2, 0, "E")

    # Tuer
    minecraft.setBlocks(0, basis_hoehe + 1, groesse, 0, basis_hoehe + 2, groesse, block.AIR)


def erzeuge_fenster(x, y, z, dir):
    if dir == "N" or dir == "S":
        z1 = z
        z2 = z
        x1 = x - 2
        x2 = x + 2

    if dir == "E" or dir == "W":
        z1 = z - 2
        z2 = z + 2
        x1 = x
        x2 = x

    minecraft.setBlocks(x1, y, z1, x1, y + 1, z1, block.AIR)
    minecraft.setBlocks(x2, y, z2, x2, y + 1, z2, block.AIR)

    if dir == "N":
        a = 3
    if dir == "S":
        a = 2
    if dir == "W":
        a = 0
    if dir == "E":
        a = 1

    minecraft.setBlock(x1, y - 1, z1, 109, a)
    minecraft.setBlock(x2, y - 1, z2, 109, a)


# --------------------------------------
#
# Hier geht es los
#
# --------------------------------------

print("Erzeuge Boden und Graben")
erzeuge_landschaft(33, 10, 23)

print("Erzeuge Aussenwaende")
erzeuge_waende(21, 1, 5, block.STONE_BRICK, True, True)

print("Erzeuge Innenwaende")
erzeuge_waende(13, 1, 6, block.STONE_BRICK, True, True)

print("Erzeuge Turm mit 4 Ebenen")
erzeuge_turm(5, 1, 4)

print("Setze Spieler in den Gehweg des Ganges")
minecraft.player.setPos(0, 30, 4)
