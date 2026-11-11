# GUIs: the Python toolkits

| Toolkit | Install | Kind | Good for |
|---|---|---|---|
| tkinter | included | Desktop | Small tools, teaching, quick utilities |
| PySide6 / PyQt6 | `pip install PySide6` | Desktop | Professional desktop apps (Qt Designer, rich widgets) |
| wxPython | `pip install wxPython` | Desktop | Native-looking desktop apps |
| Kivy | `pip install kivy` | Desktop + mobile | Touch interfaces, Android and iOS |
| Dear PyGui | `pip install dearpygui` | Desktop | Fast tool panels, real-time plots |
| Streamlit | `pip install streamlit` | Web (runs a local server) | Data apps and dashboards in a few lines |
| Gradio | `pip install gradio` | Web | Demos of machine-learning and LLM models |
| NiceGUI | `pip install nicegui` | Web | Web UIs written only in Python |
| Flet | `pip install flet` | Web, desktop, mobile | Flutter-style apps in Python |
| FastAPI + a JavaScript front end | `pip install fastapi uvicorn` | Web | Production systems (Python is the back end) |

## How to choose

1. **A quick tool for yourself or the lab bench:** tkinter, or Dear PyGui for live plots.
2. **A desktop product for customers:** PySide6.
3. **A demo for an AI model, or a data dashboard:** Gradio or Streamlit (a few lines, runs in the browser).
4. **A real web product:** FastAPI for the back end and a JavaScript front end (React/Next.js).
5. **A phone app:** Kivy or Flet.

## The same idea in three toolkits

**Gradio** (a model demo, 6 lines):

```python
import gradio as gr

def shout(text):
    return text.upper()

gr.Interface(fn=shout, inputs="text", outputs="text").launch()
```

**Streamlit** (run with `streamlit run app.py`):

```python
import streamlit as st

st.title("Temperature converter")
celsius = st.number_input("Celsius", value=100.0)
st.write(f"{celsius * 9 / 5 + 32:.1f} F")
```

**PySide6** (desktop):

```python
import sys
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("Hello from Qt")
label.show()
sys.exit(app.exec())
```

## Rules every GUI shares

- One **event loop** owns the screen. Keep callbacks short.
- Slow work (network, files, models) runs in a **thread or process**, never in a callback.
- Keep the **logic separate from the widgets**, so you can test it without a window.
- Web UIs for AI work usually talk to the model through an **API** (FastAPI) instead of loading it in the UI process.
