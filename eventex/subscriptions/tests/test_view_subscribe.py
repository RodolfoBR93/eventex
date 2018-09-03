from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeGet(TestCase):

    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        tags=(('<form',1),
              ('<input', 6),
              ('type="text"', 3),
              ('type="email"',1),
              ('type="submit"',1))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp,text,count)


    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Must have susbcrition form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Rodolfo Bruno', cpf='11140271466',
                    email='rodolfobruno93@gmail.com', phone='8299904-0708')
        self.resp = self.client.post('/inscricao/', data)
    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)#302 é o status code de redirect

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox)) #no modo de teste o django não envia o email de verdade, o que ele faz é anotar no outbox quantos emails foram enviados na requisição, 'mínimo  1'


class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """ Invalid POST should not redirect """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form,SubscriptionForm)

    def test_form_has_erros(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Rodolfo Bruno', cpf='11140271466',
                    email='rodolfobruno93@gmail.com' , phone='8299904-0708')

        response = self.client.post('/inscricao/',data, follow=True)
        self.assertContains(response,'Inscrição realizada com sucesso!')

