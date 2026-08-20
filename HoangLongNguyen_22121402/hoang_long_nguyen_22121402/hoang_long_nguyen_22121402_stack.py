from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    aws_cloudwatch as cloudwatch,
)
from constructs import Construct

class HoangLongNguyen22121402Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda Function - Web Health Crawler
        web_crawler = _lambda.Function(
            self, "WebHealthCrawler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="hello.handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(60),
            memory_size=256,
            description="Web Health Crawler - Week 3"
        )

        # Allow Lambda apply metrics on CloudWatch
        web_crawler.add_to_role_policy(
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"]
            )
        )

        # Run Lambda automatically every 5 min
        rule = events.Rule(
            self, "WebHealthSchedule",
            schedule=events.Schedule.rate(Duration.minutes(5)),
            description="Trigger WebHealth Crawler every 5 minutes"
        )
        rule.add_target(targets.LambdaFunction(web_crawler))

        # Alarm when Latency very high (> 2000ms)
        latency_alarm = cloudwatch.Alarm(
            self, "HighLatencyAlarm",
            metric=cloudwatch.Metric(
                namespace="WebHealth",
                metric_name="Latency",
                statistic="Average",
                period=Duration.minutes(5)
            ),
            threshold=2000,
            evaluation_periods=1,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            alarm_description="Website latency is too high"
        )

        # Alarm when Availability very low (< 1)
        availability_alarm = cloudwatch.Alarm(
            self, "LowAvailabilityAlarm",
            metric=cloudwatch.Metric(
                namespace="WebHealth",
                metric_name="Availability",
                statistic="Average",
                period=Duration.minutes(5)
            ),
            threshold=1.0,
            evaluation_periods=1,
            comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
            alarm_description="Website availability dropped"
        )
        # CloudWatch Dashboard
        dashboard = cloudwatch.Dashboard(
            self, "WebHealthDashboard",
            dashboard_name="WebHealth-Dashboard"
        )

        # Widget cho Latency
        latency_widget = cloudwatch.GraphWidget(
            title="Website Latency (ms)",
            left=[
                cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Latency",
                    statistic="Average",
                    period=Duration.minutes(5)
                )
            ],
            width=12
        )

        # Widget cho Availability
        availability_widget = cloudwatch.GraphWidget(
            title="Website Availability",
            left=[
                cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Availability",
                    statistic="Average",
                    period=Duration.minutes(5)
                )
            ],
            width=12
        )

        # Add 2 widget into Dashboard
        dashboard.add_widgets(latency_widget, availability_widget)