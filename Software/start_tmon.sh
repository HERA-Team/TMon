# start up tmon in a screen session so it runs in the background
screen -S TMON -d -m
screen -S TMON -X stuff "/home/obs/TMon/Software/TMon.py^M"
echo "TMon started on session TMON; attach with \"screen -r TMON\"."
