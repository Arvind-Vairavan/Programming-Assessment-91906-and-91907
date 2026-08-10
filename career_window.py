"""
career V2 Fixed experience display and button layout.

Things that can be done better:

* Salary payment on age-up still not working correctly
* Work button experience increment (1 month) doesn't match age-up (1 year)
* Promotion requirements may not match displayed experience
* No confirmation when selecting a job
  """

from tkinter import ttk, messagebox
from gui.base_window import BaseWindow
from data.constants import JOBS

class CareerWindow(BaseWindow):
    def init(self, parent, game, on_update):
        super().init(parent, game, on_update, "Career", 500, 550)
        self._setup()

    def _setup(self):
        self.add_title("CAREER", "#00ccff")
        char = self.game.get_character()
        
        # FIXED: Display experience correctly using //12 for years
        exp_years = char.job_experience // 12 if char and char.job else 0
        info = f"Current: {char.job} | Salary: ${JOBS[char.job]['salary']:,}/year | Exp: {exp_years}y" if char and char.job else "Currently Unemployed"
        ttk.Label(self.win, text=info, font=("Segoe UI", 12), foreground="#cccccc", background="#0a0a0a").pack(pady=5)
        ttk.Label(self.win, text=f"${char.money if char else 0:,}", font=("Segoe UI", 12), foreground="#00ff88", background="#0a0a0a").pack(pady=(0, 5))
        ttk.Separator(self.win, orient="horizontal").pack(fill="x", pady=10)
        
        # FIXED: Better button layout with consistent spacing
        row = ttk.Frame(self.win, style="Dark.TFrame")
        row.pack(fill="x", pady=5)
        text = "Find New Job" if char and char.job else "Find Job"
        ttk.Button(row, text=f"{text}", command=self._job_select, style="Blue.TButton").pack(side="left", padx=5, expand=True, fill="x")
        
        if char and char.job:
            ttk.Button(row, text="Work", command=self._work, style="Green.TButton").pack(side="left", padx=5, expand=True, fill="x")
            row2 = ttk.Frame(self.win, style="Dark.TFrame")
            row2.pack(fill="x", pady=5)
            ttk.Button(row2, text="Promote", command=self._promote, style="Purple.TButton").pack(side="left", padx=5, expand=True, fill="x")
            ttk.Button(row2, text="Resign", command=self._resign, style="Red.TButton").pack(side="left", padx=5, expand=True, fill="x")
        
        ttk.Separator(self.win, orient="horizontal").pack(fill="x", pady=10)
        self._show_job()
        self.add_close()

    def _show_job(self):
        char = self.game.get_character()
        if not char or not char.job:
            ttk.Label(self.win, text="No job. Click 'Find Job' to start!", font=("Segoe UI", 12), foreground="#888888", background="#0a0a0a").pack(pady=20)
            return
        emojis = {"Retail":"","Teacher":"","Developer":"","Doctor":"","CEO":"","Artist":"","Chef":"","Musician":"","Athlete":""}
        self.card(self.win, lambda i: self._job_card(i, char, emojis))

    def _job_card(self, inner, char, emojis):
        # FIXED: Consistent experience display
        exp_years = char.job_experience // 12
        ttk.Label(inner, text=f"{emojis.get(char.job, '')} {char.job}", font=("Segoe UI", 16, "bold"), foreground="white", background="#1a1a1a").pack(anchor="w")
        ttk.Label(inner, text=f"${JOBS[char.job]['salary']:,}/year", font=("Segoe UI", 13), foreground="#ffd700", background="#1a1a1a").pack(anchor="w", pady=(5, 0))
        ttk.Label(inner, text=f"{exp_years} years", font=("Segoe UI", 12), foreground="#00ccff", background="#1a1a1a").pack(anchor="w", pady=(3, 0))

    def _job_select(self):
        JobSelectWindow(self.win, self.game, self.on_update)

    def _work(self): self._exec(self.game.career.work)
    def _promote(self): self._exec(self.game.career.promote_manual)
    def _resign(self):
        if messagebox.askyesno("Resign", "Sure?"):
            self._exec(self.game.career.resign)

    def _exec(self, func):
        r = func()
        self.win.destroy()
        self.on_update()
        if r and isinstance(r, str): messagebox.showinfo("Result", r)


class JobSelectWindow(BaseWindow):
    def init(self, parent, game, on_update):
        super().init(parent, game, on_update, "Career Opportunities", 550, 600)
        self._setup()


    def _setup(self):
        self.add_title("CAREER OPPORTUNITIES", "#00ccff")
        char = self.game.get_character()
        ttk.Label(self.win, text=f"Current: {char.job if char and char.job else 'Unemployed'}", font=("Segoe UI", 11, "italic"), foreground="#888888", background="#0a0a0a").pack()
        ttk.Label(self.win, text=f"${char.money if char else 0:,}", font=("Segoe UI", 12), foreground="#00ff88", background="#0a0a0a").pack(pady=(5, 10))
        ttk.Separator(self.win, orient="horizontal").pack(fill="x", padx=30, pady=5)
        
        emojis = {"Retail":"","Teacher":"","Developer":"","Doctor":"","CEO":"","Artist":"","Chef":"","Musician":"","Athlete":""}
        self.scrollable(list(JOBS.items()), lambda p, i: self._job_card(p, i, emojis))
        self.add_close(" Cancel")

    def _job_card(self, parent, item, emojis):
        name, data = item
        self.card(parent, lambda i: self._card_content(i, name, data, emojis))

    def _card_content(self, inner, name, data, emojis):
        ttk.Label(inner, text=f"{emojis.get(name, '')} {name}", font=("Segoe UI", 15, "bold"), foreground="white", background="#1a1a1a").pack(anchor="w")
        ttk.Label(inner, text=f"${data['salary']:,}/year", font=("Segoe UI", 12), foreground="#ffd700", background="#1a1a1a").pack(anchor="w", pady=(3, 0))
        ttk.Label(inner, text=f"~${data['salary']//12:,}/month", font=("Segoe UI", 10), foreground="#888888", background="#1a1a1a").pack(anchor="w", pady=(2, 0))
        frame = ttk.Frame(inner, style="CardInner.TFrame")
        frame.pack(side="right", padx=(10, 0))
        ttk.Button(frame, text="SELECT", command=lambda: self._select(name), style="Green.TButton").pack(anchor="center", pady=5)

    def _select(self, name):
        char = self.game.get_character()
        if char:
            char.job = name
            char.job_experience = 0  # Reset experience on job change
            char.last_promotion_age = char.age
            self.win.destroy()
            self.parent.destroy()
            self.on_update()
            messagebox.showinfo("Career Started", f"Started as {name}!")

