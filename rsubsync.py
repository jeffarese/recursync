import fnmatch
import os
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--lang',
                    dest='language_code',
                    required=True,
                    help="Specify a single language code of the subtitles you want to sync (ie. 'es', 'en'...)")

parser.add_argument('--path',
                    dest='path',
                    default='.',
                    required=False,
                    help="Specify the path to sync. It will be '.' by default (current directory)")

args = parser.parse_args()

SETTINGS = {
    "SUBSYNC_PATH": 'subsync',
    "PATH_TO_SYNC": args.path,
    "VIDEO_EXTENSIONS": ['.mkv', '.mp4', '.avi'],
    "SUBTITLE_EXTENSION_TO_SYNC": f'.{args.language_code}.srt',
    "TEMP_OUTPUT_NAME": 'output.srt',
    "OLD_SUFFIX": '.old',
    "FAILED_SUFFIX": '.failed'
}


def get_subtitle(root, filename):
    return os.path.join(root, filename)


def get_file_base(root, filename):
    return os.path.join(root, filename.split(SETTINGS['SUBTITLE_EXTENSION_TO_SYNC'])[0])


def get_matching_video_extension(filename):
    video_match = None
    for extension in SETTINGS['VIDEO_EXTENSIONS']:
        video_file_to_check = f"{filename}{extension}"
        if os.path.exists(video_file_to_check):
            video_match = video_file_to_check
            break
    return video_match


def execute_subsync_process(video, subtitle, output_subtitle, output_file):
    return subprocess.call([SETTINGS['SUBSYNC_PATH'], video, "-i", subtitle, "-o", output_subtitle], stderr=output_file)


def replace_subtitle(subtitle, output):
    os.rename(subtitle,
              f"{subtitle}{SETTINGS['OLD_SUFFIX']}")
    os.rename(output, subtitle)
    os.remove(
        f"{subtitle}{SETTINGS['FAILED_SUFFIX']}")


def main():
    if os.path.exists(SETTINGS['PATH_TO_SYNC']):
        print(f"Starting sync process in path: {SETTINGS['PATH_TO_SYNC']}...")
        for root, dirnames, filenames in os.walk(f"{SETTINGS['PATH_TO_SYNC']}"):
            for filename in fnmatch.filter(filenames, f"*{SETTINGS['SUBTITLE_EXTENSION_TO_SYNC']}"):
                subtitle = get_subtitle(root, filename)
                file_base = get_file_base(root, filename)
                video_match = get_matching_video_extension(file_base)

                if video_match is not None:
                    if os.path.exists(f"{subtitle}{SETTINGS['OLD_SUFFIX']}"):
                        print("Sub already synced")
                    elif os.path.exists(f"{subtitle}{SETTINGS['FAILED_SUFFIX']}"):
                        print("This video failed previously, won't try again")
                    else:
                        try:
                            print(f"Starting sync process of: {filename}")
                            output_filename = os.path.join(
                                root, SETTINGS['TEMP_OUTPUT_NAME'], )
                            failed_file = f"{subtitle}{SETTINGS['FAILED_SUFFIX']}"
                            with open(failed_file, "w+") as outfile:
                                process_code = execute_subsync_process(video_match, subtitle,
                                                                       output_filename, outfile)
                            if process_code != 0:
                                raise Exception
                            replace_subtitle(subtitle, output_filename)
                        except:
                            print(
                                f"There has been an error in the syncing process of: ${filename}")
                else:
                    print(f"There's no video file for: {filename}")
    else:
        print("Specified path does not exist")


main()
