# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /install
COPY requirements.txt .
# Install dependencies to a specific folder
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: Final Production Image
FROM python:3.11-slim
WORKDIR /app

# Create a non-root user for security [cite: 176]
RUN useradd -m appuser

# Copy only the installed libraries from the builder stage [cite: 190]
COPY --from=builder /install /usr/local
# Copy the application code
COPY app.py .

# Switch to the non-root user [cite: 176]
USER appuser

EXPOSE 5000
CMD ["python", "app.py"]
