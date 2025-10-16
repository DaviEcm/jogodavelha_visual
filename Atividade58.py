import tkinter as tk
from tkinter import messagebox, font
BG = "#f2f4f7" 
FRAME_BG = "#ffffff"  
ACCENT = "#2b6cb0"    
BUTTON_BG = "#e6eef9" 
BTN_CONTROL_BG = "#2b6cb0"
BTN_CONTROL_FG = "#ffffff"
SCORE_BG = "#f7fafc"
TEXT_COLOR = "#222222"

FONT_TITLE = ("Helvetica", 14, "bold")
FONT_SCORE = ("Helvetica", 14)
FONT_BUTTON = ("Helvetica", 32, "bold")
FONT_CONTROL = ("Helvetica", 11)
class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha - Tic Tac Toe")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None]*3 for _ in range(3)]
        self.score = {"X": 0, "O": 0}

        self._build_ui()
    def _build_ui(self):
        pad = 12
        main_frame = tk.Frame(self.root, bg=FRAME_BG, padx=20, pady=16)
        main_frame.grid(row=0, column=0, padx=pad, pady=pad)
        score_frame = tk.Frame(main_frame, bg=SCORE_BG, pady=8, padx=12)
        score_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 12))

        self.lbl_score_x = tk.Label(score_frame, text="X: 0", font=FONT_SCORE,
                                    bg=SCORE_BG, fg=ACCENT, width=12, anchor="w")
        self.lbl_score_x.pack(side="left", padx=(0,10))

        title_lbl = tk.Label(score_frame, text="Tic Tac Toe", font=FONT_TITLE,
                             bg=SCORE_BG, fg=TEXT_COLOR)
        title_lbl.pack(side="left", padx=8)

        self.lbl_score_o = tk.Label(score_frame, text="O: 0", font=FONT_SCORE,
                                    bg=SCORE_BG, fg=ACCENT, width=12, anchor="e")
        self.lbl_score_o.pack(side="left", padx=(10,0))
        board_frame = tk.Frame(main_frame, bg=FRAME_BG)
        board_frame.grid(row=1, column=0, columnspan=3, pady=(0,12))

        for r in range(3):
            for c in range(3):
                b = tk.Button(board_frame,
                              text="",
                              font=FONT_BUTTON,
                              width=5, height=2,
                              bg=BUTTON_BG,
                              activebackground="#dbeefc",
                              relief="raised",
                              command=lambda rr=r, cc=c: self.on_click(rr, cc))
                b.grid(row=r, column=c, padx=6, pady=6)
                self.buttons[r][c] = b
        btn_restart = tk.Button(main_frame, text="Reiniciar Partida",
                                font=FONT_CONTROL, bg=BTN_CONTROL_BG, fg=BTN_CONTROL_FG,
                                activebackground="#1f4f86", padx=12, pady=6,
                                command=self.reiniciar_partida)
        btn_restart.grid(row=2, column=0, sticky="ew", padx=(0,6))

        btn_reset = tk.Button(main_frame, text="Zerar Placar",
                              font=FONT_CONTROL, bg=BTN_CONTROL_BG, fg=BTN_CONTROL_FG,
                              activebackground="#1f4f86", padx=12, pady=6,
                              command=self.zerar_placar)
        btn_reset.grid(row=2, column=1, sticky="ew", padx=6)

        btn_credits = tk.Button(main_frame, text="Créditos",
                                font=FONT_CONTROL, bg="#6b7280", fg="#ffffff",
                                activebackground="#4b5563", padx=12, pady=6,
                                command=self.mostrar_creditos)
        btn_credits.grid(row=2, column=2, sticky="ew", padx=(6,0))
        for i in range(3):
            main_frame.grid_columnconfigure(i, weight=1)
        self.status_var = tk.StringVar(value=f"Vez de: {self.current_player}")
        status_lbl = tk.Label(self.root, textvariable=self.status_var,
                              bg=BG, fg=TEXT_COLOR, anchor="w", padx=12)
        status_lbl.grid(row=1, column=0, sticky="ew")
    def on_click(self, row, col):
        if self.board[row][col] != "":
            return
        self.board[row][col] = self.current_player
        btn = self.buttons[row][col]
        btn.config(text=self.current_player, state="disabled", disabledforeground=ACCENT, bg="#ffffff")
        if self._checar_vitoria(self.current_player):
            self.score[self.current_player] += 1
            self._atualizar_placar()
            messagebox.showinfo("Vencedor", f"Jogador {self.current_player} venceu!")
            self._desabilitar_tabuleiro()
            return
        if self._checar_empate():
            messagebox.showinfo("Empate", "Deu velha! Empate.")
            self._desabilitar_tabuleiro()
            return
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_var.set(f"Vez de: {self.current_player}")

    def reiniciar_partida(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                b = self.buttons[r][c]
                b.config(text="", state="normal", bg=BUTTON_BG)
        self.current_player = "X"
        self.status_var.set(f"Vez de: {self.current_player}")

    def zerar_placar(self):
        self.score = {"X": 0, "O": 0}
        self._atualizar_placar()

    def mostrar_creditos(self):
        texto = ("Jogo da Velha - Tic Tac Toe\n\n"
                 "Autores: Seu Nome Aqui\n"
                 "Turma: Exemplo - Turma XYZ\n"
                 "Projeto para disciplina - Interface Tkinter\n\n"
                 "Obrigado por jogar!")
        messagebox.showinfo("Créditos", texto)
    def _checar_vitoria(self, jogador):
        b = self.board
        # Checa linhas
        for r in range(3):
            if b[r][0] == b[r][1] == b[r][2] == jogador:
                return True
        # Checa colunas
        for c in range(3):
            if b[0][c] == b[1][c] == b[2][c] == jogador:
                return True
        # Diagonais
        if b[0][0] == b[1][1] == b[2][2] == jogador:
            return True
        if b[0][2] == b[1][1] == b[2][0] == jogador:
            return True
        return False

    def _checar_empate(self):
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    return False
        return True

    def _desabilitar_tabuleiro(self):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(state="disabled")

    def _atualizar_placar(self):
        self.lbl_score_x.config(text=f"X: {self.score['X']}")
        self.lbl_score_o.config(text=f"O: {self.score['O']}")
        self.reiniciar_partida()

def main():
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
