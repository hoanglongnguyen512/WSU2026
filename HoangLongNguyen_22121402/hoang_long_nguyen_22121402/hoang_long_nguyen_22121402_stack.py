from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)
from constructs import Construct

class HoangLongNguyen22121402Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Hello World Lambda
        hello_fn = _lambda.Function(
            self, "HelloWorldFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="hello.handler",
            code=_lambda.Code.from_asset("lambda"),
            description="Hello World Lambda - COMP2029 Week 1"
        )
