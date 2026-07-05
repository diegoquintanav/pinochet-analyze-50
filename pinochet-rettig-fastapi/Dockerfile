# ---------------------------------------------------------------------------- #
#                            global build arguments                            #
# ---------------------------------------------------------------------------- #

# Global ARG, available to all stages (if renewed)
ARG WORKDIR="/app"

# global username
ARG USERNAME=daniellopez
ARG USER_UID=1000
ARG USER_GID=1000
ARG USER_HOME="/home/${USERNAME}"

# tag used in all images
ARG PYTHON_VERSION=3.10.9

# ---------------------------------------------------------------------------- #
#                                  build stage                                 #
# ---------------------------------------------------------------------------- #

FROM python:${PYTHON_VERSION}-slim AS builder

# Renew args
ARG WORKDIR
ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG USER_HOME

# prepare the $PATH
ENV PATH=${WORKDIR}/.venv/bin:$PATH \
    PYTHONPATH=${WORKDIR} \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# install basic packages
RUN apt-get update && apt-get install -y --no-install-recommends \
	curl iputils-ping netcat \
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

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Copy only the files needed for installing dependencies
COPY --chown=${USER_UID}:${USER_GID} pyproject.toml uv.lock prestart.sh README.md ${WORKDIR}/

# Install dependencies
RUN uv sync --no-dev

# Copy migrations
COPY --chown=${USER_UID}:${USER_GID} alembic.ini ${WORKDIR}/
COPY --chown=${USER_UID}:${USER_GID} alembic ${WORKDIR}/alembic

# Copy the rest of the files
COPY --chown=${USER_UID}:${USER_GID} src ${WORKDIR}/src

# Finalization
RUN uv pip install -e .

USER ${USERNAME}

ENTRYPOINT ["/bin/sh", "-c"]
CMD [ "/app/prestart.sh" ]

EXPOSE 8080
