# /etc/cron.d/ytdl
# 
python3 /opt/DownloadYouTubePlex/DownloadYouTubePlex-0.11.0/DownloadYouTubePlex.py  >> /proc/1/fd/1;
echo "DONE"  >> /proc/1/fd/1;