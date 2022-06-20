from django.db import models
from django.db.models import AutoField, CharField, EmailField, DateField, IntegerField, ForeignKey, DateTimeField, \
    TextField, DecimalField, TimeField, Model


class Client(Model):
    client_id = AutoField(primary_key=True)

    first_name = CharField(max_length=24)
    last_name = CharField(max_length=24)

    birthday_date = DateField()
    contact_email = EmailField()
    rfc = CharField(max_length=24, null=True, blank=True)
    curp = CharField(max_length=24, null=True, blank=True)

    state = CharField(max_length=16, null=True, blank=True)
    suburb = CharField(max_length=16, null=True, blank=True)
    municipality = CharField(max_length=16, null=True, blank=True)
    int_num = IntegerField(null=True, blank=True)

    discharge_date = DateField()

    class Meta:
        unique_together = (('client_id', 'first_name', 'last_name', 'birthday_date'),)

    def __str__(self):
        return f"ID: {self.client_id}, FirstName: {self.first_name}, LastName: {self.last_name}"


class BlackList(Model):
    client = ForeignKey(Client, on_delete=models.CASCADE)

    discharge_date = DateField(null=True, blank=True)
    reasons = TextField(null=True, blank=True)

    def __str__(self):
        return f"ID: {self.client.client_id}, ID Client: {self.client.client_id}, FirstName: {self.client.first_name}, LastName: {self.client.last_name}"


class PaymentPlane(Model):
    payment_plane_id = AutoField(primary_key=True)

    hours = IntegerField()
    mobility = CharField(max_length=24)

    def __str__(self):
        return f"{self.payment_plane_id}, {self.hours} {self.mobility}"

    class Meta:
        unique_together = ('payment_plane_id', 'mobility')

    def __str__(self):
        return f"Mobility: {self.mobility}"


class Transport(Model):
    transport_id = AutoField(primary_key=True)

    client = ForeignKey(Client, on_delete=models.CASCADE)
    payment_planes = ForeignKey(PaymentPlane, on_delete=models.CASCADE)

    model = CharField(max_length=24)
    brand = CharField(max_length=24)
    type = CharField(max_length=24)

    description = TextField(null=True, blank=True)

    circulation_card = CharField(max_length=16, null=True, blank=True)
    license = CharField(max_length=24, null=True, blank=True)

    time_init = TimeField()
    time_final = TimeField()

    def __str__(self):
        return f"{self.client.client_id}, {self.model} {self.brand}"


class Check(Model):
    TYPE_CHECK = (
        ('E', 'Entry'),
        ('D', 'Departure'),
    )

    check_id = AutoField(primary_key=True)

    transport = ForeignKey(Transport, on_delete=models.CASCADE)
    type_check = CharField(max_length=1, choices=TYPE_CHECK)

    since = DateTimeField()
    until = DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"ID: {self.check_id}, Transport {self.transport.transport_id}"


class Payment(Model):
    payment_id = AutoField(primary_key=True)

    transport = ForeignKey(Transport, on_delete=models.CASCADE)

    total = DecimalField(max_digits=5, decimal_places=2)
    type = CharField(max_length=255)
    date = DateTimeField()

    def __str__(self):
        return f"ID: {self.payment_id}, Transport: {self.transport.transport_id}"