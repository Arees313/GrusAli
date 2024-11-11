# Välj en basimage för att köra Python
FROM python:3.11

# Sätt arbetskatalogen i containern
WORKDIR /app

# Kopiera alla filer till arbetskatalogen
COPY . /app

# Installera beroenden
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponera port om nödvändigt (t.ex. för en webbtjänst)
EXPOSE 8000

# Definiera standardkommando för att starta applikationen
CMD ["python", "app.py"]
