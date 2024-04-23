import os

from utils import File, Log

log = Log('build_gig2_custom_ec')

DIR_GIG2 = os.path.join('gig2')
DIR_GIG2_CUSTOM = os.path.join('gig2_custom_ec_only')


def init():
    if not os.path.exists(DIR_GIG2_CUSTOM):
        os.makedirs(DIR_GIG2_CUSTOM)


def is_pd_id(x: str):
    return x.startswith('EC-') or x == 'LK'


def extract_lines(lines: list):
    return lines[:1] + [
        line for line in lines[1:] if is_pd_id(line.partition('\t')[0])
    ]


def process_file(file_name: str):
    file_path = os.path.join(DIR_GIG2, file_name)
    lines = File(file_path).read_lines()
    new_lines = extract_lines(lines)

    new_file_path = os.path.join(DIR_GIG2_CUSTOM, file_name)
    File(new_file_path).write_lines(new_lines)

    n = len(new_lines)
    log.info(f'Wrote {n} lines to {new_file_path}')


def main():
    init()
    for file_name in os.listdir(DIR_GIG2):
        if (
            file_name.startswith('government-elections')
            or file_name.startswith('population-religion')
            or file_name.startswith('population-ethnicity')
        ):
            process_file(file_name)


if __name__ == "__main__":
    main()
