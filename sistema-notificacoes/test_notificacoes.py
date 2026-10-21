
import unittest
from io import StringIO
from contextlib import redirect_stdout

from main import (
    Notificacao,
    CriadorEmail,
    CriadorSMS,
    CriadorPush,
    ServicoNotificacao,
)


class TestNotificacoes(unittest.TestCase):

    def setUp(self):
        self.servico = ServicoNotificacao()

    def test_envio_email(self):
        notificacao = Notificacao(
            "cliente@exemplo.com",
            "Pedido confirmado"
        )

        with redirect_stdout(StringIO()) as saida:
            resultado = self.servico.executar(
                CriadorEmail(), notificacao
            )

        self.assertTrue(resultado)
        self.assertIn("[EMAIL]", saida.getvalue())
        self.assertIn("Pedido confirmado", saida.getvalue())

    def test_envio_sms(self):
        notificacao = Notificacao("11999999999", "Pedido enviado")

        with redirect_stdout(StringIO()) as saida:
            resultado = self.servico.executar(
                CriadorSMS(), notificacao
            )

        self.assertTrue(resultado)
        self.assertIn("[SMS]", saida.getvalue())

    def test_envio_push(self):
        notificacao = Notificacao("usuario123", "Nova notificacao")

        with redirect_stdout(StringIO()) as saida:
            resultado = self.servico.executar(
                CriadorPush(), notificacao
            )

        self.assertTrue(resultado)
        self.assertIn("[PUSH]", saida.getvalue())

    def test_destinatario_vazio(self):
        notificacao = Notificacao("", "Mensagem de teste")

        with self.assertRaises(ValueError):
            self.servico.executar(CriadorEmail(), notificacao)

    def test_conteudo_vazio(self):
        notificacao = Notificacao("cliente@exemplo.com", "   ")

        with self.assertRaises(ValueError):
            self.servico.executar(CriadorEmail(), notificacao)


if __name__ == "__main__":
    unittest.main()
