import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class OrcamentoRM:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Orçamento R.M")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.nome_cliente = tk.StringVar()
        self.tipo_imovel = tk.StringVar()
        self.quartos = tk.IntVar(value=1)
        self.vagas = tk.IntVar(value=0)
        self.possui_criancas = tk.StringVar(value="s")
        self.parcelas = tk.IntVar(value=1)
        self.valor_base = 0

        self.tela_inicial()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def tela_inicial(self):
        self.limpar_tela()
        tk.Label(self.root, text="=== SISTEMA DE ORÇAMENTO R.M ===", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Label(self.root, text="Digite seu nome:", font=("Arial", 11)).pack()
        tk.Entry(self.root, textvariable=self.nome_cliente, width=30).pack(pady=10)
        tk.Button(self.root, text="Iniciar Orçamento", command=self.tela_tipo, width=20, bg="#2e8b57", fg="white").pack(pady=20)

    def tela_tipo(self):
        self.limpar_tela()
        tk.Label(self.root, text=f"Olá, {self.nome_cliente.get()}!\nSelecione o tipo de locação:", font=("Arial", 12)).pack(pady=20)
        tipos = [("Apartamento - R$700", "Apartamento"),
                 ("Casa - R$900", "Casa"),
                 ("Estúdio - R$1200", "Estúdio")]
        for texto, valor in tipos:
            ttk.Radiobutton(self.root, text=texto, value=valor, variable=self.tipo_imovel).pack(anchor="w", padx=80)
        tk.Button(self.root, text="Avançar", command=self.tela_quartos, bg="#2e8b57", fg="white").pack(pady=30)

    def tela_quartos(self):
        if not self.tipo_imovel.get():
            messagebox.showerror("Erro", "Selecione um tipo de imóvel.")
            return
        self.limpar_tela()
        tk.Label(self.root, text="Selecione a quantidade de quartos:", font=("Arial", 12)).pack(pady=20)
        if self.tipo_imovel.get() == "Estúdio":
            tk.Label(self.root, text="Estúdios possuem apenas 1 quarto.", font=("Arial", 10, "italic")).pack(pady=10)
            self.quartos.set(1)
        else:
            ttk.Radiobutton(self.root, text="1 Quarto (sem acréscimo)", value=1, variable=self.quartos).pack(anchor="w", padx=80)
            ttk.Radiobutton(self.root, text="2 Quartos (+R$200 Apto / +R$250 Casa)", value=2, variable=self.quartos).pack(anchor="w", padx=80)
        tk.Button(self.root, text="Avançar", command=self.tela_vagas, bg="#2e8b57", fg="white").pack(pady=30)

    def tela_vagas(self):
        self.limpar_tela()
        tk.Label(self.root, text="Deseja incluir vaga de garagem/estacionamento?", font=("Arial", 12)).pack(pady=20)
        if self.tipo_imovel.get() in ["Apartamento", "Casa"]:
            ttk.Radiobutton(self.root, text="Sim (+R$300)", value=1, variable=self.vagas).pack(anchor="w", padx=80)
            ttk.Radiobutton(self.root, text="Não", value=0, variable=self.vagas).pack(anchor="w", padx=80)
        else:
            ttk.Radiobutton(self.root, text="2 vagas (+R$250)", value=2, variable=self.vagas).pack(anchor="w", padx=80)
            ttk.Radiobutton(self.root, text="Mais vagas adicionais (+R$250 + R$60/extra)", value=3, variable=self.vagas).pack(anchor="w", padx=80)
            ttk.Radiobutton(self.root, text="Sem vagas", value=0, variable=self.vagas).pack(anchor="w", padx=80)
        tk.Button(self.root, text="Avançar", command=self.tela_criancas, bg="#2e8b57", fg="white").pack(pady=30)

    def tela_criancas(self):
        self.limpar_tela()
        tk.Label(self.root, text="Possui crianças?", font=("Arial", 12)).pack(pady=20)
        ttk.Radiobutton(self.root, text="Sim", value="s", variable=self.possui_criancas).pack(anchor="w", padx=80)
        ttk.Radiobutton(self.root, text="Não", value="n", variable=self.possui_criancas).pack(anchor="w", padx=80)
        tk.Button(self.root, text="Avançar", command=self.tela_parcelas, bg="#2e8b57", fg="white").pack(pady=30)

    def tela_parcelas(self):
        self.limpar_tela()
        tk.Label(self.root, text="Deseja parcelar o contrato em quantas vezes? (1 a 5)", font=("Arial", 12)).pack(pady=20)
        tk.Spinbox(self.root, from_=1, to=5, textvariable=self.parcelas, width=5, font=("Arial", 11)).pack()
        tk.Button(self.root, text="Gerar Orçamento", command=self.calcular_valor, bg="#2e8b57", fg="white").pack(pady=30)

    def calcular_valor(self):
        tipo = self.tipo_imovel.get()
        quartos = self.quartos.get()
        vagas = self.vagas.get()
        possui_criancas = self.possui_criancas.get()
        parcelas = self.parcelas.get()

        if tipo == "Apartamento":
            self.valor_base = 700
            if quartos == 2:
                self.valor_base += 200
            if vagas == 1:
                self.valor_base += 300
            if possui_criancas == "n":
                self.valor_base *= 0.95
        elif tipo == "Casa":
            self.valor_base = 900
            if quartos == 2:
                self.valor_base += 250
            if vagas == 1:
                self.valor_base += 300
        elif tipo == "Estúdio":
            self.valor_base = 1200
            if vagas == 2:
                self.valor_base += 250
            elif vagas == 3:
                self.valor_base += 250 + 60  # valor fixo por 1 vaga extra

        valor_contrato = 2000
        valor_parcela = valor_contrato / parcelas

        self.resumo(tipo, quartos, valor_contrato, valor_parcela)

    def resumo(self, tipo, quartos, valor_contrato, valor_parcela):
        self.limpar_tela()
        tk.Label(self.root, text=f"=== RESUMO DO ORÇAMENTO ===", font=("Arial", 14, "bold")).pack(pady=20)
        texto = f"""
Cliente: {self.nome_cliente.get()}
Tipo de Imóvel: {tipo}
Quartos: {quartos}
Valor do Aluguel: R$ {self.valor_base:.2f}
Valor Total do Contrato: R$ {valor_contrato:.2f}
Parcelamento: {self.parcelas.get()}x de R$ {valor_parcela:.2f}
"""
        tk.Label(self.root, text=texto, justify="left", font=("Consolas", 11)).pack(pady=10)
        tk.Button(self.root, text="Gerar CSV", command=self.gerar_csv, bg="#4682B4", fg="white").pack(pady=10)
        tk.Button(self.root, text="Novo Orçamento", command=self.tela_inicial, bg="#2e8b57", fg="white").pack(pady=10)
        tk.Button(self.root, text="Sair", command=self.root.quit, bg="#B22222", fg="white").pack(pady=10)

    def gerar_csv(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not caminho:
            return
        with open(caminho, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Mês", "Valor da Parcela (R$)"])
            for mes in range(1, 13):
                writer.writerow([f"{mes}º mês", f"{self.valor_base:.2f}"])
        messagebox.showinfo("Sucesso", "Arquivo CSV gerado com sucesso!")

# Executa o programa
if __name__ == "__main__":
    root = tk.Tk()
    app = OrcamentoRM(root)
    root.mainloop()
