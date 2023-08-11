FROM continuumio/miniconda3
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get install $(tr '\n' ' ' < packages.txt) -y && \
    pip install -r requirements.txt \
RUN chown -R adminuser:adminuser /home/adminuser/venv/lib/python3.11/site-packages/TARAVisualize/utils
ENV PATH /opt/conda/envs/TARA-Analysis/bin:$PATH
CMD ["streamlit", "run", "TARAVisualize/main.py"]
EXPOSE 8501
