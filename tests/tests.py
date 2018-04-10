# /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import tempfile

import peli2ghost


TEST_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'test.rst'))


OUTPUT = '''# My Great Title <3
Welcome on the test RST article.

```python
def some_code(arg1):
    print(arg1)
    return True
```

Some text to convert.

And some other with `inline code` inside.

Oh, and a link to my [github profile](https://github.com/avoiney).
'''


def test_rendering_from_rst_to_markdown():
    output_file = './output/published-2018-04-11-my-great-title.markdown'
    # start by cleaning the file too avoid false positive
    if os.path.exists(output_file):
        os.remove(output_file)
    peli2ghost.convert_rst_to_markdown(TEST_FILE)
    assert os.path.exists(output_file)
    assert open(output_file, 'r').read() == OUTPUT
