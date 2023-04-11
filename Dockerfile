FROM python:3.11-alpine as production
LABEL maintainer="RomanKaiser(KaiserProger) <kaisergrobe@gmail.com>" \
      description="RLT test task bot"

EXPOSE 80

COPY ./requirements /requirements
COPY .env ./.env
COPY ./app /app
RUN pip install -r /requirements/base.txt

CMD python3 -m app
