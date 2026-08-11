"""
Base window V2 Added style configuration to fix missing style errors.

Things that I can do better:
- scrollable() still uses bind_all - affects all windows globally
- Canvas scrolling only works on Windows
- No cleanup of mousewheel bindings when window closes
- Scrollbar appearance may vary by platform
- Window focus issues when multiple windows open
"""

from tkinter import ttk, Canvas, Scrollbar
from gui.gui_helpers import create_window


class BaseWindow:
    """Simple base class for all game windows"""
    
    def __init__(self, parent, game, on_update, title, width=500, height=500):
        self.parent = parent
        self.game = game
        self.on_update = on_update
        
        # FIXED: Define styles before creating window widgets
        self._setup_styles()
        
        self.win = create_window(parent, title, width, height)
        self.win.configure(bg="#0a0a0a")
        self.win.resizable(True, True)
    
    def _setup_styles(self):
        """
        Define all ttk styles to avoid missing style errors.
        FIXED: This method now defines all styles used by the class.
        """
        style = ttk.Style()
        style.theme_use("clam")  # Required for custom styles to work
        
        # Frame styles - FIXED: Now defined
        style.configure("Dark.TFrame", background="#0a0a0a")
        style.configure("Card.TFrame", background="#1a1a1a", relief="ridge", borderwidth=2)
        style.configure("CardInner.TFrame", background="#1a1a1a")
        
        # Button styles - FIXED: All button styles now defined
        style.configure("White.TButton", font=("Segoe UI", 11), 
                       foreground="white", background="#333333")
        style.configure("Green.TButton", font=("Segoe UI", 11, "bold"),
                       foreground="white", background="#00cc44")
        style.configure("Blue.TButton", font=("Segoe UI", 11, "bold"),
                       foreground="white", background="#0088ff")
        style.configure("Orange.TButton", font=("Segoe UI", 11, "bold"),
                       foreground="white", background="#ff8800")
        style.configure("Red.TButton", font=("Segoe UI", 11, "bold"),
                       foreground="white", background="#cc0000")
        style.configure("Purple.TButton", font=("Segoe UI", 11, "bold"),
                       foreground="white", background="#8800cc")
        style.configure("Pink.TButton", font=("Segoe UI", 11, "bold"),
                       foreground="white", background="#ff1493")
        style.configure("Vacation.TButton", font=("Segoe UI", 11, "bold"),
                       foreground="white", background="#ffd700")
    
    def add_title(self, text, color="#ffffff"):
        """Add a title to the window with a separator line"""
        ttk.Label(self.win, text=text, font=("Segoe UI", 20, "bold"),
                 foreground=color, background="#0a0a0a").pack(pady=(10, 5))
        ttk.Separator(self.win, orient="horizontal").pack(fill="x", padx=20, pady=5)
    
    def add_close(self, text="Close", style="White.TButton"):
        """Add a close button that destroys the window"""
        # FIXED: Styles now exist, no more AttributeError
        frame = ttk.Frame(self.win, style="Dark.TFrame")
        frame.pack(fill="x", pady=(15, 5), padx=20)
        ttk.Button(frame, text=text, command=self.win.destroy, style=style).pack()
    
    def card(self, parent, content_func):
        """Create a styled card for grouping content"""
        # FIXED: Styles now exist
        card = ttk.Frame(parent, style="Card.TFrame")
        card.pack(fill="x", pady=5)
        inner = ttk.Frame(card, style="CardInner.TFrame")
        inner.pack(fill="x", padx=15, pady=10)
        content_func(inner)
        return inner
    
    def scrollable(self, items, create_func):
        """
        Create a scrollable area with mousewheel support.
        BUG: Still uses bind_all - affects ALL windows globally.
        """
        container = ttk.Frame(self.win, style="Dark.TFrame")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        
        canvas = Canvas(container, bg="#0a0a0a", highlightthickness=0)
        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        inner = ttk.Frame(canvas, style="Dark.TFrame")
        canvas.create_window((0, 0), window=inner, anchor="nw")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def on_configure(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        def on_width(e):
            canvas.itemconfig(canvas.create_window((0, 0), window=inner, anchor="nw"), width=e.width)
        def on_scroll(e):
            # BUG: Windows only - delta/120 doesn't work on Mac/Linux
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        
        inner.bind("<Configure>", on_configure)
        canvas.bind("<Configure>", on_width)
        canvas.bind_all("<MouseWheel>", on_scroll)  # BUG: Still global!
        
        for item in items:
            create_func(inner, item)
        
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))