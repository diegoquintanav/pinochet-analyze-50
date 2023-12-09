# ---------------------------------------------------------------------------- #
#                            global build arguments                            #
# ---------------------------------------------------------------------------- #

# Global ARG, available to all stages (if renewed)
ARG WORKDIR="/app"

# global username
ARG USERNAME=dbt_user
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


# Poetry version
ARG POETRY_VERSION=1.7.1

# Pipx version
ARG PIPX_VERSION=1.2.1

# prepare the $PATH
ENV PATH=/opt/pipx/bin:${WORKDIR}/.venv/bin:$PATH \
    PIPX_BIN_DIR=/opt/pipx/bin \
    PIPX_HOME=/opt/pipx/home \
    PIPX_VERSION=$PIPX_VERSION \
    POETRY_VERSION=$POETRY_VERSION \
    PYTHONPATH=${WORKDIR} \
    # Don't buffer `stdout`
    PYTHONUNBUFFERED=1 \
    # Don't create `.pyc` files:
    PYTHONDONTWRITEBYTECODE=1 \
    # make poetry create a .venv folder in the project
    POETRY_VIRTUALENVS_IN_PROJECT=true

# ------------------------------ add user ----------------------------- #

RUN groupadd --gid $USER_GID "${USERNAME}" \
    && useradd --uid $USER_UID --gid $USER_GID -m "${USERNAME}"

RUN mkdir -p ${USER_HOME} \
    && chown ${USER_UID}:${USER_GID} ${USER_HOME}

RUN mkdir -p ${WORKDIR} \
    && chown ${USER_UID}:${USER_GID} ${WORKDIR}

# -------------------------- add python dependencies ------------------------- #

# Install Pipx using pip
RUN python -m pip install --no-cache-dir --upgrade pip pipx==${PIPX_VERSION}
RUN pipx ensurepath && pipx --version

# Install Poetry using pipx
RUN pipx install --force poetry==${POETRY_VERSION}

# ---------------------------- add code specifics ---------------------------- #

# Copy everything to the container, we filter out what we don't need using .dockerignore
WORKDIR ${WORKDIR}

# make sure the user owns /src
RUN chown -R ${USER_UID}:${USER_GID} ${WORKDIR}

# Copy only the files needed for installing dependencies
COPY --chown=${USER_UID}:${USER_GID} pyproject.toml poetry.lock ${WORKDIR}/

# Install dependencies
RUN poetry install --no-root


# ---------------------------------------------------------------------------- #
#                                  final layer                                 #
# ---------------------------------------------------------------------------- #

FROM python:${PYTHON_VERSION}-slim AS final

# Renew args
ARG WORKDIR
ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG USER_HOME

# prepare the $PATH
ENV PATH=${WORKDIR}/.venv/bin:$PATH \
    PYTHONPATH=${WORKDIR} \
    # Don't buffer `stdout`
    PYTHONUNBUFFERED=1 \
    # Don't create `.pyc` files:
    PYTHONDONTWRITEBYTECODE=1

# copy the user from the builder stage
RUN groupadd --gid $USER_GID "${USERNAME}" \
    && useradd --uid $USER_UID --gid $USER_GID -m "${USERNAME}"

RUN mkdir -p ${USER_HOME} \
    && chown ${USER_UID}:${USER_GID} ${USER_HOME}

RUN mkdir -p ${WORKDIR} \
    && chown ${USER_UID}:${USER_GID} ${WORKDIR}

# copy the virtual environment from the builder stage
COPY --from=builder --chown=${USER_UID}:${USER_GID} ${WORKDIR}/.venv ${WORKDIR}/.venv

# set the working directory
WORKDIR ${WORKDIR}

# make user non-root
USER ${USERNAME}

ENTRYPOINT ["dbt"]
CMD [ "ls" ]

EXPOSE 8089