#! /bin/bash
a=0
for i in *.png; do
  new=$(printf "%04d.ppm" "$a")
  mv -- "$i" "$new"
  let "a=a+1" 
done
