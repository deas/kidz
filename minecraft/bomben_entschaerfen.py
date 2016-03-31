#!/usr/bin/python
# --------------------------------------
#
#     Raspberry Pi Minecraft
#     Bomben entschaerfen
#
# Entschaerfe Bomben bevor die Zeit ablaeuft!
#
# Kann Status Meldungen auf einem  PiFace anzeigen
#
# Autor : Matt Hawkins
# Beitragender: Andreas Steffan

# Date   : 09/07/2014
#
# http://www.raspberrypi-spy.co.uk/
#
# --------------------------------------

# Importiere Standard Bibliotheken
import sys
import time
import math
import random as rand

# Importiere Minecraft Bibliotheken
import mcpi.minecraft as minecraft_api
import mcpi.block as block


# Importiere PiFace Bibliothek
# import pifacecad as pf

def sende_nachricht(msg):
    # Sende nachricht an Spiel, PiFace und Kommandozeile
    # cad.lcd.clear()
    msg_one_line = msg.replace('\n', ' ')
    minecraft.postToChat(msg_one_line)
    print(msg_one_line)
    # cad.lcd.write(msg)


def setze_bombe():
    # Setze TNT Block an zufaelligem Ort
    x = rand.randint(-100, 100)
    y = 100
    z = rand.randint(-100, 100)

    # Gehe tiefer, wenn unterer Block Luft oder Wasser ist
    aktueller_block = minecraft.getBlock(x, y - 1, z)
    while aktueller_block == block.AIR.id or aktueller_block == block.WATER_STATIONARY.id:
        y = y - 1
        aktueller_block = minecraft.getBlock(x, y - 1, z)

    # Begrabe unterirdisch (aber nicht im Wasser)
    if minecraft.getBlock(x, y + 1, z) != block.WATER_STATIONARY.id:
        y = rand.randint(y - 3, y - 1)

    # Setze TNT block
    minecraft.setBlock(x, y, z, block.TNT)

    # Gebe timer zurueck
    return [x, y, z, rand.randint(80, 180)]


def entfernung_naechste_bombe():
    # Finde Entfernung zur naechsten Bombe
    spieler_position = minecraft.player.getTilePos()
    mindest_entfernung = 9999
    for bombe in bomben[:]:
        entfernung = math.sqrt((spieler_position.x - bombe[0]) ** 2 + (spieler_position.y - bombe[1]) ** 2 + (spieler_position.z - bombe[2]) ** 2)
        if entfernung < mindest_entfernung:
            mindest_entfernung = entfernung

    return int(mindest_entfernung)


def zeit_bonus_hinzufuegen(bonus_sekunden):
    # Setze Bonus Zeit für alle Timer
    sende_nachricht(str(bonus_sekunden) + " Sekunden Bonus")
    for i in xrange(len(bomben)):
        bomben[i][3] = bomben[i][3] + bonus_sekunden


def bomben_timer_herabsetzen(abzug):
    # Alle countdowns herunterzaehlen
    mindest_zeit = 9999
    for i in xrange(len(bomben)):
        bomben[i][3] = bomben[i][3] - abzug
        if bomben[i][3] < mindest_zeit:
            mindest_zeit = bomben[i][3]
    return mindest_zeit


# --------------------------------------
#
# Hier geht es los
#
# --------------------------------------

minecraft = minecraft_api.Minecraft.create()

# cad = pf.PiFaceCAD()
# cad.lcd.backlight_on()

sende_nachricht("Warte ...")

# Anzahl der Bomben aus Kommandozeile
if len(sys.argv) == 2:
    anzahl_bomben = int(sys.argv[1])
else:
    anzahl_bomben = 3

# Initialisiere Variablen
spiel_an = True
bomben = []

# Erzeuge Bomben
for i in range(0, anzahl_bomben):
    bomben.append(setze_bombe())

sende_nachricht(str(anzahl_bomben) + "\nBomben aktiviert ...")

while anzahl_bomben > 0 and spiel_an:
    # 2 Sekunden warten
    time.sleep(2)

    # Teste welche Bomben noch uebrig sind
    aktuelle_bomben = []
    for bombe in bomben[:]:
        if minecraft.getBlock(bombe[0], bombe[1], bombe[2]) != block.TNT.id:
            zeit_bonus_hinzufuegen(60)
            sende_nachricht("Bombe entschaerft\n" + str(anzahl_bomben - 1) + " uebrig")
        else:
            aktuelle_bomben.append(bombe)
    bomben = aktuelle_bomben

    # Zaehle restliche Bomben
    anzahl_bomben = len(bomben)
    # Entfernung zur naechsten Bombe
    distance = entfernung_naechste_bombe()
    # Aktualisiere Timer
    mindest_zeit = bomben_timer_herabsetzen(2)

    # Zeige Status falls Spiel noch aktiv
    if anzahl_bomben > 0 and mindest_zeit > 0:
        sende_nachricht("Entfernung: " + str(distance) + "m\nZeit: " + str(mindest_zeit))
    elif mindest_zeit <= 0:
        spiel_an = False

# Entweder alle Bomben gefunden oder eine ist explodiert
if spiel_an:
    sende_nachricht("Gratulation!")
else:
    sende_nachricht("**BUMM**\nDu hast versagt!")
