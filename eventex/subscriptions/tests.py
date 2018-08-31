from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):

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
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """Html must contain csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Must have susbcrition form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name','cpf','email','phone'],list(form.fields))

class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Rodolfo Bruno', cpf='11140271466',
                    email='rodolfobruno93@gmail.com', phone='8299904-0708')
        self.resp = self.client.post('/inscricao/', data)
    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)#302 é o status code de redirect

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox)) #no modo de teste o django não envia o email de verdade, o que ele faz é anotar no outbox quantos emails foram enviados na requisição, 'mínimo  1'

    def test_subscription_email_subsject(self):
        email = mail.outbox[0]  # 0 pq só tem 1, outbox guarda uma lista dos emails enviados, objetos email que tem atributos, subject é um deles
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        email = mail.  outbox[0] # 0 pq só tem 1, outbox guarda uma lista dos emails enviados, objetos email que tem atributos, subject é um deles
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        email = mail.outbox[0] # 0 pq só tem 1, outbox guarda uma lista dos emails enviados, objetos email que tem atributos, subject é um deles
        expect = ['contato@eventex.com.br','rodolfobruno93@gmail.com']
        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]
        self.assertIn('Rodolfo Bruno', email.body)
        self.assertIn('11140271466', email.body)
        self.assertIn('rodolfobruno93@gmail.com', email.body)
        self.assertIn('8299904-0708', email.body)

class SubscribeInvalidPost(TestCase):
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
