docker rm bokeh -f 
docker run --name bokeh -d -p 5006:5006 \
  -v /root/cookbook:/home/jovyan/cookbook \
  -v /root/cookbook/sudoers:/etc/sudoers \
  -v /root/cookbook/data:/home/jovyan/data \
  jupyter/datascience-notebook sh /home/jovyan/cookbook/startbokeh.sh
