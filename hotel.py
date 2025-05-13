import flet as ft
from datetime import datetime, timedelta
import uuid

class Cliente:
    def __init__(self, nome, telefone, email):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.id = str(uuid.uuid4())

class Quarto:
    def __init__(self, numero, tipo, preco_diaria):
        self.numero = numero
        self.tipo = tipo  # 'single', 'double', 'suite'
        self.preco_diaria = preco_diaria
        self.disponivel = True
        
    def __str__(self):
        return f"Quarto {self.numero} ({self.tipo}) - R${self.preco_diaria}/noite - {'Disponível' if self.disponivel else 'Ocupado'}"

class Reserva:
    def __init__(self, cliente, quarto, check_in, check_out):
        self.cliente = cliente
        self.quarto = quarto
        self.check_in = check_in
        self.check_out = check_out
        self.status = "Confirmada"
        self.id = str(uuid.uuid4())
        
    def calcular_valor_total(self):
        dias = (self.check_out - self.check_in).days
        return dias * self.quarto.preco_diaria

class GerenciadorDeReservas:
    def __init__(self):
        self.clientes = []
        self.quartos = []
        self.reservas = []
        
        self.quartos.append(Quarto(1, "single", 250))
        self.quartos.append(Quarto(2, "single", 250))
        self.quartos.append(Quarto(3, "double", 350))
        self.quartos.append(Quarto(4, "double", 350))
        self.quartos.append(Quarto(5, "suite", 550))
        self.quartos.append(Quarto(6, "suite", 550))
    
    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)
    
    def verificar_disponibilidade(self, quarto, check_in, check_out):
        for reserva in self.reservas:
            if reserva.quarto == quarto:
                if (check_in < reserva.check_out and check_out > reserva.check_in):
                    return False
        return True
    
    def criar_reserva(self, cliente, quarto, check_in, check_out):
        if self.verificar_disponibilidade(quarto, check_in, check_out):
            reserva = Reserva(cliente, quarto, check_in, check_out)
            self.reservas.append(reserva)
            quarto.disponivel = False
            return reserva
        return None
    
    def cancelar_reserva(self, reserva_id):
        for reserva in self.reservas:
            if reserva.id == reserva_id:
                reserva.quarto.disponivel = True
                reserva.status = "Cancelada"
                self.reservas.remove(reserva)
                return True
        return False
    
    def listar_reservas(self):
        return self.reservas
    
    def listar_clientes(self):
        return self.clientes
    
    def listar_quartos_disponiveis(self, check_in=None, check_out=None):
        if check_in is None or check_out is None:
            return [q for q in self.quartos if q.disponivel]
        else:
            disponiveis = []
            for quarto in self.quartos:
                if self.verificar_disponibilidade(quarto, check_in, check_out):
                    disponiveis.append(quarto)
            return disponiveis


class HotelApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Havaianas Hotel - Sistema de Reservas"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 900
        self.page.window_height = 700
        
        self.gerenciador = GerenciadorDeReservas()
        
        self.gerenciador.adicionar_cliente(Cliente("Felipe Lages", "11987654321", "joao@email.com"))
        self.gerenciador.adicionar_cliente(Cliente("José do Carmo", "21987654321", "maria@email.com"))
        
        self.pagina_atual = "inicio"
        self.criar_interface()
    
    def criar_interface(self):
        nav_bar = ft.Row(
            controls=[
                ft.ElevatedButton("Início", on_click=lambda e: self.mudar_pagina("inicio")),
                ft.ElevatedButton("Nova Reserva", on_click=lambda e: self.mudar_pagina("nova_reserva")),
                ft.ElevatedButton("Clientes", on_click=lambda e: self.mudar_pagina("clientes")),
                ft.ElevatedButton("Reservas", on_click=lambda e: self.mudar_pagina("reservas")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
        
        self.conteudo = ft.Column()
        0
        self.page.add(
            ft.Column(
                [
                    ft.Text("Havaianas Hotel", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    nav_bar,
                    ft.Divider(),
                    self.conteudo
                ],
                expand=True
            )
        )
        
        self.atualizar_conteudo()
    
    def mudar_pagina(self, pagina):
        self.pagina_atual = pagina
        self.atualizar_conteudo()
    
    def atualizar_conteudo(self):
        self.conteudo.controls.clear()
        
        if self.pagina_atual == "inicio":
            self.mostrar_inicio()
        elif self.pagina_atual == "nova_reserva":
            self.mostrar_nova_reserva()
        elif self.pagina_atual == "clientes":
            self.mostrar_clientes()
        elif self.pagina_atual == "reservas":
            self.mostrar_reservas()
        
        self.page.update()
    
    def mostrar_inicio(self):
        titulo = ft.Text("Quartos Disponíveis", size=24, weight=ft.FontWeight.BOLD)
        self.conteudo.controls.append(titulo)
        
        # Lista de quartos
        for quarto in self.gerenciador.quartos:
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"Quarto {quarto.numero}", weight=ft.FontWeight.BOLD),
                            ft.Text(f"Tipo: {quarto.tipo}"),
                            ft.Text(f"Preço: R${quarto.preco_diaria}/noite"),
                            ft.Text("Disponível" if quarto.disponivel else "Ocupado", 
                                    color=ft.colors.GREEN if quarto.disponivel else ft.colors.RED),
                        ],
                        spacing=5
                    ),
                    padding=10,
                    width=300
                )
            )
            self.conteudo.controls.append(card)
    
    def mostrar_nova_reserva(self):
        titulo = ft.Text("Nova Reserva", size=24, weight=ft.FontWeight.BOLD)
        self.conteudo.controls.append(titulo)
        
        self.dropdown_clientes = ft.Dropdown(
            options=[ft.dropdown.Option(c.nome) for c in self.gerenciador.clientes],
            label="Cliente",
            width=400
        )
        
        self.dropdown_quartos = ft.Dropdown(
            options=[ft.dropdown.Option(f"Quarto {q.numero} ({q.tipo})") for q in self.gerenciador.quartos if q.disponivel],
            label="Quarto",
            width=400
        )
        
        self.data_checkin = ft.TextField(label="Check-in (DD/MM/AAAA)", width=200)
        self.data_checkout = ft.TextField(label="Check-out (DD/MM/AAAA)", width=200)
        
        btn_reservar = ft.ElevatedButton(
            "Confirmar Reserva",
            on_click=self.criar_reserva,
            icon=ft.icons.CHECK
        )
        
        form = ft.Column(
            [
                self.dropdown_clientes,
                self.dropdown_quartos,
                ft.Row([self.data_checkin, self.data_checkout]),
                btn_reservar
            ],
            spacing=20
        )
        
        self.conteudo.controls.append(form)
    
    def criar_reserva(self, e):
        try:
            cliente_nome = self.dropdown_clientes.value
            cliente = next(c for c in self.gerenciador.clientes if c.nome == cliente_nome)
            
            quarto_desc = self.dropdown_quartos.value
            quarto_num = int(quarto_desc.split()[1])
            quarto = next(q for q in self.gerenciador.quartos if q.numero == quarto_num)
            
            check_in = datetime.strptime(self.data_checkin.value, "%d/%m/%Y").date()
            check_out = datetime.strptime(self.data_checkout.value, "%d/%m/%Y").date()
            
            if check_in >= check_out:
                raise ValueError("Data de check-out deve ser após check-in")
            
            reserva = self.gerenciador.criar_reserva(cliente, quarto, check_in, check_out)
            
            if reserva:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Reserva criada com sucesso!"),
                    action="OK"
                )
                self.page.snack_bar.open = True
                self.mudar_pagina("inicio")
            else:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Quarto não disponível para estas datas"),
                    action="OK",
                    bgcolor=ft.colors.RED
                )
                self.page.snack_bar.open = True
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Erro: {str(ex)}"),
                action="OK",
                bgcolor=ft.colors.RED
            )
            self.page.snack_bar.open = True
        
        self.page.update()
    
    def mostrar_clientes(self):
        titulo = ft.Text("Clientes Cadastrados", size=24, weight=ft.FontWeight.BOLD)
        self.conteudo.controls.append(titulo)
        
        btn_novo_cliente = ft.ElevatedButton(
            "Novo Cliente",
            on_click=lambda e: self.mostrar_form_cliente(),
            icon=ft.icons.PERSON_ADD
        )
        self.conteudo.controls.append(btn_novo_cliente)
        
        for cliente in self.gerenciador.clientes:
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(cliente.nome, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Telefone: {cliente.telefone}"),
                            ft.Text(f"E-mail: {cliente.email}"),
                        ],
                        spacing=5
                    ),
                    padding=10,
                    width=400
                )
            )
            self.conteudo.controls.append(card)
    
    def mostrar_form_cliente(self):
        self.conteudo.controls.clear()
        
        titulo = ft.Text("Novo Cliente", size=24, weight=ft.FontWeight.BOLD)
        self.conteudo.controls.append(titulo)
        
        self.novo_cliente_nome = ft.TextField(label="Nome", width=400)
        self.novo_cliente_telefone = ft.TextField(label="Telefone", width=400)
        self.novo_cliente_email = ft.TextField(label="E-mail", width=400)
        
        btn_salvar = ft.ElevatedButton(
            "Salvar",
            on_click=self.salvar_cliente,
            icon=ft.icons.SAVE
        )
        
        btn_cancelar = ft.ElevatedButton(
            "Cancelar",
            on_click=lambda e: self.mudar_pagina("clientes"),
            icon=ft.icons.CANCEL
        )
        
        form = ft.Column(
            [
                self.novo_cliente_nome,
                self.novo_cliente_telefone,
                self.novo_cliente_email,
                ft.Row([btn_salvar, btn_cancelar])
            ],
            spacing=20
        )
        
        self.conteudo.controls.append(form)
        self.page.update()
    
    def salvar_cliente(self, e):
        try:
            novo_cliente = Cliente(
                self.novo_cliente_nome.value,
                self.novo_cliente_telefone.value,
                self.novo_cliente_email.value
            )
            self.gerenciador.adicionar_cliente(novo_cliente)
            
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Cliente cadastrado com sucesso!"),
                action="OK"
            )
            self.page.snack_bar.open = True
            
            self.mudar_pagina("clientes")
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Erro: {str(ex)}"),
                action="OK",
                bgcolor=ft.colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
    
    def mostrar_reservas(self):
        titulo = ft.Text("Reservas Ativas", size=24, weight=ft.FontWeight.BOLD)
        self.conteudo.controls.append(titulo)
        
        if not self.gerenciador.reservas:
            self.conteudo.controls.append(ft.Text("Nenhuma reserva encontrada."))
            return
        
        for reserva in self.gerenciador.reservas:
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"Reserva #{reserva.id[:8]}", weight=ft.FontWeight.BOLD),
                            ft.Text(f"Cliente: {reserva.cliente.nome}"),
                            ft.Text(f"Quarto: {reserva.quarto.numero} ({reserva.quarto.tipo})"),
                            ft.Text(f"Check-in: {reserva.check_in.strftime('%d/%m/%Y')}"),
                            ft.Text(f"Check-out: {reserva.check_out.strftime('%d/%m/%Y')}"),
                            ft.Text(f"Status: {reserva.status}"),
                            ft.ElevatedButton(
                                "Cancelar Reserva",
                                on_click=lambda e, r=reserva: self.cancelar_reserva(r),
                                icon=ft.icons.CANCEL,
                                color=ft.colors.RED
                            ) if reserva.status == "Confirmada" else None
                        ],
                        spacing=5
                    ),
                    padding=10,
                    width=400
                )
            )
            self.conteudo.controls.append(card)
    
    def cancelar_reserva(self, reserva):
        if self.gerenciador.cancelar_reserva(reserva.id):
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Reserva cancelada com sucesso!"),
                action="OK"
            )
            self.page.snack_bar.open = True
            self.mudar_pagina("reservas")
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Erro ao cancelar reserva"),
                action="OK",
                bgcolor=ft.colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()

def main(page: ft.Page):
    app = HotelApp(page)

ft.app(target=main)