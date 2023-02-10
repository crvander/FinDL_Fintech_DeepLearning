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
pip install pandas
import pandas as pd

df = pd.DataFrame({'name': ['carlos', 'diane'], 'gender': ['male', 'female']})
df
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


