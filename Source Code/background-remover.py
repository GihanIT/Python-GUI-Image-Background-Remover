import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from threading import Thread
import queue

class BackgroundRemoverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GihanIT Advanced Background Remover")
        self.root.geometry("1000x800")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        self.style.configure('Info.TLabel', font=('Helvetica', 10))
        self.style.configure('Status.TLabel', font=('Helvetica', 10, 'italic'))
        
        # Configure custom button styles
        self.style.configure('Primary.TButton', 
                           padding=10,
                           font=('Helvetica', 10, 'bold'))
        self.style.configure('Action.TButton',
                           padding=8,
                           font=('Helvetica', 10))
        
        # Configure frame styles
        self.style.configure('Card.TFrame', padding=15)
        self.style.configure('Controls.TLabelframe', padding=15)
        
        self.original_image = None
        self.processed_image = None
        self.original_path = None
        self.cv2_image = None
        
        self.processing_queue = queue.Queue()
        self.is_processing = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20", style='Card.TFrame')
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, 
                              text="Advanced Background Remover",
                              style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Action buttons frame with gradient background
        action_frame = ttk.Frame(main_frame, style='Card.TFrame')
        action_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        action_frame.grid_columnconfigure(1, weight=1)
        
        # Choose file button
        self.choose_btn = ttk.Button(
            action_frame,
            text="Choose Image",
            command=self.choose_file,
            style='Primary.TButton'
        )
        self.choose_btn.grid(row=0, column=0, padx=5)
        
        # Process button
        self.process_btn = ttk.Button(
            action_frame,
            text="Remove Background",
            command=self.start_processing,
            state='disabled',
            style='Action.TButton'
        )
        self.process_btn.grid(row=0, column=1, padx=5)
        
        # Save file button
        self.save_btn = ttk.Button(
            action_frame,
            text="Save Image",
            command=self.save_file,
            state='disabled',
            style='Action.TButton'
        )
        self.save_btn.grid(row=0, column=2, padx=5)
        
        # Progress bar with custom styling
        self.progress = ttk.Progressbar(
            action_frame,
            orient="horizontal",
            length=150,
            mode="indeterminate",
            style='Horizontal.TProgressbar'
        )
        self.progress.grid(row=0, column=3, padx=10)
        
        # Controls section
        controls_frame = ttk.LabelFrame(
            main_frame,
            text="Processing Controls",
            style='Controls.TLabelframe',
            padding="15"
        )
        controls_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        
        # Grid configuration for controls
        for i in range(3):
            controls_frame.grid_columnconfigure(i*2 + 1, weight=1)
        
        # Threshold control
        self.create_slider_control(
            controls_frame, 0,
            "Threshold:", "threshold_var",
            0.8, "Adjusts the sensitivity of background detection"
        )
        
        # Edge sensitivity control
        self.create_slider_control(
            controls_frame, 1,
            "Edge Sensitivity:", "edge_var",
            0.5, "Controls the detection of edges between foreground and background"
        )
        
        # Detail preservation control
        self.create_slider_control(
            controls_frame, 2,
            "Detail Level:", "detail_var",
            0.7, "Adjusts the preservation of fine details in the image"
        )
        
        # Preview section
        preview_frame = ttk.Frame(main_frame)
        preview_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 20))
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(1, weight=1)
        
        # Original image preview
        original_container = ttk.Frame(preview_frame, style='Card.TFrame')
        original_container.grid(row=0, column=0, padx=10, sticky="nsew")
        
        ttk.Label(original_container, 
                 text="Original Image",
                 style='Header.TLabel').pack(pady=(0, 10))
        
        self.original_preview = ttk.Label(original_container)
        self.original_preview.pack()
        
        # Processed image preview
        processed_container = ttk.Frame(preview_frame, style='Card.TFrame')
        processed_container.grid(row=0, column=1, padx=10, sticky="nsew")
        
        ttk.Label(processed_container,
                 text="Processed Image",
                 style='Header.TLabel').pack(pady=(0, 10))
        
        self.processed_preview = ttk.Label(processed_container)
        self.processed_preview.pack()
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Ready to process images",
            style='Status.TLabel'
        )
        self.status_label.grid(row=4, column=0, pady=(0, 10))

    def create_slider_control(self, parent, position, label_text, var_name, default_value, tooltip_text):
        frame = ttk.Frame(parent)
        frame.grid(row=position, column=0, columnspan=2, sticky="ew", pady=5)
        frame.grid_columnconfigure(1, weight=1)
        
        label = ttk.Label(frame, text=label_text, style='Info.TLabel')
        label.grid(row=0, column=0, padx=(0, 10))
        
        setattr(self, var_name, tk.DoubleVar(value=default_value))
        slider = ttk.Scale(
            frame,
            from_=0.0,
            to=1.0,
            orient='horizontal',
            variable=getattr(self, var_name),
            length=200
        )
        slider.grid(row=0, column=1, sticky="ew")
        
        # Tooltip
        tooltip = ttk.Label(frame, text=tooltip_text, style='Status.TLabel')
        tooltip.grid(row=1, column=0, columnspan=2, pady=(2, 0))
    def choose_file(self):
        file_types = [
            ('Image files', '*.png *.jpg *.jpeg'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(filetypes=file_types)
        if filename:
            self.original_path = filename
            self.load_original_image(filename)
            self.process_btn.config(state='normal')
            self.save_btn.config(state='disabled')
            self.status_label.config(text="Image loaded successfully")

    def load_original_image(self, path):
        try:
            # Load and preprocess image
            image = Image.open(path)
            
            # Resize large images before preview
            max_size = (800, 800)
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            preview_size = (350, 350)
            preview_image = image.copy()
            preview_image.thumbnail(preview_size)
            photo = ImageTk.PhotoImage(preview_image)
            
            self.original_image = image
            self.original_preview.config(image=photo)
            self.original_preview.image = photo
            
            # Load image with OpenCV for processing
            self.cv2_image = cv2.imread(path)
            
            # Clear processed preview
            self.processed_preview.config(image='')
            self.processed_image = None
            
        except Exception as e:
            self.status_label.config(text=f"Error loading image: {str(e)}")
            return False
        return True

    def remove_background_improved(self, image):
        # Resize large images for processing
        max_size = 1500
        height, width = image.shape[:2]
        scale = 1.0
        
        if height > max_size or width > max_size:
            scale = max_size / max(height, width)
            image = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        
        # Enhanced preprocessing
        blur = cv2.GaussianBlur(image, (3, 3), 0)
        
        # Create initial mask
        mask = np.zeros(image.shape[:2], np.uint8)
        bgdModel = np.zeros((1,65), np.float64)
        fgdModel = np.zeros((1,65), np.float64)
        
        # Calculate rectangle with margin based on image content
        height, width = image.shape[:2]
        margin = int(min(width, height) * 0.1)
        rect = (margin, margin, width-margin, height-margin)
        
        # First pass of GrabCut
        cv2.grabCut(blur, mask, rect, bgdModel, fgdModel, 3, cv2.GC_INIT_WITH_RECT)
        
        # Edge detection for refinement
        edge_sensitivity = int(self.edge_var.get() * 100)
        detail_level = self.detail_var.get()
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, edge_sensitivity, edge_sensitivity * 2)
        
        # Create refined mask using edge information
        mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
        
        # Combine edge information with mask
        kernel = np.ones((3, 3), np.uint8)
        dilated_edges = cv2.dilate(edges, kernel, iterations=1)
        mask2 = cv2.bitwise_or(mask2, cv2.threshold(dilated_edges, 0, 1, cv2.THRESH_BINARY)[1])
        
        # Second pass of GrabCut with refined mask
        mask[mask2 == 1] = 1
        cv2.grabCut(image, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)
        
        # Create final mask with threshold
        thresh_value = self.threshold_var.get()
        mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
        
        # Apply detail preservation
        if detail_level > 0.5:
            kernel_size = max(1, int((1 - detail_level) * 5))
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernel)
        
        # Color-based refinement
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        saturation = hsv[:,:,1]
        mask2 = cv2.bitwise_and(mask2, cv2.threshold(saturation, 30, 1, cv2.THRESH_BINARY)[1])
        
        # Apply mask to image
        result = image * mask2[:,:,np.newaxis]
        
        # Create alpha channel
        b, g, r = cv2.split(result)
        alpha = np.where((b == 0) & (g == 0) & (r == 0), 0, 255).astype('uint8')
        
        # Final refinement
        alpha = cv2.morphologyEx(alpha, cv2.MORPH_CLOSE, np.ones((2, 2), np.uint8))
        
        # Resize back to original size if scaled
        if scale != 1.0:
            b = cv2.resize(b, (width, height), interpolation=cv2.INTER_LINEAR)
            g = cv2.resize(g, (width, height), interpolation=cv2.INTER_LINEAR)
            r = cv2.resize(r, (width, height), interpolation=cv2.INTER_LINEAR)
            alpha = cv2.resize(alpha, (width, height), interpolation=cv2.INTER_LINEAR)
        
        return cv2.merge((b, g, r, alpha))

    def start_processing(self):
        if not self.is_processing and self.cv2_image is not None:
            self.is_processing = True
            self.process_btn.config(state='disabled')
            self.choose_btn.config(state='disabled')
            self.save_btn.config(state='disabled')
            self.progress.start(10)
            self.status_label.config(text="Processing image...")
            
            thread = Thread(target=self.process_image_thread)
            thread.daemon = True
            thread.start()
            
            self.root.after(100, self.check_processing_complete)

    def process_image_thread(self):
        try:
            result_rgba = self.remove_background_improved(self.cv2_image.copy())
            self.processing_queue.put(("success", result_rgba))
        except Exception as e:
            self.processing_queue.put(("error", str(e)))

    def check_processing_complete(self):
        try:
            if not self.processing_queue.empty():
                status, result = self.processing_queue.get_nowait()
                
                if status == "success":
                    result_pil = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
                    result_pil.thumbnail((350, 350))
                    photo = ImageTk.PhotoImage(result_pil)
                    
                    self.processed_image = result
                    self.processed_preview.config(image=photo)
                    self.processed_preview.image = photo
                    
                    self.status_label.config(text="Background removed successfully")
                    self.save_btn.config(state='normal')
                else:
                    self.status_label.config(text=f"Error: {result}")
                
                self.progress.stop()
                self.is_processing = False
                self.process_btn.config(state='normal')
                self.choose_btn.config(state='normal')
                return
            
            self.root.after(100, self.check_processing_complete)
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            self.progress.stop()
            self.is_processing = False
            self.process_btn.config(state='normal')
            self.choose_btn.config(state='normal')

    def save_file(self):
        if self.processed_image is not None:
            directory = os.path.dirname(self.original_path)
            filename = os.path.basename(self.original_path)
            name, ext = os.path.splitext(filename)
            default_name = f"{name}_no_bg.png"
            
            file_path = filedialog.asksaveasfilename(
                initialdir=directory,
                initialfile=default_name,
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")]
            )
            
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                self.status_label.config(text=f"Image saved to: {file_path}")

def main():
    root = tk.Tk()
    app = BackgroundRemoverGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()