FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY README.md .
COPY src ./src

RUN pip install --no-cache-dir .

ENV HOST=0.0.0.0
ENV PORT=8055
ENV TRANSPORT=sse

EXPOSE 8055

CMD ["perplexity-mcp"]