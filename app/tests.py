import json

from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase

from .schema import schema


class MyTestCase(GraphQLTestCase):
    # Here you need to inject your test case's schema
    GRAPHQL_SCHEMA = schema

    def test_muzakki_query(self):
        response = self.query(
            '''
            query {
                muzakki {
                    id
                    name
                }
            }
            '''
        )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
