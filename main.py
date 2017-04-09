import re
import sys
from collections import Counter
import subprocess

INSTRUCTION_REGEX = ' +[0-9a-f]+:\t+(\w+)'


def get_format_string(longest_string_length, maximum_count):
    return '{{:{}}} | {{:{}}}| {{:7f}}'.format(longest_string_length, len(str(maximum_count)))


def longest_string(strings):
    return max(map(len, strings))


if __name__ == '__main__':
    object = None
    if len(sys.argv) < 2:
        raise Exception
    else:
        object = sys.argv[1]
    completed = subprocess.run(['objdump', '-d', '--no-show-raw-insn', object], stdout=subprocess.PIPE)
    instruction_counter = Counter()
    for line in completed.stdout.decode('utf-8').split('\n'):
        for instruction_string in re.findall(INSTRUCTION_REGEX, line):
            instruction_counter.update([instruction_string])
    instruction_total = sum(instruction_counter.values())
    format_string = get_format_string(longest_string(instruction_counter.keys()), instruction_total)
    print(format_string.format('*', instruction_total, instruction_total / instruction_total))
    for instruction, count in sorted(instruction_counter.items(), key=lambda pair: -pair[1]):
        print(format_string.format(instruction, count, count / instruction_total))
