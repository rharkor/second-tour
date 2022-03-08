<<<<<<< HEAD
#!/bin/bash
service nginx start
sh && cd /app/website/secondtour_website/ && uwsgi website.ini
=======
#!/bin/sh
service nginx start && sleep 10 && cd /app/website/secondtour_website && uwsgi /app/website/secondtour_website/website.ini
>>>>>>> e622058f3d06495f28c060a037fa123d84e6ea00
