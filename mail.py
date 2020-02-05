# -*- coding: utf-8 -*-
from email.mime.text import MIMEText

def getMail(node):
    msg = MIMEText('''Hey {nickname},

Du hast gerade einen neuen Knoten für das Netz von Freifunk Rhein-Neckar registriert - cool!

Die Daten deines Knotens lauten:

    Hostname:       {hostname}
    MAC:            {mac}
    VPN Key:        {key}
    Nick:           {nickname}
    Mail:           {email}
    Token:          {token}

Bitte halte diese Daten aktuell. Du kannst sie unter [1] mit deinem Token pflegen.

Wir hoffen, dass Du gut zurecht gekommen bist und würden uns freuen, wenn Du dich auch persönlich in die Community einbringen würdest. Vielleicht kannst Du ja sogar noch weitere Leute von unserem Projekt überzeugen.

Solltest Du Probleme oder Anregungen haben, kannst Du die Community am besten über unser Forum [2] erreichen. Es gibt aber auch andere Kontaktmöglichkeiten [3].

Viele Grüße,
Freifunk Rhein-Neckar

[1] https://register.freifunk-rhein-neckar.de/
[2] https://forum.ffrn.de/
[3] https://www.freifunk-rhein-neckar.de/kontakt.html

'''.format(**node))

    msg['Subject'] = "Dein Freifunk Knoten"
    return msg
