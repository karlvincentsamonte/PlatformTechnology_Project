import random
import tkinter as tk
from contextlib import redirect_stdout
from io import StringIO
from tkinter import messagebox, ttk

# Import existing modules without modifying them
from FIFO import fifo
from LRU import lru
from Optimal import optimal
from Result import compare_results, display_results


# ==============================
# COLOR PALETTE - SOFT ROSE
# ==============================

BG = "#FCE4EC"
PANEL = "#FFF5F8"
CARD = "#FFFFFF"
INPUT_BG = "#F8BBD0"
ACCENT = "#EC407A"
ACCENT_HOVER = "#D81B60"
SECONDARY_BTN = "#F48FB1"
HIT_COLOR = "#2E7D32"
HIT_BG = "#E8F5E9"
FAULT_COLOR = "#C62828"
FAULT_BG = "#FFEBEE"
TEXT = "#6A1B4D"
MUTED = "#9C4A73"
BORDER = "#F3B6CC"


class PageReplacementGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Page Replacement Simulator")
        self.root.geometry("1120x780")
        self.root.minsize(920, 660)
        self.root.configure(bg=BG)

        self._configure_styles()
        self._build_ui()
        self._bind_shortcuts()
        self._show_welcome_message()

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TCombobox",
            fieldbackground=INPUT_BG,
            background=INPUT_BG,
            foreground=TEXT,
            arrowcolor=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=6,
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", INPUT_BG)],
            foreground=[("readonly", TEXT)],
            selectbackground=[("readonly", INPUT_BG)],
            selectforeground=[("readonly", TEXT)],
        )

        style.configure(
            "Vertical.TScrollbar",
            background=INPUT_BG,
            troughcolor=PANEL,
            bordercolor=PANEL,
            arrowcolor=TEXT,
        )
        style.configure(
            "Horizontal.TScrollbar",
            background=INPUT_BG,
            troughcolor=PANEL,
            bordercolor=PANEL,
            arrowcolor=TEXT,
        )

    def _build_ui(self) -> None:
        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=28, pady=(20, 10))

        title_row = tk.Frame(header, bg=BG)
        title_row.pack(fill="x")

        tk.Label(
            title_row,
            text="Page Replacement Simulator",
            font=("Segoe UI", 22, "bold"),
            bg=BG,
            fg=TEXT,
        ).pack(side="left")

        tk.Label(
            title_row,
            text="FIFO  •  LRU  •  OPTIMAL",
            font=("Segoe UI", 10, "bold"),
            bg=INPUT_BG,
            fg=TEXT,
            padx=10,
            pady=4,
        ).pack(side="right", pady=4)

        tk.Label(
            header,
            text="Simulate memory page faults, hits, and replacement behavior step by step.",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED,
        ).pack(anchor="w", pady=(3, 0))

        # Input Card
        input_card = tk.Frame(
            self.root,
            bg=PANEL,
            padx=20,
            pady=16,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        input_card.pack(fill="x", padx=28, pady=8)

        tk.Label(
            input_card,
            text="SIMULATION SETTINGS",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL,
            fg=ACCENT,
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

        # Page Reference String
        tk.Label(
            input_card,
            text="Page Reference String",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL,
            fg=TEXT,
        ).grid(row=1, column=0, sticky="w", pady=(0, 4))

        self.page_entry = tk.Entry(
            input_card,
            font=("Consolas", 11),
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        self.page_entry.grid(row=2, column=0, sticky="ew", padx=(0, 14), ipady=8)
        self.page_entry.insert(0, "1 2 3 4 1 2 5 1 2 3 4 5")

        # Frame Count
        tk.Label(
            input_card,
            text="Frames",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL,
            fg=TEXT,
        ).grid(row=1, column=1, sticky="w", pady=(0, 4))

        self.frame_entry = tk.Entry(
            input_card,
            font=("Consolas", 11),
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            width=10,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=ACCENT,
        )
        self.frame_entry.grid(row=2, column=1, sticky="ew", padx=(0, 14), ipady=8)
        self.frame_entry.insert(0, "3")

        # Algorithm Selector
        tk.Label(
            input_card,
            text="Algorithm",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL,
            fg=TEXT,
        ).grid(row=1, column=2, sticky="w", pady=(0, 4))

        self.algorithm_var = tk.StringVar(value="Run All Algorithms")
        self.algorithm_menu = ttk.Combobox(
            input_card,
            textvariable=self.algorithm_var,
            values=["Run All Algorithms", "FIFO", "LRU", "Optimal"],
            state="readonly",
            font=("Segoe UI", 10),
            width=20,
        )
        self.algorithm_menu.grid(row=2, column=2, sticky="ew", ipady=3)

        input_card.columnconfigure(0, weight=4)
        input_card.columnconfigure(1, weight=1)
        input_card.columnconfigure(2, weight=2)

        # Action & Helper Bar
        action_bar = tk.Frame(self.root, bg=BG)
        action_bar.pack(fill="x", padx=28, pady=(6, 8))

        self.run_btn = tk.Button(
            action_bar,
            text="▶  Run Simulation",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT,
            fg="#FFFFFF",
            activebackground=ACCENT_HOVER,
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=9,
            command=self.run_simulation,
        )
        self.run_btn.pack(side="left", padx=(0, 8))

        self.random_btn = tk.Button(
            action_bar,
            text="🎲 Random String",
            font=("Segoe UI", 10, "bold"),
            bg=INPUT_BG,
            fg=TEXT,
            activebackground=SECONDARY_BTN,
            activeforeground=TEXT,
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=9,
            command=self.generate_random_pages,
        )
        self.random_btn.pack(side="left", padx=(0, 8))

        self.clear_btn = tk.Button(
            action_bar,
            text="Clear",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL,
            fg=TEXT,
            activebackground=INPUT_BG,
            activeforeground=TEXT,
            relief="flat",
            highlightbackground=BORDER,
            highlightthickness=1,
            cursor="hand2",
            padx=14,
            pady=8,
            command=self.clear_fields,
        )
        self.clear_btn.pack(side="left")

        # Metrics Summary Strip
        metrics_row = tk.Frame(self.root, bg=BG)
        metrics_row.pack(fill="x", padx=28, pady=(0, 8))

        _, self.hits_val = self._create_metric_card(metrics_row, "PAGE HITS", "—")
        _, self.faults_val = self._create_metric_card(metrics_row, "PAGE FAULTS", "—")
        _, self.ratio_val = self._create_metric_card(metrics_row, "HIT RATIO", "—")

        # Results Card
        results_card = tk.Frame(
            self.root,
            bg=PANEL,
            padx=16,
            pady=14,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        results_card.pack(fill="both", expand=True, padx=28, pady=(0, 6))

        tk.Label(
            results_card,
            text="SIMULATION OUTPUT & COMPARISON",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL,
            fg=ACCENT,
        ).pack(anchor="w", pady=(0, 8))

        text_container = tk.Frame(results_card, bg=CARD)
        text_container.pack(fill="both", expand=True)

        v_scroll = ttk.Scrollbar(text_container, orient="vertical")
        h_scroll = ttk.Scrollbar(text_container, orient="horizontal")

        self.result_text = tk.Text(
            text_container,
            font=("Consolas", 10),
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            wrap="none",
            padx=14,
            pady=12,
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set,
        )

        v_scroll.config(command=self.result_text.yview)
        h_scroll.config(command=self.result_text.xview)

        h_scroll.pack(side="bottom", fill="x")
        v_scroll.pack(side="right", fill="y")
        self.result_text.pack(side="left", fill="both", expand=True)

        self.result_text.tag_configure("hit", foreground=HIT_COLOR, background=HIT_BG)
        self.result_text.tag_configure("fault", foreground=FAULT_COLOR, background=FAULT_BG)
        self.result_text.tag_configure(
            "header", foreground=ACCENT, font=("Consolas", 10, "bold")
        )

        # Status Bar
        self.status_label = tk.Label(
            self.root,
            text="Ready — Press Enter to run simulation.",
            font=("Segoe UI", 9),
            bg=BG,
            fg=MUTED,
        )
        self.status_label.pack(anchor="w", padx=30, pady=(0, 12))

    def _create_metric_card(self, parent: tk.Frame, label: str, value: str):
        card = tk.Frame(
            parent,
            bg=PANEL,
            padx=14,
            pady=8,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        card.pack(side="left", fill="x", expand=True, padx=(0, 8))

        tk.Label(
            card,
            text=label,
            font=("Segoe UI", 8, "bold"),
            bg=PANEL,
            fg=MUTED,
        ).pack(anchor="w")

        val_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 13, "bold"),
            bg=PANEL,
            fg=TEXT,
        )
        val_label.pack(anchor="w", pady=(2, 0))
        return card, val_label

    def _bind_shortcuts(self) -> None:
        self.root.bind("<Return>", lambda _event: self.run_simulation())
        self.root.bind("<Escape>", lambda _event: self.clear_fields())

    def _show_welcome_message(self) -> None:
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(
            tk.END,
            "Welcome to Page Replacement Simulator!\n\n"
            "1. Enter a page reference string (e.g., 1 2 3 4 1 2 5 1 2 3 4 5)\n"
            "2. Enter a positive number of memory frames\n"
            "3. Choose an algorithm or 'Run All Algorithms'\n",
        )
        self.result_text.config(state="disabled")

    def generate_random_pages(self) -> None:
        length = random.randint(10, 16)
        max_page = random.randint(4, 7)
        sample = [str(random.randint(1, max_page)) for _ in range(length)]
        self.page_entry.delete(0, tk.END)
        self.page_entry.insert(0, " ".join(sample))
        self.status_label.config(
            text=f"Generated {length} random page references (1–{max_page}).",
            fg=TEXT,
        )

    def _parse_inputs(self):
        try:
            frame_size = int(self.frame_entry.get().strip())
            if frame_size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Frame Count",
                "Please enter a whole number greater than 0 for frames.",
            )
            return None

        raw_pages = self.page_entry.get().replace(",", " ").split()
        if not raw_pages:
            messagebox.showerror(
                "Missing Page References",
                "Please enter at least one page number.",
            )
            return None

        try:
            pages = [int(p) for p in raw_pages]
        except ValueError:
            messagebox.showerror(
                "Invalid Page Reference",
                "Page references must be valid integers separated by spaces or commas.",
            )
            return None

        return frame_size, pages

    def run_simulation(self) -> None:
        parsed = self._parse_inputs()
        if not parsed:
            return

        frame_size, pages = parsed
        choice = self.algorithm_var.get()
        buffer = StringIO()

        try:
            with redirect_stdout(buffer):
                if choice == "FIFO":
                    res = fifo(pages, frame_size)
                    display_results("FIFO", res, len(pages))
                    self._update_metrics_single(res[0], res[1], len(pages))

                elif choice == "LRU":
                    res = lru(pages, frame_size)
                    display_results("LRU", res, len(pages))
                    self._update_metrics_single(res[0], res[1], len(pages))

                elif choice == "Optimal":
                    res = optimal(pages, frame_size)
                    display_results("OPTIMAL", res, len(pages))
                    self._update_metrics_single(res[0], res[1], len(pages))

                else:
                    fifo_res = fifo(pages, frame_size)
                    lru_res = lru(pages, frame_size)
                    opt_res = optimal(pages, frame_size)

                    display_results("FIFO", fifo_res, len(pages))
                    display_results("LRU", lru_res, len(pages))
                    display_results("OPTIMAL", opt_res, len(pages))
                    compare_results(fifo_res, lru_res, opt_res)
                    self._update_metrics_all(fifo_res, lru_res, opt_res, len(pages))

            self._render_output(buffer.getvalue())
            self.status_label.config(
                text=f"Completed '{choice}' with {frame_size} frames and {len(pages)} references.",
                fg=HIT_COLOR,
            )

        except Exception as exc:
            messagebox.showerror("Simulation Error", str(exc))
            self.status_label.config(
                text="Simulation encountered an error.",
                fg=FAULT_COLOR,
            )

    def _update_metrics_single(self, hits: int, faults: int, total: int) -> None:
        ratio = (hits / total * 100) if total else 0.0
        self.hits_val.config(text=str(hits))
        self.faults_val.config(text=str(faults))
        self.ratio_val.config(text=f"{ratio:.1f}%")

    def _update_metrics_all(self, f_res, l_res, o_res, total: int) -> None:
        self.hits_val.config(text=f"F:{f_res[0]}  L:{l_res[0]}  O:{o_res[0]}")
        self.faults_val.config(text=f"F:{f_res[1]}  L:{l_res[1]}  O:{o_res[1]}")
        best_hits = max(f_res[0], l_res[0], o_res[0])
        best_ratio = (best_hits / total * 100) if total else 0.0
        self.ratio_val.config(text=f"Up to {best_ratio:.1f}%")

    def _render_output(self, content: str) -> None:
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)

        for line in content.splitlines(keepends=True):
            stripped = line.strip()
            start_idx = self.result_text.index(tk.END)
            self.result_text.insert(tk.END, line)
            end_idx = self.result_text.index(tk.END)

            if stripped.startswith("===") or "ALGORITHM" in stripped or "COMPARISON" in stripped:
                self.result_text.tag_add("header", start_idx, end_idx)
            elif stripped.endswith("HIT"):
                self.result_text.tag_add("hit", start_idx, end_idx)
            elif stripped.endswith("FAULT"):
                self.result_text.tag_add("fault", start_idx, end_idx)

        self.result_text.config(state="disabled")

    def clear_fields(self) -> None:
        self.page_entry.delete(0, tk.END)
        self.frame_entry.delete(0, tk.END)
        self.algorithm_var.set("Run All Algorithms")
        self.hits_val.config(text="—")
        self.faults_val.config(text="—")
        self.ratio_val.config(text="—")

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state="disabled")

        self.status_label.config(text="Cleared inputs and output.", fg=MUTED)


if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementGUI(root)
    root.mainloop()