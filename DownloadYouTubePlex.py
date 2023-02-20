# RUN /mnt/pve/NFS_1TB/Python$ python3 /mnt/pve/NFS_1TB/Python/Read_XML.py
from pathlib import Path
from xml.dom import minidom
import time
from xml.parsers.expat import ExpatError
import os
import subprocess
import json
import requests
from email_validator import validate_email, EmailNotValidError
# from email_validator import EmailNotValidError
# from email_validator import EmailSynaxError
# from email_validator import EmailUndeliverableError

# def Write_to_Log(logContent):
#     x = datetime.datetime.now()
#     print(x.strftime("%X")) 
#     # print(x)

def NotifyPushover(AppToken,nTitle,nBody,pThumbnail):
    # wget -O "/config/json/maxresdefault2.jpg" $ytvideo_thumbnail;
    # $htmltext = "<html><body>${ytvideo_title}}<br /><br />--------------------------------------------<br /><br />${ytvideo_description}</body></html>";
    # Out-File -FilePath "/config/json/pushovernotify2.txt" -InputObject $htmltext -Force;
    
    # cat "/config/json/pushovernotify2.txt" | mutt -a "/config/json/maxresdefault2.jpg" -s "RSS Podcast Downloaded (${ChannelID})" -- mphfckm6ji@pomail.net;
    try:
        print ('------------------      START NotifyPushover\n')
        bashcmd = 'wget -O /config/maxresdefault.jpg ' + pThumbnail
        print("bashcmd: " + bashcmd)
        process = subprocess.Popen(bashcmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        APPLICATION_TOKEN = AppToken
        USER_TOKEN = "ZLzrC79W0yAeoj5f4Jz0P3EZbHJKAB"
        url = 'https://api.pushover.net/1/messages.json'
        my_pushover_request = {'token': APPLICATION_TOKEN, 'user': USER_TOKEN,
                    'title': nTitle, 'message': nBody, 'html': '1'}
        req = requests.post(url, data=my_pushover_request, files={"attachment":open("/config/maxresdefault.jpg","rb")})
        print("Pushover Status: " + str(req.status_code))
        print ('------------------      END NotifyPushover\n')
    except Exception as err:
        print ('------------------      START NotifyPushover ERROR\n')
        print (err)
        print ('\n------------------      END NotifyPushover ERROR')

def Run_YTDLP(sMediaFolder, pName, pChannelID, pFileFormat, pDownloadArchive, pFileQuality, pChannelThumbnail, pYouTubeURL):
    print('Run_YTDLP')
    error = ''

    try:
        print ('------------------      START YT-DLP\n')
        # ======================================================== #
        # ============== Download Channel JSON Only ============== #
        # ======================================================== #
        pubDate = time.strftime('%Y%m%d%H%M')
        bashcmd3 = "yt-dlp -v -o " + sMediaFolder + pChannelID + "/" + pChannelID + "/Season 1/s1." + pubDate + ".mp4 --write-info-json --playlist-items 0 --restrict-filenames --add-metadata --merge-output-format " + pFileFormat + " --format " + pFileQuality + " --abort-on-error --abort-on-unavailable-fragment --no-overwrites --continue " + pYouTubeURL
        # bashcmd = "yt-dlp -v -o '" + sMediaFolder + pChannelID + "/%(id)s.%(ext)s' --write-info-json --external-downloader aria2c --external-downloader-args '-c -j 10 -x 10 -s 10 -k 1M' --playlist-items 1,2,3,4,5,3,4,5 --restrict-filenames --download-archive '" + pDownloadArchive + "' --add-metadata --merge-output-format " + pFileFormat + " --format " + pFileQuality + " --abort-on-error --abort-on-unavailable-fragment --no-overwrites --continue --write-description " + pYouTubeURL
        # print(bashcmd)

        process3 = subprocess.Popen(bashcmd3.split(), stdout=subprocess.PIPE)
        output3, error3 = process3.communicate()

        print("output: " + str(output3))
        print("error: " + str(error3))

        # ======================================================== #
        # ============== Download Videos with yt-dlp ============= #
        # ======================================================== #

        bashcmd = "yt-dlp -v -o " + sMediaFolder + pChannelID + "/Season 1/[%(id)s].%(ext)s --write-info-json --no-write-playlist-metafiles --playlist-items 1,2 --restrict-filenames --download-archive " + pDownloadArchive + " --add-metadata --merge-output-format " + pFileFormat + " --format " + pFileQuality + " --abort-on-error --abort-on-unavailable-fragment --no-overwrites --continue --write-description " + pYouTubeURL
        # bashcmd = "yt-dlp -v -o '" + sMediaFolder + pChannelID + "/%(id)s.%(ext)s' --write-info-json --external-downloader aria2c --external-downloader-args '-c -j 10 -x 10 -s 10 -k 1M' --playlist-items 1,2,3,4,5,3,4,5 --restrict-filenames --download-archive '" + pDownloadArchive + "' --add-metadata --merge-output-format " + pFileFormat + " --format " + pFileQuality + " --abort-on-error --abort-on-unavailable-fragment --no-overwrites --continue --write-description " + pYouTubeURL
        print ('------------------      \n\n')
        print("bashcmd: " + bashcmd)
        print ('------------------      \n\n')

        process = subprocess.Popen(bashcmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        print("output: " + str(output))
        print("error: " + str(error))

        print('Downloaded Video Files for ' + pName)
        print ('------------------      END YT-DLP\n')
    except Exception as err:
        print ('------------------      START YT-DLP ERROR\n')
        print (err)
        print ('\n------------------      END YT-DLP ERROR')

    if error == None:
        try:
            print("List Files")
            
            directory = os.fsencode(sMediaFolder + pChannelID + "/Season 1")
                
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                filename_noext = ""
                filename_mediafile = ""
                filename_json = ""
                if filename.endswith(".description"): 
                    try:
                        pathname, extension = os.path.splitext(filename)
                        filename = pathname.split('/')
                        filename_noext = filename[-1]
                        
                        print("filename (no ext)" + filename_noext)
                    except:
                        print ('------------------      START GET EXT ERROR\n')
                        print (err)
                        print ('\n------------------      END GET EXT ERROR')

                    filename_json = sMediaFolder + pChannelID + "/Season 1/" + filename_noext + ".info.json"
                    filename_mp3 = sMediaFolder + pChannelID + "/Season 1/" + filename_noext + ".mp3"
                    filename_mp4 = sMediaFolder + pChannelID + "/Season 1/" + filename_noext + ".mp4"

                    print("filename_json: " + filename_json)
                    print("filename_mp3: " + filename_mp3)
                    print("filename_mp4: " + filename_mp4)

                    filename_json_isfile = False
                    filename_mp3_isfile = False
                    filename_mp4_isfile = False

                    if os.path.isfile(filename_json):
                        print('The JSON file is present.')
                        filename_json_isfile = True
                    if os.path.isfile(filename_mp3):
                        print('The MP3 file is present.')
                        filename_mp3_isfile = True
                        filename_ext = filename_noext + ".mp3"
                    if os.path.isfile(filename_mp4):
                        print('The MP4 file is present.')
                        filename_mp4_isfile = True
                        filename_ext = filename_noext + ".mp4"

                    ytvideo_uid = ""
                    ytvideo_title = ""
                    ytvideo_thumbnail = ""
                    ytvideo_description = ""
                    ytvideo_uploader = ""
                    ytvideo_uploader_url = ""
                    ytvideo_channel_id = ""
                    ytvideo_channel_url = ""
                    ytvideo_duration = ""
                    ytvideo_webpage_url = ""
                    ytvideo_filesize = ""

                    if (filename_json_isfile == True and filename_mp4_isfile == True):
                        # print("ADD FILE TO RSS FEED: " + filename_mp4)
                        # print("Read JSON File")
                        f = open(filename_json)
                        data = json.load(f)
                        # print(data['id'])
                        
                        # Iterating through the json
                        # list
                        # for i in data['id']:
                        #     print(i)
                        
                        # ~~~~~~~~~~~~~ Get JSON Data ~~~~~~~~~~~~~ #
                        ytvideo_uid = data['id']
                        ytvideo_title = data['title']
                        ytvideo_description = data['description']
                        ytvideo_uploader = data['uploader']
                        ytvideo_uploader_id = data['uploader_id']
                        ytvideo_uploader_url = data['uploader_url']
                        ytvideo_channel_id = data['channel_id']
                        ytvideo_channel_url = data['channel_url']
                        ytvideo_duration = data['duration']
                        ytvideo_webpage_url = data['webpage_url']
                        ytvideo_filesize = data['filesize_approx']
                        ytvideo_thumbnail = data['thumbnail']

                        print("ytvideo_uid: " + ytvideo_uid)
                        print("ytvideo_title: " + ytvideo_title)
                        print("ytvideo_uploader: " + ytvideo_uploader)
                        print("ytvideo_uploader_id: " + ytvideo_uploader_id)
                        print("ytvideo_uploader_url: " + ytvideo_uploader_url)
                        print("ytvideo_channel_id: " + ytvideo_channel_id)
                        print("ytvideo_channel_url: " + ytvideo_channel_url)
                        print("ytvideo_webpage_url: " + ytvideo_webpage_url)

                        # print('ytvideo_duration: ' + str(ytvideo_duration))
                        print ('\n------------------      Item (' + ytvideo_uid + ')')

                        # Closing file
                        f.close()

                        # ======================================================== #
                        # ================ Get Channel Information =============== #
                        # ======================================================== #
                        channel_filename_json = sMediaFolder + pChannelID + "/Season 1/" + pChannelID + ".info.json"
                        channelf = open(channel_filename_json)
                        channeldata = json.load(channelf)
                        ytvideo_channel_desc = channeldata['description']
                        ytvideo_channel_image = ''
                        # print("----------------------   Thumbnails")
                        # print(channeldata['thumbnails'])
                        for thumbs in channeldata['thumbnails']:
                            thumbsjson = str(thumbs).replace("'",'"')
                            # print('thumbs json: ' + thumbsjson)
                            thumbdata = json.loads(thumbsjson)

                            if thumbdata['id'] == "avatar_uncropped":
                                # print("id: " + thumbdata['id'])
                                # print("url: " + thumbdata['url'])
                                ytvideo_channel_image = thumbdata['url']
                            # print("-------- THUMB")
                        # print("----------------------")
                        if pChannelThumbnail == "":
                            pChannelThumbnail = ytvideo_channel_image
                        print("Channel Thumbnail: " + ytvideo_channel_image)
                        channelf.close

                        # ======================================================== #
                        # ==================== Notify Pushover =================== #
                        # ======================================================== #

                        with open(pDownloadArchive, 'r') as rsstemplate:
                            RSSData = rsstemplate.readlines()
                            strRSSData = ''.join(RSSData)

                        # ======================================================== #
                        # =============== Add Items to Existing XML ============== #
                        # ======================================================== #

                        if ytvideo_uid in strRSSData:
                            print("Item (" + ytvideo_uid + ") already in archive file")
                        else:
                            NotifyPushover("apb75jkyb1iegxzp4styr5tgidq3fg","YouTube Video Downloaded (" + pName + ")","<html><body>" + ytvideo_title + "<br /><br />--------------------------------------------<br /><br />" + ytvideo_description + "</body></html>",ytvideo_thumbnail)
                    continue
                else:
                    continue
        except Exception as err:
            print ('------------------      START GET FILES ERROR\n')
            print (err)
            print (err.__annotations__)
            print (err.with_traceback)
            print ('\n------------------      END GET FILES ERROR')
    else:
        # print("YT-DLP ERROR")
        print ('------------------      START YT-DLP ERROR\n')
        print (err)
        print (err.__annotations__)
        print (err.with_traceback)
        print ('\n------------------      END YT-DLP ERROR')
        
# ======================================================== #
# ===================== Script Start ===================== #
# ======================================================== #
settingsPath = '/config/settings.xml'
# settingsPath = '/mnt/pve/NFS_1TB/Python/DownloadYouTubePlex/settings.xml'
# rssTemplatePath = '/mnt/pve/NFS_1TB/Python/RSS_TEMPLATE_2.0.xml'
rssTemplatePath = '/config/RSS_TEMPLATE_2.0.xml'
rssPath = '/data/rss/'
# rssPath = '/mnt/pve/NFS_1TB/Python/'
httpHost = 'http://10.0.0.205:8383'
jsonFolder = '/config/json/'
jsonMediaFolder_YouTube = '/config/json/ytvideos/'
# jsonMediaFolder_Twitch = '/config/json/twitchvideos/'
# Twitch_DownloadArchive = "/mnt/pve/NFS_1TB/Python/youtube-dl-notifytwitch.txt"
# Twitch_DownloadArchive = "/config/json/youtube-dl-notifytwitch.txt"


Settings_Email = ''
Settings_MediaFolder = ''

IsValid_Email = False
IsValid_MediaFolder = False

print('=============================      PodcastsDownload\n')

if os.path.isfile(settingsPath):
    print('The settings file is present.')
    exist = True
else:
    print('The settings file is not present.')
    exist = False

# print(exist)

if exist == True:
    try:
        # parse an xml file by name
        file = minidom.parse(settingsPath)

        # ------ Get Email Tag ----- #
        xmlSettingsEmail = file.getElementsByTagName('Email')
        Settings_Email = xmlSettingsEmail[0].firstChild.data

        # ----- Validate Email ----- #

        # (EmailNotValidError, EmailSynaxError, EmailUndeliverableError)
        try:
            emailObject = validate_email(Settings_Email)
            # print("Valid Email: " + emailObject.email)
            IsValid_Email = True
            print('The email (' + Settings_Email + ') is valid.')
        except EmailNotValidError as EmailError:
            print('The email (' + Settings_Email + ') is valid.')
            IsValid_Email = False
            print ('------------------      START EMAIL ERROR\n')
            print (EmailError)
            print ('\n------------------      END EMAIL ERROR')

        # ---- Get MediaPath Tag --- #
        xmlSettingsMediaFolder = file.getElementsByTagName('MediaFolder')
        Settings_MediaFolder = xmlSettingsMediaFolder[0].firstChild.data
        
        # --- Validate MediaPath --- #
        if os.path.exists(Settings_MediaFolder):
            print('The folder (' + Settings_MediaFolder + ') is present.')
            IsValid_MediaFolder = True
        else:
            print('The folder (' + Settings_MediaFolder + ')  is not present.')
            IsValid_MediaFolder = False

        # ~~~~~~~~~ Print Valid Variables ~~~~~~~~~ #

        print("IsValid_Email: " + str(IsValid_Email))
        print("IsValid_MediaFolder: " + str(IsValid_MediaFolder))

        if IsValid_Email ==  True and IsValid_MediaFolder == True:
            print ('\n------------------      Valid Data\n')

            print("Email: " + Settings_Email)
            print("MediaFolder: " + Settings_MediaFolder)

            # ======================================================== #
            # ============= Loop through PodcastsDownload ============ #
            # ======================================================== #

            xmlPodcastsDownload = file.getElementsByTagName('PodcastDownload')
            for elem in xmlPodcastsDownload:
                Podcast_Name = elem.attributes['Name'].value
                Podcast_ChannelID = elem.attributes['ChannelID'].value
                Podcast_FileFormat = elem.attributes['FileFormat'].value
                Podcast_DownloadArchive = elem.attributes['DownloadArchive'].value
                Podcast_FileQuality = elem.attributes['FileQuality'].value
                Podcast_ChannelThumbnail = elem.attributes['ChannelThumbnail'].value
                Podcast_YouTubeURL = elem.attributes['YouTubeURL'].value
                
                print ('------------------      Podcast\n')
                print("Podcast_Name: " + Podcast_Name)
                print("Podcast_ChannelID: " + Podcast_ChannelID)
                print("Podcast_FileFormat: " + Podcast_FileFormat)
                print("Podcast_DownloadArchive: " + Podcast_DownloadArchive)
                print("Podcast_FileQuality: " + Podcast_FileQuality)
                print("Podcast_ChannelThumbnail: " + Podcast_ChannelThumbnail)
                print("Podcast_YouTubeURL: " + Podcast_YouTubeURL)
                print ('\n')

                # ======================================================== #
                # ====================== Run YT-DLP ====================== #
                # ======================================================== #

                Run_YTDLP(Settings_MediaFolder, Podcast_Name, Podcast_ChannelID, Podcast_FileFormat, Podcast_DownloadArchive, Podcast_FileQuality, Podcast_ChannelThumbnail, Podcast_YouTubeURL)
        else:
            print ('\n------------------')
            print("Settings Not Valid")
            print ('\n------------------')


        # ~~~~~~~~~~~~~ Validate Email ~~~~~~~~~~~~ #

    except ExpatError as XMLerr:
        print ('------------------      START XML ERROR\n')
        print (XMLerr)
        print ('\n------------------      END XML ERROR')
else:
    print('Settings Path Not Valid')