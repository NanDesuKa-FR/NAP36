# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: Nap36Src\__main__.py
import argparse, os, sys
parser = argparse.ArgumentParser()
parser.add_argument('--mode', dest='mode', nargs=1, help='netflix, amazon or primevideo.', default=[])
parser.add_argument('--url', dest='url_season', help='If set, it will download all assets from the season provided.')
parser.add_argument('--nv', '--no-video', dest='novideo', help="If set, don't download video", action='store_true')
parser.add_argument('--na', '--no-audio', dest='noaudio', help="If set, don't download audio", action='store_true')
parser.add_argument('--ns', '--no-subs', dest='nosubs', help="If set, don't download subs", action='store_true')
parser.add_argument('--all-season', dest='all_season', help='If set, active download mode.', action='store_true')
parser.add_argument('-e', '--episode', dest='episodeStart', help='If set, it will start downloading the season from that episode.')
parser.add_argument('-s', dest='season', help='If set, it will download all assets from the season provided.')
parser.add_argument('-q', '--quality', dest='customquality', nargs=1, help='For configure quality of video.', default=[])
parser.add_argument('-o', '--output', dest='output', help='If set, it will download all assets to directory provided.')
parser.add_argument('--keep', dest='keep', help='If set, it will list all formats available.', action='store_true')
parser.add_argument('--no-mux', dest='nomux', help='If set, dont mux.', action='store_true')
parser.add_argument('--langtag', dest='langtag', nargs=1, help='For configure language tag of MKV.', default=[])
parser.add_argument('--only-2ch-audio', dest='only_2ch_audio', help='If set, no clean tag subtitles.', action='store_true')
parser.add_argument('--custom-command', dest='custom_command', nargs=1, help='If set, download only selected audio languages', default=[])
parser.add_argument('--fix-pitch', '--fpitch', dest='fpitch', nargs='*', help='If set, download only selected audio languages', default=[])
parser.add_argument('--source-fps', dest='sourcefps', nargs=1, help='For configure language tag of MKV.', default=[])
parser.add_argument('--target-fps', dest='targetfps', nargs=1, help='For configure language tag of MKV.', default=[])
parser.add_argument('--alang', '--audio-language', dest='audiolang', nargs='*', help='If set, download only selected audio languages', default=[])
parser.add_argument('--slang', '--subtitle-language', dest='sublang', nargs='*', help='If set, download only selected subtitle languages', default=[])
parser.add_argument('--flang', '--forced-language', dest='forcedlang', nargs='*', help='If set, download only selected forced subtitle languages', default=[])
parser.add_argument('--no-cleansubs', dest='nocleansubs', help='If set, no clean tag subtitles.', action='store_true')
parser.add_argument('--title', dest='titlecustom', nargs=1, help='Customize the title of the show', default=[])
parser.add_argument('--hevc', dest='hevc', help='If set, it will return HEVC manifest', action='store_true')
parser.add_argument('--micro', dest='lower', help='If set, it will return HEVC manifest', action='store_true')
parser.add_argument('--asin', dest='asin', help='Enter ASIN.')
parser.add_argument('--retry', dest='retry', help='Retry.', action='store_true')
parser.add_argument('--atmos', dest='atmos', help='If set, it will return Atmos MPDs', action='store_true')
parser.add_argument('--nc', '--no-chapters', dest='nochpaters', help="If set, don't download chapters", action='store_true')
parser.add_argument('-r', '--region', default='ps', choices=['ps', 'ps-int', 'us', 'uk', 'de', 'jp'], help='amazon video region')
parser.add_argument('--clang', '--chapters-language', dest='chapterslang', nargs=1, help='If set, download only selected forced subtitle languages', default=[])
parser.add_argument('--tlang', '--title-language', dest='titlelang', nargs=1, help='If set, download only selected forced subtitle languages', default=[])
parser.add_argument('--ID', dest='nflxID', nargs='?', help='The Netflix viewable ID.')
parser.add_argument('--hdr', dest='hdr', help='If set, it will return HDR manifest', action='store_true')
parser.add_argument('--force-audiohq', dest='forceaudiohq', help='If set, it will return HDR manifest', action='store_true')
parser.add_argument('--aformat-2ch', '--audio-format-2ch', dest='aformat_2ch', nargs=1, help='For configure format of audio.', default=[])
parser.add_argument('--aformat-51ch', '--audio-format-51ch', dest='aformat_51ch', nargs=1, help='For configure format of audio.', default=[])
parser.add_argument('--vp9', dest='video_vp9', help='If set, no clean tag subtitles.', action='store_true')
parser.add_argument('--np', '--no-prompt', dest='noprompt', help='If set, it will disable the yes/no prompt when URLs are grabbed.', action='store_true')
parser.add_argument('--nar', '--no-all-regions', dest='noallregions', help='If set, it will disable collating assets from all regions.', action='store_true')
parser.add_argument('--only-keys', dest='onlykeys', help='If set, no clean tag subtitles.', action='store_true')
parser.add_argument('--vpngate', dest='country_code', help="If set, you'll be connected to the desired country using VPNGate.", default=None)
parser.add_argument('--ipv', dest='ipversion', help='Workaround for NF HIGH Profiles ipv4 SSL Errors. If problem, use --ipv 6')
args = parser.parse_args()
args.onlykeys = False
args.forceaudiohq = False
currentFile = '__main__'
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
from binaries.VPN.VPNGate import VPNGateConnect
if __name__ == '__main__':
    if args.country_code != None:
        print('Killing previous OpenVPN sessions...')
        os.system('taskkill /im openvpn.exe /f')
        VPNGateConnect(args.country_code)
    if args.url_season and 'netflix' in args.url_season or args.nflxID or args.mode and args.mode[0] == 'netflix':
        mode = 'netflix'
        import netflix36
        netflix36()
    else:
        if args.url_season and 'amazon' in args.url_season or args.asin or args.mode and args.mode[0] == 'amazon':
            mode = 'amazon'
            import primevideo36
            primevideo36()
        else:
            if args.url_season and 'primevideo.com' in args.url_season or args.asin or args.mode and args.mode[0] == 'primevideo':
                mode = 'primevideo'
                import primevideo36
                primevideo36()
            else:
                url_season = input('Enter the Netflix, Amazon or Primevideo URL (with https): ')
                args.url_season = url_season
                if 'netflix' in url_season:
                    mode = 'netflix'
                    import netflix36
                    netflix36()
                else:
                    if 'amazon' in url_season:
                        mode = 'amazon'
                        import primevideo36
                        primevideo36()
                    else:
                        if 'primevideo.com' in url_season:
                            mode = 'primevideo'
                            import primevideo36
                            primevideo36()
                        else:
                            if args.country_code != None:
                                os.system('taskkill /im openvpn.exe /f')
                            print('Error! This url or mode is not recognized.')
                            sys.exit(0)