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

# MD page

<blockquote>
    There is <del>nothing</del> <ins>no code</ins> either good or bad, but <del>thinking</del> <ins>running it</ins> makes it so.
</blockquote>

<!-- show input and output -->
### show input and output
```{code-cell} ipython3
note = "Python syntax highlighting"
print(note)
```

### hide input, show output
<!-- hide input, show output -->
```{code-cell} ipython3
:tags: ["hide-input"]
print("This is a test.")
```

### show input, hide output
<!-- show input, hide output -->
```{code-cell} ipython3
:tags: ["hide-output"]
print("This is a test.")
```

### hide input and output
<!-- hide input and output -->
```{code-cell} ipython3
:tags: ["hide-cell"]
print("This is a test.")
```

### remove input, show output
<!-- remove input, show output -->
```{code-cell} ipython3
:tags: ["remove-input"]
print("This is a test.")
```

### show input, remove output
<!-- show input, remove output -->
```{code-cell} ipython3
:tags: ["remove-output"]
print("This is a test.")
```

### remove all
<!-- remove all -->
```{code-cell} ipython3
:tags: ["remove-cell"]
print("This is a test.")
```

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



