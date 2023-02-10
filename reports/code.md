---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Code

### remove input, show output
<!-- remove input, show output -->
```{code-cell} ipython3
:tags: ["remove-input"]
import sys
import json
import pandas as pd

sys.path.insert(0, 'src')
from etl import get_data, save_data

def main(targets):

    data_config = json.load(open('config/config.json'))

    if 'test' in targets:

        data = get_data(data_config)
        save_data(data_config, data) #load and train the model with test_load data
        # return print("test ok")
        return

    elif 'run' in targets:

        return print("run ok")

    else:

        return print("error target")

if __name__ == '__main__':

    targets = sys.argv[1:]
    # targets = 'testdata'
    main(targets)
```



<!------------->




### Thebe
<!-- Configure and load Thebe !-->
<script type="text/x-thebe-config">
  {
      requestKernel: true,
      mountActivateWidget: true,
      mountStatusWidget: true,
      binderOptions: {
      repo: "binder-examples/requirements",
      },
  }
</script>

<script src="https://unpkg.com/thebe@latest/lib/index.js"></script>

<pre data-executable="true" data-language="python">print("Hello!")</pre>

<div class="thebe-activate"></div>
<div class="thebe-status"></div>


