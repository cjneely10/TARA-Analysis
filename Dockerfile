FROM continuumio/miniconda3
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get install $(tr '\n' ' ' < packages.txt) -y
ENV PATH /opt/conda/envs/TARA-Analysis/bin:$PATH
USER appuser
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "TARAVisualize/main.py"]
EXPOSE 8501