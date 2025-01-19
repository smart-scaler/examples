To install
bash install-demo.sh

To uninstall
bash uninstall-demo.sh

To change load function
change value on demo_setup/chart-acme/templates/smartscaler-load-gen.yaml:32 to either sinusoidal.
change value on demo_setup/chart-boutique/templates/loadgenerator.yaml:29 to either sinusoidal.py, heartbeat.py