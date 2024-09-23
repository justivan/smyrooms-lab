FROM jupyter/datascience-notebook:lab-4.0.7

USER root

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends libpq-dev binutils libproj-dev gdal-bin cron

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

USER jovyan

RUN mkdir -p /home/jovyan/.jupyter/lab/user-settings/@jupyterlab/apputils-extension/
COPY themes.jupyterlab-settings /home/jovyan/.jupyter/lab/user-settings/@jupyterlab/apputils-extension/