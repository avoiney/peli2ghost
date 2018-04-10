#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import re
import unicodedata
import os
import sys
import pypandoc


def slugify(value):
    """
    /!\ taken from the django source
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    value = unicodedata.normalize('NFKC', value)
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()

    return re.sub(r'[-\s]+', '-', value)


INFO_REGEX = ':(date|author|tags|lang|slug): ([a-zA-Z0-9\-: .,]+)'
OUTPUT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'output')).rstrip('/')


def get_formarted_now():
    return datetime.datetime.strftime(datetime.datetime.now(),
                                      '%Y-%m-%d %H:%M')


def convert_rst_to_markdown(f):
    with open(f, 'r') as input_file:
        data = input_file.read()
        # get the title of the file
        title = re.search('(.+)\n#+', data).groups()[0]
        # find all usefull information contain sin pelican rst file header
        info = dict(re.findall(INFO_REGEX,
                               data, re.MULTILINE))
        # get date from info
        date = info.get('date', get_formarted_now())
        # remove info from text
        data = re.sub(INFO_REGEX, '', data)
        # find the slug
        try:
            slug = info['slug']
        except KeyError:
            slug = slugify(title)
        # find index of the summary start
        try:
            summary_idx = re.search(':summary:', data).start()
        except AttributeError:
            summary_idx = 0
        # start data from summary
        data = data[summary_idx:]
        data_lines = data.splitlines()
        # find the end of the summary
        for summary_end, line in enumerate(data_lines):
            if not line:
                break
        # keep everything except the summary
        data_lines = data_lines[summary_end:]
        # join the lines
        entry_text = '\n'.join(data_lines).strip()
        # compute the new name
        new_entry_name = 'published-{}-{}.markdown'.format(date.split()[0],
                                                           slug)
        output_entry_path = '{}/{}'.format(OUTPUT_PATH, new_entry_name)
        with open(output_entry_path, 'w') as output_file:
            # convert the text to markdown using pandoc
            pandoc_args = ('--columns=80', '--normalize')
            converted_text = pypandoc.convert_text(entry_text, 'md',
                                                   extra_args=pandoc_args,
                                                   format='rst')
            # encode converted text in utf8
            converted_text = converted_text.encode('utf8')
            # outputed code formatting does not fit with ghost needs
            # change it keeping the language information
            converted_text = re.sub(' {\.sourceCode \.(?P<lang>.+)}',
                                    '\g<lang>', converted_text)
            # same thing for inline code blocks
            converted_text = re.sub('{\.sourceCode}', '', converted_text)
            # add the title (markdown style)
            converted_text = '# {}\n'.format(title) + converted_text
            # write the content in the new file
            output_file.write(converted_text)


if __name__ == '__main__':
    if len(sys.argv) == 0:
        print('Filename required')
        exit(1)
    for filename in sys.argv[1:]:
        convert_rst_to_markdown(filename)
    exit(0)
