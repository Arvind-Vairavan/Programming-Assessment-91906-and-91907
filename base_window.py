"""
base window V1 - starting with basic window features.

Things that can be done better:
- Styles (Dark.TFrame, Card.TFrame, etc.) are not defined - will cause AttributeError
- scrollable() uses bind_all which affects ALL windows globally
- Canvas scrolling only works on Windows (uses delta/120)
- No error handling for missing styles or invalid items
- Window resizing may cause layout issues


"""

from tkinter import ttk, Canvas, Scrollbar
from gui.gui_helpers import create_window


class BaseWindow:
    """Simple base class for all game windows"""
    
    def __init__(self, parent, game, on_update, title, width=500, height=500):
        # Store references for later use
        self.parent = parent
        self.game = game
        self.on_update = on_update
        
        # Create the actual window using helper function
        # BUG: Styles not defined yet - will cause errors when adding widgets
        self.win = create_window(parent, title, width, height)
        self.win.configure(bg="#0a0a0a")  # Dark theme background
        self.win.resizable(True, True)  # Allow window resizing
    
    def add_title(self, text, color="#ffffff"):
        """
        Add a title to the window with a separator line.
        BUG: Uses style "Dark.TFrame" which doesn't exist yet.
        """
        # Title label with custom color
        ttk.Label(self.win, text=text, font=("Segoe UI", 20, "bold"),
                 foreground=color, background="#0a0a0a").pack(pady=(10, 5))
        # Separator line for visual division
        ttk.Separator(self.win, orient="horizontal").pack(fill="x", padx=20, pady=5)
    
    def add_close(self, text="Close", style="White.TButton"):
        """
        Add a close button that destroys the window.
        BUG: Uses styles "Dark.TFrame" and "White.TButton" which don't exist.
        """
        # Frame to contain the button for better layout control
        frame = ttk.Frame(self.win, style="Dark.TFrame")  # BUG: Style not defined
        frame.pack(fill="x", pady=(15, 5), padx=20)
        # Button that closes the window when clicked
        ttk.Button(frame, text=text, command=self.win.destroy, style=style).pack()
    
    def card(self, parent, content_func):
        """
        Create a styled card for grouping content.
        BUG: Uses styles "Card.TFrame" and "CardInner.TFrame" which don't exist.
        """
        # Outer card with border
        card = ttk.Frame(parent, style="Card.TFrame")  # BUG: Style not defined
        card.pack(fill="x", pady=5)
        # Inner frame for content with padding
        inner = ttk.Frame(card, style="CardInner.TFrame")  # BUG: Style not defined
        inner.pack(fill="x", padx=15, pady=10)
        # Call the content function to add widgets
        content_func(inner)
        return inner
    
    def scrollable(self, items, create_func):
        """
        Create a scrollable area with mousewheel support.
        BUG: Uses bind_all which affects ALL windows.
        BUG: Scrolling only works on Windows systems.
        """
        # Container frame
        container = ttk.Frame(self.win, style="Dark.TFrame")  # BUG: Style not defined
        container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Canvas for scrolling content
        canvas = Canvas(container, bg="#0a0a0a", highlightthickness=0)
        # Scrollbar linked to canvas
        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Inner frame that holds the actual content
        inner = ttk.Frame(canvas, style="Dark.TFrame")
        # Add the inner frame to the canvas as a window
        canvas.create_window((0, 0), window=inner, anchor="nw")
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # BUG: bind_all affects ALL windows, not just this one
        def on_configure(e):
            """Update scroll region when content changes size"""
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def on_width(e):
            """Update canvas width when resized"""
            canvas.itemconfig(canvas.create_window((0, 0), window=inner, anchor="nw"), width=e.width)
        
        def on_scroll(e):
            """Handle mousewheel scrolling - BUG: Windows only (delta/120)"""
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        
        # Bind events
        inner.bind("<Configure>", on_configure)
        canvas.bind("<Configure>", on_width)
        canvas.bind_all("<MouseWheel>", on_scroll)  # BUG: Global binding!
        
        # Create each item using the provided function
        for item in items:
            create_func(inner, item)
        
        # Finalize layout
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))