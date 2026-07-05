# ---------------------------------------------------------------------------- #
#                            global build arguments                            #
# ---------------------------------------------------------------------------- #

ARG WORKDIR="/app"
ARG USERNAME=dbt_user
ARG USER_UID=1000
ARG USER_GID=1000
ARG USER_HOME="/home/${USERNAME}"
ARG PYTHON_VERSION=3.13
ARG UV_VERSION=0.11.26

# ---------------------------------------------------------------------------- #
#                                  uv stage                                    #
# ---------------------------------------------------------------------------- #

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

# ---------------------------------------------------------------------------- #
#                                  build stage                                 #
# ---------------------------------------------------------------------------- #

FROM python:${PYTHON_VERSION}-slim AS builder

ARG WORKDIR
ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG USER_HOME

# Install uv
COPY --from=uv /uv /uvx /bin/

# prepare the $PATH
ENV PATH=/opt/venv/bin:$PATH \
    PYTHONPATH=${WORKDIR} \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv

# install basic packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl iputils-ping netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------ add user ----------------------------- #

RUN groupadd --gid $USER_GID "${USERNAME}" \
    && useradd --uid $USER_UID --gid $USER_GID -m "${USERNAME}"

RUN mkdir -p ${USER_HOME} \
    && chown ${USER_UID}:${USER_GID} ${USER_HOME}

RUN mkdir -p ${WORKDIR} \
    && chown ${USER_UID}:${USER_GID} ${WORKDIR}

# ---------------------------- add code specifics ---------------------------- #

WORKDIR ${WORKDIR}

# make sure the user owns /app
RUN chown -R ${USER_UID}:${USER_GID} ${WORKDIR}

# Create venv directory ahead of time so uv creates files with correct ownership
RUN mkdir -p /opt/venv && chown -R ${USER_UID}:${USER_GID} /opt/venv

# Install dependencies into a temporary layer for caching
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy the rest of the files
COPY --chown=${USER_UID}:${USER_GID} . ${WORKDIR}/

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Make sure app user owns the venv
RUN chown -R ${USER_UID}:${USER_GID} /opt/venv

# Switch to app user for runtime
USER ${USERNAME}

LABEL org.opencontainers.image.title="pinochet-rettig-dbt" \
      org.opencontainers.image.description="dbt project for the Pinochet-Rettig dataset" \
      org.opencontainers.image.source="https://github.com/diegoquintanav/pinochet-analyze-50" \
      org.opencontainers.image.licenses="MIT"

ENTRYPOINT ["dbt"]
CMD ["ls"]

EXPOSE 8089
