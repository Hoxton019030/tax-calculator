import tkinter as tk
from tkinter import messagebox, filedialog

class TaxCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("營業稅計算器")
        self.root.geometry("300x500")  # 固定視窗大小為300x500

        self.entry_var = tk.StringVar()
        self.entry_label = tk.Label(root, text="含稅金額")
        self.entry_label.pack(pady=5)
        self.entry = tk.Entry(root, textvariable=self.entry_var, width=15)
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", self.enter_callback)  # 綁定Enter鍵

        self.label_excluded = tk.Label(root, text="未稅金額: ")
        self.label_excluded.pack()

        self.label_tax = tk.Label(root, text="稅額: ")
        self.label_tax.pack()

        self.frame1 = tk.LabelFrame(root, text="統計")
        self.frame1.pack(pady=10)

        self.stats_label = tk.Label(root, text="輸入次數: 0\n含稅金額總計: 0\n未稅金額總計: 0\n稅額總計: 0")  # 顯示統計資訊
        self.stats_label.pack()

        self.entry_count = 0
        self.total_included_amount = 0
        self.total_excluded_amount = 0
        self.total_tax_amount = 0

        self.calculate_button = tk.Button(root, text="計算", command=self.calculate_tax)
        self.calculate_button.pack(pady=5)

        self.txt_button = tk.Button(root, text="儲存成txt檔", command=self.save_txt)
        self.txt_button.pack(pady=5)

        self.clear_button = tk.Button(root, text="全部清除", command=self.clear_all)
        self.clear_button.pack(pady=5)

        # 创建一个Canvas和垂直滚动条，用于包含输入行
        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)  # 绑定滚轮事件

        # 创建一个框架，用于放置输入行
        self.output_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.output_frame, anchor="nw",height=1000)

        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # 用于存储输入行和删除按钮的列表
        self.entries = []

    def format_currency(self, amount):
        return "{:,.0f}".format(amount)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def calculate_tax(self):
        try:
            included_amount = float(self.entry_var.get())

            # 检查输入的值是否为0或负数，如果是，则不添加到输入信息中
            if included_amount <= 0:
                messagebox.showwarning("警告", "請輸入大於0的數字。")
            else:
                excluded_amount = round(included_amount / 1.05)
                tax_amount = included_amount - excluded_amount

                self.label_excluded.config(text=f"未稅金額: {self.format_currency(excluded_amount)}")
                self.label_tax.config(text=f"稅額: {self.format_currency(tax_amount)}")

                self.entry_count += 1
                self.total_included_amount += included_amount
                self.total_excluded_amount += excluded_amount
                self.total_tax_amount += tax_amount

                self.stats_label.config(
                    text=f"輸入次數: {self.entry_count}\n含稅金額總計: {self.format_currency(self.total_included_amount)}\n未稅金額總計: {self.format_currency(self.total_excluded_amount)}\n稅額總計: {self.format_currency(self.total_tax_amount)}")

                entry_frame = tk.Frame(self.output_frame)  # 创建一个新的Frame用于包含每个输入行和删除按钮
                entry_frame.pack()

                entry_label_text = f"含稅金額: {self.format_currency(included_amount)} 未稅金額: {self.format_currency(excluded_amount)} " \
                                    f"稅額: {self.format_currency(tax_amount)} "

                entry_label = tk.Label(entry_frame, text=entry_label_text)
                entry_label.pack(side=tk.LEFT)

                # 创建删除按钮并将其绑定到删除方法
                delete_button = tk.Button(entry_frame, text="刪除", command=lambda text=entry_label_text: self.delete_entry(text, entry_frame))
                delete_button.pack(side=tk.LEFT)

                # 将输入行、删除按钮和索引存储到列表中
                self.entries.append((entry_frame, entry_label, delete_button))

                self.entry_var.set("")
        except ValueError:
            messagebox.showerror("錯誤", "請輸入有效的數字。")

    def enter_callback(self, event):
        self.calculate_tax()

    def delete_entry(self, entry_text, entry_frame):
    # 检查列表是否为空
        if self.entries:
        # 从列表中删除输入行和对应的删除按钮
            for index, (_, entry_label, delete_button) in enumerate(self.entries):
                if entry_label.cget("text") == entry_text and entry_frame == self.entries[index][0]:
                    entry_frame.destroy()  # 移除整个Frame
                    self.entries.pop(index)  # 从列表中移除对应项

                # 更新统计信息
                    self.update_stats()

    def update_stats(self):
        self.entry_count = len(self.entries)
        self.total_included_amount = sum(
            float(entry_label.cget("text").split("含稅金額: ")[1].split(" ")[0].replace(",", "")) for _, entry_label, _ in
            self.entries)
        self.total_excluded_amount = sum(
            float(entry_label.cget("text").split("未稅金額: ")[1].split(" ")[0].replace(",", "")) for _, entry_label, _ in
            self.entries)
        self.total_tax_amount = sum(
            float(entry_label.cget("text").split("稅額: ")[1].split(" ")[0].replace(",", "")) for _, entry_label, _ in
            self.entries)

        self.stats_label.config(
            text=f"輸入次數: {self.entry_count}\n含稅金額總計: {self.format_currency(self.total_included_amount)}\n未稅金額總計: {self.format_currency(self.total_excluded_amount)}\n稅額總計: {self.format_currency(self.total_tax_amount)}")

    def save_txt(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write("統計資訊\n")
                file.write("====================\n\n")
                file.write("含稅總金額總計: {}\n".format(self.format_currency(self.total_included_amount)))
                file.write("未稅總金額總計: {}\n".format(self.format_currency(self.total_excluded_amount)))
                file.write("稅額總計: {}\n\n".format(self.format_currency(self.total_tax_amount)))
                file.write("個別輸入資訊:\n")
                for _, entry_label, _ in self.entries:
                    text = entry_label.cget("text")
                    if "刪除" not in text:  # 排除包含 "刪除" 的行
                        file.write(text + "\n")

    def clear_all(self):
        self.entry_var.set("")  # 清空輸入框
        self.label_excluded.config(text="未稅金額: ")
        self.label_tax.config(text="稅額: ")
        self.stats_label.config(text="輸入次數: 0\n含稅金額總計: 0\n未稅金額總計: 0\n稅額總計: 0")

        # 移除所有輸入行和刪除按鈕
        for entry_frame, _, delete_button in self.entries:
            entry_frame.destroy()
            delete_button.destroy()

        # 清空列表
        self.entries.clear()

        # 重置統計資訊
        self.entry_count = 0
        self.total_included_amount = 0
        self.total_excluded_amount = 0
        self.total_tax_amount = 0

    def on_canvas_configure(self, event):
        # 调整Canvas的大小以适应内容
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

root = tk.Tk()
app = TaxCalculatorApp(root)
root.mainloop()