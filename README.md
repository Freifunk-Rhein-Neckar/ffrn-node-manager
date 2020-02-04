# FFRN: Node-Manager

Bei dem Node-Manager des FFRN handelt es sich um die Software welche unter 
[register.freifunk-rhein-neckar.de](https://register.freifunk-rhein-neckar.de/) zur Verfügung steht. 
Sie wird genutzt um die Knoten zu registrieren und so die fastd Keys zu erfassen.

## Installation

### Abhängigkeiten:
* python3
* python3-venv (*)
* supervisor (*)

\* falls so wie hier beschrieben konfiguriert

### virtual enviroment (venv) aufsetzen
Die Idee ist es alle in der `requirements.txt` gennanten Abhängigkeiten in ein 
virtual environments zu installieren. Dafür muss dieses erstellt und die Pakete
in diesem installiert werden:

```bash
python3 -m venv venv                # venv erstellen
source venv/bin/activate            # venv aktivieren
pip install -r requirements.txt     # Abhängigkeiten installieren
deactivate                          # venv wieder verlassen
```

### autostart mit supervisor einrichten

Als erstes `supervisor` installieren, dann die folgende Datei in beispielsweise 
`/etc/supervisor/conf.d/ffrn-node-manager.conf` anlegen:

Es sollte am besten ein komplett unpriviligierter Benutzer erstellt werden unter
dem gunicorn laufen kann. 

```
[program:ffrn-node-manager]
command = /opt/ffrn-node-manager/venv/bin/gunicorn backend:app -b 127.0.0.1:8432
directory = /opt/ffrn-node-manager/
user=ffrn-node-manager
autostart=true
autorestart=true
```

Nun noch `supervisor` die Konfigruation einlesen lassen:
```bash
supervisorctl reread
supervisorctl update
supervisorctl status ffrn-node-manager
```

Das sollte es gewesen sein. Auf Port 127.0.0.1:8432 sollte nun der Node-Manager
laufen.

### nginx proxy einrichten
Nun noch einen Proxy einrichten damit ein Zugriff von außen möglich ist.


## Update
Eventuell könnte das folgende (ungetestete) funktionieren:
```bash
cd /opt/ffrn-node-manager/
source venv/bin/activate
pip install --upgrade -r requirements.txt
deactivate
```
Ein Export der aktuellen Versionen kann dann mittels `pip freeze` erfolgen.
