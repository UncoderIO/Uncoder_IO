FROM python:3.9-alpine
RUN apk add --update --no-cache linux-headers build-base python3-dev libffi-dev
WORKDIR /siem_converter
COPY . .
RUN pip install --upgrade pip && \
    python -m pip install --upgrade setuptools && \
    pip install --trusted-host=pypi.python.org --trusted-host=pypi.org --trusted-host=files.pythonhosted.org --no-cache-dir -Ur requirements/requirements_prod.txt
EXPOSE 8000
CMD ["python", "server.py"]
