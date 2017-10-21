#!/bin/bash


source env_vars.sh
python app/application.py > ./api.out & 2> ./api_errors 
