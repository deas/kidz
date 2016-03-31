#!/usr/bin/python3
# --------------------------------------
#
#     Minecraft Python API
#         Test Script
#
# Dieses Skript erzeugt einen 3 x 3 Stein Würfel
#
# Autor : Matt Hawkins
# Contributor: Andreas Steffan
#
# http://www.raspberrypi-spy.co.uk/
#
# --------------------------------------

# Importiere Minecraft Bibliothek
import mcpi.minecraft as minecraft_api
import mcpi.block as block

minecraft = minecraft_api.Minecraft.create()

# Position des Spielers ermitteln
spieler_position = minecraft.player.getTilePos()

# Nachricht versenden
minecraft.postToChat("Teste Würfel und Spieler Position!")

# Verändere Block
print("Erzeuge 3 x 3 Würfel aus Stein")
minecraft.setBlocks(spieler_position.x - 1, spieler_position.y, spieler_position.z - 1, spieler_position.x + 1, spieler_position.y + 2, spieler_position.z + 1, block.STONE)

print("Position des Spielers um drei Blöcke verändern")
minecraft.player.setPos(spieler_position.x, spieler_position.y + 3, spieler_position.z)

minecraft.postToChat("Bewege und lasse nochmal laufen.")
