FROM continuumio/miniconda3
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install libgl1-mesa-glx -y && \
    conda env create -f environment.yml && \
    echo "source activate TARA-Analysis" > ~/.bashrc
ENV PATH /opt/conda/envs/TARA-Analysis/bin:$PATH
CMD ["streamlit", "run", "TARAVisualize/main.py"]
EXPOSE 8501
