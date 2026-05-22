from pathlib import Path
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from scanner import scan_folder
from normalizer import enrich_file_record
from exporters.csv_exporter import export_to_csv
from exporters.excel_exporter import export_to_excel
from reporting import generate_summary


class MetadataIndexerGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Metadata Indexer")
        self.root.geometry("650x420")

        self.folder_path = tk.StringVar()
        self.export_csv = tk.BooleanVar(value=True)
        self.export_excel = tk.BooleanVar(value=True)

        self.build_ui()

    def build_ui(self) -> None:
        title = tk.Label(
            self.root,
            text="Metadata Indexer",
            font=("Segoe UI", 18, "bold"),
        )
        title.pack(pady=15)

        folder_frame = tk.Frame(self.root)
        folder_frame.pack(fill="x", padx=20)

        folder_entry = tk.Entry(
            folder_frame,
            textvariable=self.folder_path,
            font=("Segoe UI", 10),
        )
        folder_entry.pack(side="left", fill="x", expand=True)

        browse_button = tk.Button(
            folder_frame,
            text="Browse",
            command=self.browse_folder,
        )
        browse_button.pack(side="left", padx=8)

        options_frame = tk.LabelFrame(self.root, text="Export Options")
        options_frame.pack(fill="x", padx=20, pady=15)

        tk.Checkbutton(
            options_frame,
            text="Export CSV",
            variable=self.export_csv,
        ).pack(anchor="w", padx=10, pady=4)

        tk.Checkbutton(
            options_frame,
            text="Export Excel",
            variable=self.export_excel,
        ).pack(anchor="w", padx=10, pady=4)

        self.run_button = tk.Button(
            self.root,
            text="Run Metadata Scan",
            command=self.start_scan_thread,
            height=2,
            bg="#2d6cdf",
            fg="white",
        )
        self.run_button.pack(fill="x", padx=20, pady=10)

        self.status_label = tk.Label(
            self.root,
            text="Select a folder to begin.",
            anchor="w",
        )
        self.status_label.pack(fill="x", padx=20)

        self.output_box = tk.Text(self.root, height=10)
        self.output_box.pack(fill="both", expand=True, padx=20, pady=10)

    def browse_folder(self) -> None:
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            self.folder_path.set(selected_folder)

    def start_scan_thread(self) -> None:
        thread = threading.Thread(target=self.run_scan, daemon=True)
        thread.start()

    def run_scan(self) -> None:
        folder = self.folder_path.get().strip()

        if not folder:
            messagebox.showerror("Missing Folder", "Please select a folder to scan.")
            return

        if not self.export_csv.get() and not self.export_excel.get():
            messagebox.showerror(
                "Missing Export Option",
                "Please select CSV, Excel, or both.",
            )
            return

        self.run_button.config(state="disabled")
        self.output_box.delete("1.0", tk.END)
        self.status_label.config(text="Scanning files...")

        try:
            folder_path = Path(folder)
            files = scan_folder(folder_path)

            if not files:
                self.status_label.config(text="No supported files found.")
                return

            self.output_box.insert(tk.END, f"Found {len(files)} supported file(s).\n")
            self.output_box.insert(tk.END, "Processing files...\n\n")

            records = []

            for file_path in files:
                record = enrich_file_record(file_path)
                records.append(record)

            output_dir = Path("output")
            output_dir.mkdir(parents=True, exist_ok=True)

            if self.export_csv.get():
                csv_output = output_dir / "metadata_index.csv"
                export_to_csv(records, csv_output)
                self.output_box.insert(tk.END, f"CSV exported: {csv_output.resolve()}\n")

            if self.export_excel.get():
                excel_output = output_dir / "metadata_index.xlsx"
                export_to_excel(records, excel_output)
                self.output_box.insert(
                    tk.END,
                    f"Excel exported: {excel_output.resolve()}\n",
                )

            summary = generate_summary(records)

            self.output_box.insert(tk.END, "\nSummary:\n")
            self.output_box.insert(tk.END, f"Total files: {summary['total_files']}\n")
            self.output_box.insert(tk.END, f"Success: {summary['success_count']}\n")
            self.output_box.insert(tk.END, f"Errors: {summary['error_count']}\n")
            self.output_box.insert(
                tk.END,
                f"Total size (KB): {summary['total_size_kb']}\n",
            )

            self.output_box.insert(tk.END, "\nBy file type:\n")
            for file_type, count in summary["file_types"].items():
                self.output_box.insert(tk.END, f"  {file_type}: {count}\n")

            self.status_label.config(text="Scan complete.")

        except Exception as error:
            self.status_label.config(text="Error.")
            messagebox.showerror("Error", str(error))

        finally:
            self.run_button.config(state="normal")


def main() -> None:
    root = tk.Tk()
    app = MetadataIndexerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
