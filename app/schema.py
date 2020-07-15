from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
import graphene
import graphql_jwt

from .models import Muzakki, ZakatType, ZakatQuality, User, Period, ZakatPayment, ZakatTransaction


class MuzakkiType(DjangoObjectType):
    class Meta:
        model = Muzakki


class UserType(DjangoObjectType):
    class Meta:
        model = User


class PeriodType(DjangoObjectType):
    class Meta:
        model = Period


class ZakatTypesType(DjangoObjectType):
    class Meta:
        model = ZakatType


class ZakatQualityType(DjangoObjectType):
    class Meta:
        model = ZakatQuality


class ZakatPaymentType(DjangoObjectType):
    class Meta:
        model = ZakatPayment


class ZakatTransactionType(DjangoObjectType):
    class Meta:
        model = ZakatTransaction


class MuzakkiQuery(graphene.ObjectType):
    muzakkis = graphene.List(MuzakkiType)
    muzakki = graphene.Field(MuzakkiType, muzakki_id=graphene.Int())

    def resolve_muzakkis(self, info, **kwargs):
        return Muzakki.objects.all()

    def resolve_muzakki(self, info, muzakki_id):
        return Muzakki.objects.get(pk=muzakki_id)


class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()


class PeriodQuery(graphene.ObjectType):
    active_period = graphene.Int()

    def resolve_active_period(self, info, **kwargs):
        return Period.objects.get(is_active=True).year


class ZakatTypeQuery(graphene.ObjectType):
    zakat_types = graphene.List(ZakatTypesType)

    def resolve_zakat_types(self, info, **kwargs):
        return ZakatType.objects.all()


class ZakatQualityQuery(graphene.ObjectType):
    zakat_qualities = graphene.List(ZakatQualityType)

    def resolve_zakat_qualities(self, info, **kwargs):
        return ZakatQuality.objects.all()


class ZakatTransactionInput(graphene.InputObjectType):
    income_value = graphene.Int()
    income_goods = graphene.Int()
    muzakki_id = graphene.ID(required=True)
    transaction_type = graphene.Field(
        graphene.Enum(
            'TransactionType', ZakatTransaction.TRANSACTION_TYPES
        ), required=True)
    zakat_quality_id = graphene.ID(required=True)


class AddTransaction(graphene.Mutation):
    class Input:
        payer_name = graphene.String(required=True)
        payer_address = graphene.String(required=True)
        payer_phone = graphene.String()
        payer_email = graphene.String()
        receiver_id = graphene.ID(required=True)
        transactions = graphene.List(ZakatTransactionInput, required=True)

    payment = graphene.Field(ZakatPaymentType)

    def mutate(self, info, **input):
        receiver = User.objects.get(pk=input.get('receiver_id'))
        payment = ZakatPayment(
            payer_name=input.get('payer_name'),
            payer_address=input.get('payer_address'),
            receiver=receiver,
            period=Period.get_active_period()
        )
        if input.get('payer_phone'):
            payment.payer_phone = input.get('payer_phone')
        if input.get('payer_email'):
            payment.payer_email = input.get('payer_email')

        payment.save()
        payment.generate_payment_code()

        def extract_transaction(transaction):
            muzakki = Muzakki.objects.get(pk=transaction.get('muzakki_id'))
            quality = ZakatQuality.objects.get(
                pk=transaction.get('zakat_quality_id'))
            zakat_transaction = ZakatTransaction(
                muzakki=muzakki,
                transaction_type=transaction.get('transaction_type'),
                zakat_quality=quality,
                zakat_payment=payment
            )
            if transaction.get('income_value'):
                zakat_transaction.income_value = transaction.get(
                    'income_value')
            if transaction.get('income_goods'):
                zakat_transaction.income_goods = transaction.get(
                    'income_goods')
            return zakat_transaction

        transactions = input.get('transactions')
        list_transaction = [extract_transaction(
            transaction) for transaction in transactions]
        ZakatTransaction.objects.bulk_create(list_transaction)

        return AddTransaction(payment=payment)


class Query(
    MuzakkiQuery,
    PeriodQuery,
    ZakatTypeQuery,
    ZakatQualityQuery,
    UserQuery,
    graphene.ObjectType
):
    pass


class Mutation(graphene.ObjectType):
    add_transaction = AddTransaction.Field()
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    logout = graphql_jwt.DeleteJSONWebTokenCookie.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
