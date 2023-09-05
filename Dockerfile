
FROM python:3.11
LABEL authors="Daniel Torres"

ENV PYTHONUNBUFFERED 1

# Install Dependencies
COPY src/requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY ./src/ /app/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY VERSION /VERSION

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "180", "app:app"]


