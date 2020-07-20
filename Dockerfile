FROM pypy:3.6-buster	

RUN apt-get update && \	
    apt-get install -y \
		make \
		libopus0 \
		ffmpeg \
		libsodium23 \
		git \
		atomicparsley \
		aria2

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt 

RUN useradd --create-home appuser

WORKDIR /home/appuser

USER appuser

COPY . .

CMD ["pypy3", "./main.py"]
