# /etc/cron.d/ytdl
# 
python3 -m pip install -U yt-dlp
python3 /opt/DownloadYouTubePlex/DownloadYouTubePlex-0.43.0/DownloadYouTubePlex.py  >> /proc/1/fd/1;
echo "DONE"  >> /proc/1/fd/1;