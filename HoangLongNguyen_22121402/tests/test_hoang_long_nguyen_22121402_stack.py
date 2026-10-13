import aws_cdk as core
import aws_cdk.assertions as assertions

from hoang_long_nguyen_22121402.hoang_long_nguyen_22121402_stack import HoangLongNguyen22121402Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in hoang_long_nguyen_22121402/hoang_long_nguyen_22121402_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = HoangLongNguyen22121402Stack(app, "hoang-long-nguyen-22121402")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
