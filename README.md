# Stock Portfolio Tracker

A modern **Tkinter-based Python application** to manage and visualize stock portfolios.  
This project was developed as part of the **CodeAlpha Python Internship** to demonstrate key programming concepts while building a professional, user-friendly interface.

---

## Features
- Add new stocks with quantity, purchase price, and current price
- Automatic calculation of:
  - Invested amount
  - Current value
  - Profit/Loss percentage
- Color-coded profit/loss highlighting (green for profit, red for loss)
- Embedded bar chart visualization (Invested vs Current Value)
- Save portfolio to CSV file
- Load portfolio back from CSV file
- Clean, modern UI with headings, alignment, and summary section

---

## Concepts Demonstrated
This project explicitly integrates the following internship requirements:

- **Dictionary** → Hardcoded stock price list for validation  
- **Input/Output** → User entries via Tkinter `Entry` fields, echoed to console with `[INPUT]` and `[OUTPUT]` logs  
- **Arithmetic** → Calculations for invested amount, current value, and profit/loss percentage  
- **File Handling** → Save portfolio to `portfolio.csv` and load it back into the app  

---

## Technologies Used
- **Python 3**
- **Tkinter** → GUI framework
- **ttk** → Modern themed widgets
- **messagebox** → User feedback dialogs
- **csv** → File handling for portfolio persistence
- **matplotlib** → Embedded charts for visualization

---

## Project Structure

StockPortfolioTracker/
├── StackPortfolioTracker.py   # Main application code
├── portfolio.csv              # Saved portfolio data
├── README.md                  # Documentation
└── LICENSE                    # MIT License file

---

## How to Run
1. Clone the repository:
   git clone https://github.com/yourusername/StockPortfolioTracker.git
2. Navigate to the project folder:
   cd StockPortfolioTracker
3. Run the application:
python StackPortfolioTracker.py

---

## Screenshots

Start 

<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/3fec7318-1fff-45b5-8531-c2e80f3278a2" />

---

Adding Stock with graph

<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/208a09b2-04c7-4293-8a86-94a39f53c13a" />

---

## Internship Learning Outcome
This project demonstrates how core programming concepts (dictionary, input/output, arithmetic, file handling) can be applied in a real-world GUI application.
It combines technical rigor with modern UI/UX design, making it both educational and portfolio-ready.

---

## License
This project is licensed under the [MIT License](LICENSE) — feel free to use, modify, and share.

----
