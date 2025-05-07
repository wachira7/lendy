import zeep
from loan_app.soap_client import CoreBankingAPIClient


class CoreBankingService:
    def __init__(self):
        self.client = CoreBankingAPIClient()


    def get_customer_kyc(self, customer_number):
        #  Call KYC API
        return self.client.get_customer_kyc(customer_number)


    def get_transaction_data(self, customer_number):
        #  Call Transaction Data API
        return self.client.get_transaction_data(customer_number)


