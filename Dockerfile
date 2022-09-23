FROM registry.access.redhat.com/ubi8/ubi-minimal:8.6

RUN microdnf update -y && microdnf install -y python3 python3-pip && microdnf clean all && python3 -m pip install --upgrade pip

COPY requirements.txt .

RUN python3 -m pip install -I --no-cache-dir -r requirements.txt

COPY . ./
RUN python3 -m pip install .

ENTRYPOINT ["promql_tester"]
