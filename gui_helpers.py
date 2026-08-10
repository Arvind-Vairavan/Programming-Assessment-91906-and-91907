"""
Reusable GUI helper functions to avoid code duplication.
this is the second version which is also the final version where everything works 
"""

from tkinter import Toplevel, ttk, StringVar, messagebox


def create_window(parent, title, width=500, height=500):
    """
    Create a centered popup window.
    """
    win = Toplevel(parent)
    win.title(title)
    win.geometry(f"{width}x{height}")
    win.configure(bg="black")
    win.transient(parent)
    win.grab_set()
    
    # Center window
    x = (win.winfo_screenwidth() - width) // 2
    y = (win.winfo_screenheight() - height) // 2
    win.geometry(f"+{x}+{y}")
    return win


def add_title(parent, text, color="white", size=20):
    """Add a title to a window"""
    ttk.Label(parent, text=text, font=("Helvetica", size, "bold"), foreground=color, background="black").pack(pady=20)


def add_close_button(parent):
    """Add a close button to a window"""
    ttk.Button(parent, text="Close", command=parent.destroy, style="Dialog.TButton").pack(pady=15)


def create_button(parent, text, command, style="Blue.TButton", pack_kwargs=None):
    """Create a styled button"""
    btn = ttk.Button(parent, text=text, command=command, style=style)
    if pack_kwargs:
        btn.pack(**pack_kwargs)
    else:
        btn.pack(pady=4, padx=10, fill="x")
    return btn


def button(parent, text, command, style="Blue.TButton", **kwargs):
    """Simple button creator with kwargs support"""
    btn = ttk.Button(parent, text=text, command=command, style=style)
    if kwargs:
        btn.pack(**kwargs)
    else:
        btn.pack(pady=4, padx=10, fill="x")
    return btn


def create_section(parent, title, content=None, buttons=None):
    """
    Create a labeled section with optional content and buttons.
    """
    frame = ttk.LabelFrame(parent, text=title, style="Dark.TFrame")
    frame.pack(fill="x", padx=20, pady=10)
    
    if content:
        display_text = content() if callable(content) else content
        ttk.Label(frame, text=display_text, font=("Helvetica", 12), foreground="#cccccc", background="black", justify="left").pack(pady=5, padx=10)
    
    if buttons:
        for btn in buttons:
            create_button(frame, btn["text"], btn["action"], btn.get("style", "Blue.TButton"))


def create_stats_display(parent, stats_text):
    """Create a stats display section"""
    ttk.Label(parent, text=stats_text, font=("Helvetica", 12), foreground="#00ccff", background="black", justify="left").pack(pady=5, padx=40)


def create_item_list(parent, items, action_func, label_format=None, button_text="Select"):
    '''
    Create a list of items with action buttons.
    '''
    for item in items:
        frame = ttk.Frame(parent, style="Dark.TFrame")
        frame.pack(fill="x", pady=5)
        
        # Format the label
        if label_format:
            label = label_format.format(**item)
        else:
            label = f"{item['name']} ${item.get('cost', 0):,}"
            if 'happiness' in item:
                label += f" +{item['happiness']}"
            if 'reward' in item:
                label += f" Reward: ${item['reward']:,}"
            if 'risk' in item:
                label += f" Risk: {item['risk']}%"
        
        ttk.Label(frame, text=label, font=("Helvetica", 11), foreground="#cccccc", background="black").pack(side="left", padx=10)
        
        # Create action button - FIXED: default argument binds current item
        if action_func:
            cmd = lambda i=item: action_func(i)  # Fixed: default arg binds correctly
            ttk.Button(frame, text=button_text, command=cmd, style="Green.TButton").pack(side="right", padx=10)