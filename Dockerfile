FROM python:3.9

# Set the working directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Create a non-root user for Hugging Face
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Copy the 'app' folder and the 'main.py'
WORKDIR $HOME/app
COPY --chown=user . $HOME/app

# Expose the mandatory port for HF
EXPOSE 7860

# Run main.py from the root of the copy
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]