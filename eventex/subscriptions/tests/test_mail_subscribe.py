from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Rodolfo Bruno', cpf='11140271466',
                    email='rodolfobruno93@gmail.com', phone='8299904-0708')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0] # 0 pq só tem 1, outbox guarda uma lista dos emails enviados, objetos email que tem atributos, subject é um deles

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br','rodolfobruno93@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents=['Rodolfo Bruno',
                  '11140271466',
                  'rodolfobruno93@gmail.com',
                  '8299904-0708',
                  ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)


