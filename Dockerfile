FROM mcr.microsoft.com/devcontainers/base:bullseye
RUN apt-get update \
  && apt-get install -y libwebkit2gtk-4.0-dev libssl-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev git vim curl bash \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN echo "source /usr/share/bash-completion/completions/git" >> ~/.bashrc

WORKDIR /workspace

RUN curl -O https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh
RUN curl -O https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash
RUN chmod a+x git*.*
RUN ls -l $PWD/git*.* | awk '{print "source "$9}' >> ~/.bashrc

RUN echo "GIT_PS1_SHOWDIRTYSTATE=true" >> ~/.bashrc
RUN echo "GIT_PS1_SHOWUNTRACKEDFILES=true" >> ~/.bashrc
RUN echo "GIT_PS1_SHOWUPSTREAM=auto" >> ~/.bashrc

RUN echo 'export PS1="\[\033[01;32m\]\u@\h\[\033[01;33m\] \w \[\033[01;31m\]\$(__git_ps1 \"(%s)\") \\n\[\033[01;34m\]\\$ \[\033[00m\]"' >> ~/.bashrc