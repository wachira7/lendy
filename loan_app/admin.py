from django.contrib import admin

from .models import Loan, Customer, TransactionDataEndpoint

admin.site.register(Loan)
admin.site.register(Customer)
admin.site.register(TransactionDataEndpoint)
