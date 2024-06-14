rsync -a --exclude='.*' --exclude='wordlist' . /home/nfsl2001/aaexam/
cd /home/nfsl2001/aaexam/
buildozer android debug
cp /home/nfsl2001/aaexam/bin/*.apk /mnt/d/Desktop/UM/Y3S2/WIG3005/aaexam/