# With ssh key
# rsync -az --out-format="%t %n %'''b" \
#       --remove-source-files \
#       --timeout 30 \
#       -e "ssh -i ~/.ssh/lab -p 2020 -o StrictHostKeyChecking=no" \
#       ./rgb_img/ \
#       <replaced>@<replaced>:/path/to/dir
#
# rsync -az --out-format="%t %n %'''b" \
#       --remove-source-files \
#       --timeout 30 \
#       -e "ssh -i ~/.ssh/lab -p 2020 -o StrictHostKeyChecking=no" \
#       ./IR_HDF5_* \
#       <replaced>@<replaced>:/path/to/dir

# With ssh password
sshpass -p '<replaced>' \
rsync -az --out-format="%t %n %'''b" \
      --remove-source-files \
      --timeout 30 \
      -e "ssh -p <replaced> -o StrictHostKeyChecking=no" \
      ./rgb_img/ \
      <replaced>@<replaced>:/path/to/dir

sshpass -p '<replaced>' \
rsync -az --out-format="%t %n %'''b" \
      --remove-source-files \
      --timeout 30 \
      -e "ssh -p <replaced> -o StrictHostKeyChecking=no" \
      ./IR_HDF5_* \
      <replaced>@<replaced>:/path/to/dir
