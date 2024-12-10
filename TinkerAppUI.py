import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SQL Query Generator")
        self.geometry("800x600")

        # Input frame
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(fill="x")

        self.nlp_input_label = tk.Label(self.input_frame, text="NLP Input:")
        self.nlp_input_label.pack(side="left")

        self.nlp_input_entry = tk.Text(self.input_frame, height=5, width=50)
        self.nlp_input_entry.pack(side="left")

        self.generate_button = tk.Button(self.input_frame, text="Generate SQL Query", command=self.generate_sql_query)
        self.generate_button.pack(side="left")

        # Recent prompts frame
        self.recent_prompts_frame = tk.Frame(self)
        self.recent_prompts_frame.pack(fill="x")

        self.recent_prompts_label = tk.Label(self.recent_prompts_frame, text="Recent Prompts:")
        self.recent_prompts_label.pack(side="left")

        self.recent_prompts_listbox = tk.Listbox(self.recent_prompts_frame, width=50)
        self.recent_prompts_listbox.pack(side="left")

        # Query results frame
        self.query_results_frame = tk.Frame(self)
        self.query_results_frame.pack(fill="both", expand=True)

        self.query_results_tree = ttk.Treeview(self.query_results_frame)
        self.query_results_tree.pack(fill="both", expand=True)

        # Export data button
        self.export_data_button = tk.Button(self.query_results_frame, text="Export Data to CSV", command=self.export_data_to_csv)
        self.export_data_button.pack()

        # SQL query output frame
        self.sql_query_output_frame = tk.Frame(self)
        self.sql_query_output_frame.pack(fill="x")

        self.sql_query_output_label = tk.Label(self.sql_query_output_frame, text="SQL Query Output:")
        self.sql_query_output_label.pack(side="left")

        self.sql_query_output_text = tk.Text(self.sql_query_output_frame, height=5, width=50)
        self.sql_query_output_text.pack(side="left")

    def generate_sql_query(self):
        nlp_input = self.nlp_input_entry.get("1.0", "end-1c")
        # Call the generate_query method here
        sql_query = self.sql_generator.generate_query(nlp_input)
        self.sql_query_output_text.delete("1.0", "end")
        self.sql_query_output_text.insert("1.0", sql_query)

        # Update the recent prompts listbox
        self.recent_prompts_listbox.insert("end", nlp_input)

        # Update the query results treeview
        # Call the method to execute the SQL query and get the results
        results = self.execute_sql_query(sql_query)
        self.query_results_tree.delete(*self.query_results_tree.get_children())
        for row in results:
            self.query_results_tree.insert("", "end", values=row)

    def export_data_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            results = self.query_results_tree.get_children()
            data = []
            for row in results:
                data.append(self.query_results_tree.item(row, "values"))
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)

    def execute_sql_query(self, sql_query):
        # Implement the method to execute the SQL query and get the results
        pass

if __name__ == "__main__":
    app = Application()
    app.mainloop()