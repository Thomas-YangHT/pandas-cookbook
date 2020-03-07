docker run --name notebook -d -p 8888:8888 \
  -v /root/cookbook:/home/jovyan/cookbook \
  -v /root/cookbook/sudoers:/etc/sudoers \
  -v /root/cookbook/data:/home/jovyan/data \
  jupyter/datascience-notebook
