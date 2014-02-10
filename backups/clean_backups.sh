#!/bin/bash

LIMIT=10

echo "Cleaning journal files..."
rm *.db-journal 2> /dev/null

echo "Checking if backups need to be cleaned..."
backups=$(ls *.db | wc -l)

if [ "$backups" -gt "$LIMIT" ]
then
  count=$(expr $backups - $LIMIT) 
  echo "$backups backups found. Removing $count oldest."
  for i in $(seq $count)
  do
    file=$(ls *.db | head -n 1)
    rm $file
    echo "Deleted $file"
  done
else
   echo "No backups removed."
fi
