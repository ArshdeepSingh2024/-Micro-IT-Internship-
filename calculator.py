import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Initialize variables
        self.current_input = "0"
        self.full_operation = ""
        self.last_was_operator = False
        self.last_was_equals = False
        
        # Fonts
        self.display_font = font.Font(size=24, weight="bold")
        self.button_font = font.Font(size=14)
        
        # Create display frame
        self.display_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        self.display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Small display for showing full operation
        self.small_display = tk.Label(
            self.display_frame,
            text="",
            font=font.Font(size=12),
            anchor=tk.E,
            bg="#2c3e50",
            fg="#95a5a6",
            padx=10,
            pady=5
        )
        self.small_display.pack(fill=tk.X)
        
        # Main display
        self.display = tk.Label(
            self.display_frame, 
            text=self.current_input,
            font=self.display_font,
            anchor=tk.E,
            bg="#2c3e50",
            fg="white",
            padx=10,
            pady=5
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons frame
        self.buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure grid
        for i in range(5):
            self.buttons_frame.rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.columnconfigure(i, weight=1)
        
        # Create buttons
        self.create_buttons()
    
    def create_buttons(self):
        # First row - Clear and operators
        self.create_button("AC", 0, 0, 2, bg="#e74c3c", fg="white", command=self.clear)
        self.create_button("÷", 0, 2, 1, bg="#3498db", fg="white", command=lambda: self.handle_operator("/"))
        self.create_button("×", 0, 3, 1, bg="#3498db", fg="white", command=lambda: self.handle_operator("*"))
        
        # Digit buttons
        self.create_digit_buttons()
        
        # More operators
        self.create_button("-", 1, 3, 1, bg="#3498db", fg="white", command=lambda: self.handle_operator("-"))
        self.create_button("+", 2, 3, 1, bg="#3498db", fg="white", command=lambda: self.handle_operator("+"))
        
        # Last row - Zero, decimal and equals
        self.create_button("0", 4, 0, 2, bg="#ecf0f1", command=lambda: self.append_digit("0"))
        self.create_button(".", 4, 2, 1, bg="#ecf0f1", command=self.append_decimal)
        self.create_button("=", 3, 3, 2, bg="#2ecc71", fg="white", command=self.evaluate, row_span=2)
    
    def create_digit_buttons(self):
        digits = {
            7: (1, 0), 8: (1, 1), 9: (1, 2),
            4: (2, 0), 5: (2, 1), 6: (2, 2),
            1: (3, 0), 2: (3, 1), 3: (3, 2)
        }
        
        for digit, coords in digits.items():
            self.create_button(
                str(digit), 
                coords[0], 
                coords[1], 
                1,
                bg="#ecf0f1", 
                command=lambda d=digit: self.append_digit(str(d))
            )
    
    def create_button(self, text, row, column, col_span=1, row_span=1, bg="#ffffff", fg="black", command=None):
        button = tk.Button(
            self.buttons_frame,
            text=text,
            font=self.button_font,
            bg=bg,
            fg=fg,
            relief=tk.RAISED,
            borderwidth=2,
            command=command
        )
        button.grid(
            row=row, 
            column=column, 
            columnspan=col_span, 
            rowspan=row_span, 
            padx=5, 
            pady=5, 
            sticky="nsew"
        )
    
    def append_digit(self, digit):
        if self.current_input == "0" or self.current_input == "Error" or self.last_was_operator or self.last_was_equals:
            self.current_input = digit
            self.last_was_operator = False
            self.last_was_equals = False
        else:
            self.current_input += digit
        self.update_display()
    
    def append_decimal(self):
        if self.last_was_operator or self.last_was_equals:
            self.current_input = "0."
            self.last_was_operator = False
            self.last_was_equals = False
        elif self.current_input == "Error":
            self.current_input = "0."
        elif "." not in self.current_input:
            self.current_input += "."
        self.update_display()
    
    def handle_operator(self, operator):
        if self.current_input == "Error":
            return
            
        # If we previously hit equals, start a new calculation with the result
        if self.last_was_equals:
            self.full_operation = self.current_input
            
        # If this is our first entry or if the last button was also an operator, update the operator
        elif not self.full_operation or self.last_was_operator:
            # Replace the last operator if there's one
            if self.full_operation:
                self.full_operation = self.full_operation[:-1]
                
            # If no full operation yet, use the current input as the first number
            if not self.full_operation and self.current_input:
                self.full_operation = self.current_input
        else:
            # Normal operation - append the current number to the operation string
            self.full_operation += self.current_input
            
            # Try to evaluate the expression so far
            try:
                result = str(eval(self.full_operation))
                self.current_input = self.format_number(result)
            except:
                pass
        
        # Add the new operator
        self.full_operation += operator
        self.last_was_operator = True
        self.last_was_equals = False
        self.update_display()
    
    def evaluate(self):
        if self.current_input == "Error" or not self.full_operation:
            return
            
        # Don't evaluate if we just pressed equals or an operator
        if self.last_was_equals or (self.last_was_operator and not self.current_input):
            return
            
        try:
            # Add the current number to the operation
            if not self.last_was_operator:
                self.full_operation += self.current_input
                
            # Calculate the result
            result = eval(self.full_operation)
            
            # Format the result
            self.current_input = self.format_number(str(result))
            self.full_operation = ""
            self.last_was_equals = True
            self.last_was_operator = False
            self.update_display()
        except ZeroDivisionError:
            self.current_input = "Error"
            self.full_operation = ""
            self.update_display()
        except Exception as e:
            self.current_input = "Error"
            self.full_operation = ""
            self.update_display()
    
    def format_number(self, number_str):
        try:
            # Convert to float first to handle scientific notation
            num = float(number_str)
            
            # If it's an integer, remove the decimal part
            if num.is_integer():
                return str(int(num))
            else:
                return number_str
        except:
            return number_str
    
    def clear(self):
        self.current_input = "0"
        self.full_operation = ""
        self.last_was_operator = False
        self.last_was_equals = False
        self.update_display()
    
    def update_display(self):
        # Format the operation string for display
        display_operation = self.full_operation.replace("*", "×").replace("/", "÷")
        self.small_display.config(text=display_operation)
        self.display.config(text=self.current_input)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()