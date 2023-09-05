# ---------------------------------------------------------------------------- #
#                            global build arguments                            #
# ---------------------------------------------------------------------------- #

# Global ARG, available to all stages (if renewed)
ARG WORKDIR="/src"

# global username
ARG USERNAME=daniellopez
ARG USER_UID=1000
ARG USER_GID=1000
ARG USER_HOME=/home/${USERNAME}

# tag used in all images
ARG PYTHON_VERSION=3.10.5

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
ENV PATH=${USER_HOME}/.venv/bin:$PATH \
	PYTHONPATH=${WORKDIR} \
	# Don't buffer `stdout`
	PYTHONUNBUFFERED=1 \
	# Don't create `.pyc` files:
	PYTHONDONTWRITEBYTECODE=1

# ------------------------------ add user ----------------------------- #

RUN groupadd --gid $USER_GID "${USERNAME}" \
	&& useradd --uid $USER_UID --gid $USER_GID -m "${USERNAME}"

RUN mkdir -p ${USER_HOME} \
	&& chown ${USER_UID}:${USER_GID} ${USER_HOME}

RUN mkdir -p ${WORKDIR} \
	&& chown ${USER_UID}:${USER_GID} ${WORKDIR}

# ---------------------------- add code specifics ---------------------------- #

# Copy everything to the container, we filter out what we don't need using .dockerignore
WORKDIR ${WORKDIR}

# make sure the user owns /src
RUN chown -R ${USER_UID}:${USER_GID} ${WORKDIR}

RUN python -m venv ${USER_HOME}/.venv

# Copy only the files needed for installing dependencies
COPY --chown=${USER_UID}:${USER_GID} requirements.txt ${WORKDIR}/

# Install dependencies
RUN pip install --upgrade pip \
	&& pip install --no-cache-dir -r requirements.txt

# copy the rest of the files
COPY --chown=${USER_UID}:${USER_GID} src/* ${WORKDIR}/

# finalization
USER ${USERNAME}
ENTRYPOINT ["streamlit"]
CMD [ "run", "/src/app.py" ]
EXPOSE 80