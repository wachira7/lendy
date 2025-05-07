from .models import Customer, Loan
from .soap_client import CoreBankingAPIClient
from scoring_engine_integration.services import ScoringEngineService
from cbs_integration.services import CoreBankingService
from django.db import transaction
from django.core.exceptions import ValidationError


class LoanService:
    def create_loan(self, customer_number, amount):
        #  Business logic for loan creation
        #  1. Check for existing pending loan
        if Loan.objects.filter(
            customer__customer_number=customer_number, status='PENDING'
            ).exists():
            raise ValidationError(
                'Customer has an existing pending loan application.'
                )  

        #  2. Fetch customer from KYC API
        core_banking_service = CoreBankingService()
        customer_data = core_banking_service.get_customer_kyc(customer_number)
        if not customer_data:
            raise ValidationError('Customer not found.')
        try:
            customer = Customer.objects.get(customer_number=customer_number)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(
            customer_number=customer_number, **customer_data
            )

        with transaction.atomic():
            loan = Loan.objects.create(customer=customer, amount=amount, status='PENDING')

        #  3. Initiate Scoring
        scoring_service = ScoringEngineService()
        token = scoring_service.initiate_query_score(customer_number)
        loan.token = token
        loan.save()

        #  4. Asynchronously get the score and limit with retries
        ScoringEngineService.get_score_and_limit_with_retry.delay(loan.id, token)

        return loan


    def get_loan_status(self, customer_number):
        #  Logic to get loan status
        try:
            loan = Loan.objects.get(customer__customer_number=customer_number)
            return loan.status
        except Loan.DoesNotExist:
            return 'No loan found for this customer.'
        

class TransactionDataService:
    def __init__(self):
        self.client = CoreBankingAPIClient()