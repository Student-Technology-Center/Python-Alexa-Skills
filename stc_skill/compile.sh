#!/bin/sh

rm -R skill_env
mkdir skill_env

pip install -r requirements.txt -t skill_env
cp lambda/* skill_env/
