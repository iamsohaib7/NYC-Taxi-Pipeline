FROM public.ecr.aws/lambda/python:3.12

RUN pip install boto3>=1.40.18 cryptography>=45.0.6 --target "${LAMBDA_TASK_ROOT}"

WORKDIR ${LAMBDA_TASK_ROOT}
COPY src/ src/
COPY handler.py .

CMD ["handler.handler"]
