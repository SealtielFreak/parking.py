from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    contact_email = models.EmailField()
    rfc = models.CharField(max_length=255)
    curp = models.CharField(max_length=255)
    birthday_date = models.DateField()

    discharge_date = models.DateField()

    state = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255)
    int_num = models.IntegerField()


class BlackList(models.Model):
    id_client = models.ForeignKey(Client, null=False, on_delete=models.CASCADE)


class Payment(models.Model):
    hours = models.DateTimeField()
    mobility = models.CharField(max_length=512)


class Transport(models.Model):
    id_client = models.ForeignKey(Client, null=False, on_delete=models.CASCADE)
    id_payment = models.ForeignKey(Payment, null=False, on_delete=models.CASCADE)

    circulation_card = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    license = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    time_init = models.DateTimeField()
    time_final = models.DateTimeField()


class Page(models.Model):
    id_transport = models.ForeignKey(Transport, null=False, on_delete=models.CASCADE)

    total = models.DecimalField(max_digits=5, decimal_places=2)
    type = models.CharField(max_length=255)
    date_page = models.DateTimeField()
