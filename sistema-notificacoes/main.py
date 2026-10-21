
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Notificacao:
    destinatario: str
    conteudo: str

    def validar(self):
        if not self.destinatario.strip():
            raise ValueError("Destinatario vazio")

        if not self.conteudo.strip():
            raise ValueError("Conteudo vazio")


class CanalNotificacao(ABC):
    @abstractmethod
    def enviar(self, notificacao):
        pass


class CanalEmail(CanalNotificacao):
    def enviar(self, notificacao):
        notificacao.validar()
        print(f"[EMAIL] Para: {notificacao.destinatario}")
        print(f"Mensagem: {notificacao.conteudo}")
        return True


class CanalSMS(CanalNotificacao):
    def enviar(self, notificacao):
        notificacao.validar()
        print(f"[SMS] Para: {notificacao.destinatario}")
        print(f"Mensagem: {notificacao.conteudo}")
        return True


class CanalPush(CanalNotificacao):
    def enviar(self, notificacao):
        notificacao.validar()
        print(f"[PUSH] Para: {notificacao.destinatario}")
        print(f"Mensagem: {notificacao.conteudo}")
        return True


class CriadorNotificacao(ABC):
    @abstractmethod
    def criar_canal(self):
        pass

    def notificar(self, notificacao):
        canal = self.criar_canal()
        return canal.enviar(notificacao)


class CriadorEmail(CriadorNotificacao):
    def criar_canal(self):
        return CanalEmail()


class CriadorSMS(CriadorNotificacao):
    def criar_canal(self):
        return CanalSMS()


class CriadorPush(CriadorNotificacao):
    def criar_canal(self):
        return CanalPush()


class ServicoNotificacao:
    def executar(self, criador, notificacao):
        notificacao.validar()
        return criador.notificar(notificacao)


def main():
    servico = ServicoNotificacao()

    mensagem = Notificacao(
        "cliente@exemplo.com",
        "Seu pedido foi confirmado!"
    )

    servico.executar(CriadorEmail(), mensagem)

    servico.executar(
        CriadorSMS(),
        Notificacao("11999999999", "Pedido enviado!")
    )

    servico.executar(
        CriadorPush(),
        Notificacao("usuario123", "Nova notificacao!")
    )


if __name__ == "__main__":
    main()
