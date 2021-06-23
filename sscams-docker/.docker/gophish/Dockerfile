FROM gophish/gophish

USER root

RUN cd /home  && \
    apt-get update -y && \
	apt-get install -y wget && \
	apt install -y build-essential && \
	apt-get install -y manpages-dev && \
	apt-get install -y git-all && \
    wget https://golang.org/dl/go1.16.3.linux-amd64.tar.gz && \
    rm -rf /usr/local/go && tar -C /usr/local -xzf go1.16.3.linux-amd64.tar.gz


# COPY ../../gophish/mailer/mailer.go /opt/gophish/mailer/mailer.go
# COPY ../../gophish/models/campaign.go /opt/gophish/models/campaign.go
# COPY ../../gophish/controllers/api/camapign.go /opt/gophish/controllers/api/camapign.go
# COPY ../../gophish/worker/worker.go /opt/gophish/worker/worker.go

RUN cd /opt/gophish

# RUN export PATH=$PATH:/usr/local/go/bin
# RUN export PATH=$PATH:/usr/bin

# RUN go build

RUN chmod +x ./docker/run.sh
CMD ["./docker/run.sh"]

#CMD ["bash"]

# docker run -d -it --network gophish_default --name gophishserver -p 3333:3333 -p 8080:8080 -p 8443:8443 -v /Users/nahomymoya/Documents/SSScams/sscams-docker/gophish/mailer::/opt/gophish/mailer -v C:\development\docker\gophish\src\models:/opt/gophish/models gophish bash
# docker run -d -it --network sscams-docker_default  --name gophishserver2 -p 3333:3333 -p 8080:8080 -p 8443:8443 -v /Users/nahomymoya/Documents/SSScams/sscams-docker/gophish/mailer:/opt/gophish/mailer -v /Users/nahomymoya/Documents/SSScams/sscams-docker/gophish/models:/opt/gophish/models -v /Users/nahomymoya/Documents/SSScams/sscams-docker/gophish/controllers/api:/opt/gophish/controllers/api -v /Users/nahomymoya/Documents/SSScams/sscams-docker/gophish/worker:/opt/gophish/worker sscams-docker_gophish bash
# 6543737d6d7876af8
