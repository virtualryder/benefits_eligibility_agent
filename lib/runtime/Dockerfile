# P0-8 supply-chain: pin the base image by DIGEST (not the mutable :3.12-slim tag) and run as a
# non-root user. The digest is python:3.12-slim resolved 2026-09-08; re-resolve on a deliberate
# base bump. Bumped 2026-09-08: trivy - running for the first time after its action pin was
# fixed - reported 30 FIXABLE HIGH/CRITICAL Debian advisories against the 2026-07 digest and 0
# in the Python packages. A digest pin freezes the OS packages too, so it accrues every
# advisory published after it; tests/test_base_image_freshness.py now fails once this date is
# more than 90 days old. The digest below was READ from the Security workflow's own resolve
# step on a GitHub runner - the agent proxy blocks public.ecr.aws and the dev machine has no
# container client, so inventing one would have been a fabricated supply-chain pin.
FROM public.ecr.aws/docker/library/python:3.12-slim@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea

WORKDIR /app

# non-root runtime user (P0-8): create an unprivileged user up front and drop to it before CMD.
RUN groupadd -r app && useradd -r -g app -u 10001 app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app agent.py .
ENV PYTHONUNBUFFERED=1

USER 10001
CMD ["opentelemetry-instrument", "python", "-u", "agent.py"]
