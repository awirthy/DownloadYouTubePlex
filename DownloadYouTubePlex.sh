# /etc/cron.d/ytdl
# 
python3 /opt/DownloadYouTubev2/DownloadYouTubePlex-0.10.0/DownloadYouTubePlex.py  >> /proc/1/fd/1;
echo "DONE"  >> /proc/1/fd/1;