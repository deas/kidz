#!/usr/bin/python3
# --------------------------------------
#
#     Minecraft Python API
#        Was ist das?
#
# Dieses Skript zeigt den Block unter dem
# Spieler an
#
# Autor : Matt Hawkins
# Betragender: Andreas Steffan
#
# Date   : 08/06/2014
#
# http://www.raspberrypi-spy.co.uk/
#
# --------------------------------------

# Importiere Minecraft Bibliotheken
import mcpi.minecraft as minecraft_api
import mcpi.block as block

minecraft = minecraft_api.Minecraft.create()

# Position des Spielers ermitteln
spieler_position = minecraft.player.getTilePos()

# Block unter dem Spieler holen
block_unter_spieler = minecraft.getBlockWithData(spieler_position.x, spieler_position.y - 1, spieler_position.z)

# Nachricht anzeigen
minecraft.postToChat("Du stehst vor Block ID : {} Daten : {}".format(block_unter_spieler.id, block_unter_spieler.data))
