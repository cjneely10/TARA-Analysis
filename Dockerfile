FROM continuumio/miniconda3
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get install $(tr '\n' ' ' < packages.txt) -y && \
    pip install -r requirements.txt
ENV PATH /opt/conda/envs/TARA-Analysis/bin:$PATH
USER adminuser
CMD ["streamlit", "run", "TARAVisualize/main.py"]
EXPOSE 8501