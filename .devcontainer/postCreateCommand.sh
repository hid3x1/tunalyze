#!/bin/bash

curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash

echo 'source "$HOME/.rye/env"' >> ~/.bashrc
. "$HOME/.rye/env"