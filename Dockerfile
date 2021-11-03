# Set base image with Python 3.8.2
FROM python:3.8.2

# Label with contact information from maintainers
LABEL MAINTAINER Ana Jaime <anamaria.jaimerivera@student.uts.edu.au>, Javiera de la Carrera <javiera.delacarreragarcia@student.uts.edu.au>, Felipe Monroy <felipe.monroy@student.uts.edu.au>

# Set app name as env variable
ENV APP data_explorer_tool

# Create app directory inside the container
WORKDIR /app

# Copy app dependencies file into the container
COPY requirements.txt .

# Install app dependencies inside the container
RUN pip install --upgrade pip -r requirements.txt

# Copy app files into the container
COPY . /app

# Launch streamlit application
CMD ["streamlit", "run", "app.py"]
