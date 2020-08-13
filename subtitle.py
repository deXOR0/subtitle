import argparse
import shutil
import datetime

parser = argparse.ArgumentParser(
    description='Program to adjust subtitle timings')

parser.add_argument('-o', '--original', type=str, metavar='',
                    required=True, help='set original subtitle file')
parser.add_argument('-n', '--new', type=str, metavar='',
                    help='set new subtitle file, leave blank to name it like the original file')
parser.add_argument('-t', '--time', type=int, metavar='', required=True,
                    help='timing adjustment offset')

args = parser.parse_args()


def time_manipulation(time, offset):
    times = time.split(':')
    hours = int(times[0])
    minute = int(times[0])
    second = int(times[2][:times[2].find(',')])
    millisecond = int(times[2][times[2].find(',')+1:])

    a = datetime.datetime(100, 1, 1, hours, minute, second, millisecond * 1000)
    b = a + datetime.timedelta(microseconds=offset*1000)

    new_time = str(b.time())
    lst = list(new_time)
    for i in range(len(lst)):
        if lst[i] == ',':
            lst[i] = '.'
    new_time = ''.join(lst[:-3])
    return new_time


def adjust_timing(subtitle, offset):
    lines = subtitle.read().splitlines()
    for i in range(len(lines)):
        if ' --> ' in lines[i]:
            times = lines[i].split(' --> ')
            times[0] = time_manipulation(times[0], offset)
            times[1] = time_manipulation(times[1], offset)
            lines[i] = ' --> '.join(times)
    return lines


if __name__ == '__main__':

    original_name = args.original

    if args.new is None:

        old_original = original_name[:original_name.find('.srt')] + '-old.srt'

        shutil.move(original_name, old_original)

        subtitle_file = open(old_original)

        new_file = open(original_name, 'w')
    else:
        new_name = args.new

        subtitle_file = open(original_name)

        new_file = open(new_name, 'w')

    content = (adjust_timing(subtitle_file, args.time))

    new_file_contents = '\n'.join(content)
    new_file.write(new_file_contents)

    new_file.close()
    subtitle_file.close()
