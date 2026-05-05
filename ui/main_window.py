# will contains all the ui main window
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk

from .components import (
    create_button,
    create_label,
    create_labeled_frame,
    create_radio,
    create_text_box,
    create_image_canvas,
)
from config.settings import AVAILABLE_MODELS
from models.model_factory import get_model
from utils.image_utils import process_image


# create a main window class
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter AI GUI")
        self.geometry("900x520")
        self.resizable(False, False)

        self.selected_model_key = tk.StringVar(value="vit")
        self.input_mode = tk.StringVar(value="image")
        self.loaded_model = None
        self.current_image_path = None
        self.tk_preview_image = None

        self._build_menu()
        self._build_header()
        self._build_body()
        
        # Fullscreen state and shortcuts
        self.is_fullscreen = False
        self.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.bind("<Escape>", lambda e: self.exit_fullscreen())

    def _build_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="Toggle Full Screen (F11)", command=self.toggle_fullscreen)
        viewmenu.add_command(label="Exit Full Screen (Esc)", command=self.exit_fullscreen)
        menubar.add_cascade(label="View", menu=viewmenu)

        modelmenu = tk.Menu(menubar, tearoff=0)
        modelmenu.add_command(label="Load Model", command=self.load_model)
        menubar.add_cascade(label="Models", menu=modelmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=lambda: None)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def exit_fullscreen(self):
        self.is_fullscreen = False
        self.attributes("-fullscreen", False)

    def _build_header(self):
        container = ttk.Frame(self, padding=(10, 8))
        container.pack(fill="x")

        ttk.Label(container, text="Model Selection:").pack(side="left")

        self.model_combo = ttk.Combobox(
            container,
            values=["ViT (Classify)",
                    "DeiT (Classify)", 
                    "ResNet (Classify)",
                    "Stable Diffusion (text2image)"],
            state="readonly",
            width=28,
        )
        self.model_combo.current(0)
        self.model_combo.pack(side="left", padx=8)

        load_btn = create_button(container, "Load Model", self.load_model)
        load_btn.pack(side="left", padx=8)

    def _build_body(self):
        body = ttk.Frame(self, padding=(10, 0))
        body.pack(fill="both", expand=True)

        # Left: User Input Section
        input_frame = create_labeled_frame(body, "User Input Section")
        input_frame.place(x=10, y=10, width=420, height=440)

        radios_frame = ttk.Frame(input_frame)
        radios_frame.pack(anchor="w", pady=(0, 6))
        create_radio(radios_frame, "Text", "text", self.input_mode).pack(side="left", padx=(0, 12))
        create_radio(radios_frame, "Image", "image", self.input_mode).pack(side="left")

        browse_btn = create_button(input_frame, "Browse", self.browse_image)
        browse_btn.pack(anchor="w", pady=(0, 8))

        self.prompt_box = create_text_box(input_frame, height=10, width=48)
        self.prompt_box.pack(anchor="w")

        buttons_row = ttk.Frame(input_frame)
        buttons_row.pack(anchor="w", pady=8)
        run1 = create_button(buttons_row, "Run Model 1", self.run_model)
        run2 = create_button(buttons_row, "Run Model 2", self.run_model)
        clear = create_button(buttons_row, "Clear", self.clear_output)
        run1.pack(side="left", padx=(0, 6))
        run2.pack(side="left", padx=(0, 6))
        clear.pack(side="left")

        # Right: Output Section
        output_frame = create_labeled_frame(body, "Model Output Section")
        output_frame.place(x=440, y=10, width=440, height=440)

        create_label(output_frame, "Output Display:").pack(anchor="w")
        self.output_box = create_text_box(output_frame, height=10, width=48)
        self.output_box.pack(anchor="w", pady=(0, 8))

        create_label(output_frame, "Preview:").pack(anchor="w")
        self.preview_canvas = create_image_canvas(output_frame, width=380, height=220)
        self.preview_canvas.pack(anchor="w", pady=(0, 4))

    def _parse_model_key(self):
        selection = self.model_combo.get()
        if "deit" in selection.lower():
            return "deit"
        if "resnet" in selection.lower():
            return "resnet"
        if "diffusion" in selection.lower() or "text2image" in selection.lower():
            return "text2image"
        return "vit"

    def load_model(self):
        model_key = self._parse_model_key()
        try:
            self.loaded_model = get_model(model_key)
            self._append_output(f"Loaded model: {model_key} -> {AVAILABLE_MODELS[model_key]}")
        except Exception as exc:
            self._append_output(f"Error loading model: {exc}")
            
        print("DEBUG: Model key selected ->", model_key)


    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[["Image files", "*.jpg *.jpeg *.png"]])
        if not file_path:
            return
        self.current_image_path = file_path
        self._show_preview(file_path)
        self._append_output(f"Selected image: {file_path}")

    def run_model(self):
        if not self.loaded_model:
            self._append_output("Please load a model first.")
            return
        
        model_key = self._parse_model_key()

       
        # ---- text2image model ----
        if model_key == "text2image":
            prompt = self.prompt_box.get("1.0", tk.END).strip()
            if not prompt:
                self._append_output("Please enter a prompt for text-to-image generation.")
                return
            image = self.loaded_model.predict(prompt)

            self.tk_preview_image = ImageTk.PhotoImage(image.resize((380, 220)))
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(0, 0, anchor="nw", image=self.tk_preview_image)
            self._append_output("Generated image from prompt.")
            return

        # ---- image classification models ----
        if self.input_mode.get() == "image":
            if not self.current_image_path:
                self._append_output("Please browse and select an image.")
                return
            results = self.loaded_model.predict(self.current_image_path)
        else:
            prompt = self.prompt_box.get("1.0", tk.END).strip()
            if not prompt:
                self._append_output("Please enter a prompt or switch to Image mode.")
                return
            self._append_output("Text mode is not supported for classification; showing prompt only.")
            results = []

        if results:
            self._render_predictions(results)

    def clear_output(self):
        self.output_box.delete("1.0", tk.END)

    def _append_output(self, text):
        self.output_box.insert(tk.END, text + "\n")
        self.output_box.see(tk.END)

    def _show_preview(self, image_path):
        img = process_image(image_path, (380, 220))
        self.tk_preview_image = ImageTk.PhotoImage(img)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(0, 0, anchor="nw", image=self.tk_preview_image)

    def _render_predictions(self, results):
        self._append_output("Predictions:")
        for pred in results:
            label = pred.get("label")
            score = pred.get("score")
            self._append_output(f"- {label}: {score:.4f}")


