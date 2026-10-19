from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_events as events,
    aws_events_targets as targets,
    aws_iam as iam,
    aws_cloudwatch as cloudwatch,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_dynamodb as dynamodb,
    aws_cloudwatch_actions as cw_actions,
    aws_apigateway as apigateway,
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
            description="Web Health Crawler - Week 3",
        )
        web_crawler.apply_removal_policy(RemovalPolicy.DESTROY)

        # Allow Lambda apply metrics on CloudWatch
        web_crawler.add_to_role_policy(
            iam.PolicyStatement(
                actions=["cloudwatch:PutMetricData"],
                resources=["*"]
            )
        )

        # Run Lambda automatically every 30 mins
        rule = events.Rule(
    self, "WebHealthSchedule",
    schedule=events.Schedule.rate(Duration.minutes(30)),
    description="Trigger WebHealth Crawler every 30 minutes"
    )
        rule.add_target(targets.LambdaFunction(web_crawler))

        # SNS Topic for alarm notifications
        alarm_topic = sns.Topic(
            self, "WebHealthAlarmTopic",
            display_name="WebHealth Alarm Notifications"
        )
        # Email subscription - change to your email
        alarm_topic.add_subscription(
            subscriptions.EmailSubscription("22121402@student.westernsydney.edu.au")
        )

        # List of website need to monitor
        websites = [
            "https://www.westernsydney.edu.au/",
            "https://www.google.com/",
            "https://www.github.com/",
            "https://aws.amazon.com/",
            "https://this-website-does-not-exist-12345.com"
        ]

        # Create alarm for each website
        for website in websites:
            clean_name = website.replace("https://", "").replace("/", "").replace(".", "-")

            # Alarm Availability
            availability_alarm = cloudwatch.Alarm(
                self, f"AvailabilityAlarm-{clean_name}",
                metric=cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Availability",
                    statistic="Average",
                    period=Duration.minutes(5),
                    dimensions_map={"Website": website}
                ),
                threshold=1.0,
                evaluation_periods=1,
                comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
                alarm_description=f"Availability dropped for {website}",
                alarm_name=f"Availability-{clean_name}"
            )
            availability_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))

            # Alarm Latency
            latency_alarm = cloudwatch.Alarm(
                self, f"LatencyAlarm-{clean_name}",
                metric=cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Latency",
                    statistic="Average",
                    period=Duration.minutes(5),
                    dimensions_map={"Website": website}
                ),
                threshold=2000,
                evaluation_periods=1,
                comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
                alarm_description=f"Latency too high for {website}",
                alarm_name=f"Latency-{clean_name}"
            )
            latency_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))

        # Apply SNS after Alarm was created
        latency_alarm.add_alarm_action(
            cw_actions.SnsAction(alarm_topic)
        )
        availability_alarm.add_alarm_action(
            cw_actions.SnsAction(alarm_topic)
        )

        # CloudWatch Dashboard
        dashboard = cloudwatch.Dashboard(
            self, "WebHealthDashboard",
            dashboard_name="WebHealth-Dashboard"
        )

                # DynamoDB table to log alarms
        alarm_table = dynamodb.Table(
            self, "WebHealthAlarmTable",
            partition_key=dynamodb.Attribute(
                name="alarm_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        # DynamoDB table for website list
        website_table = dynamodb.Table(
            self, "WebsiteTable",
            partition_key=dynamodb.Attribute(
                name="url",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        website_table.grant_read_data(web_crawler)
        
        web_crawler.add_environment("WEBSITE_TABLE_NAME", website_table.table_name)

        # Lambda for Website CRUD API
        website_api_lambda = _lambda.Function(
            self, "WebsiteApi",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="website_api.handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            environment={
                "WEBSITE_TABLE_NAME": website_table.table_name
            }
        )
        website_api_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        website_table.grant_read_write_data(website_api_lambda)

        # API Gateway
        api = apigateway.LambdaRestApi(
            self, "WebsiteApiGateway",
            handler=website_api_lambda,
            proxy=True,
            rest_api_name="WebsiteCRUDApi"
        )

        # Lambda to log SNS alarms into DynamoDB
        alarm_logger = _lambda.Function(
            self, "AlarmLogger",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="alarm_logger.handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            environment={
                "ALARM_TABLE_NAME": alarm_table.table_name
            }
        )
        alarm_logger.apply_removal_policy(RemovalPolicy.DESTROY)

        alarm_table.grant_write_data(alarm_logger)

        alarm_topic.add_subscription(
            subscriptions.LambdaSubscription(alarm_logger)
        )
        

        # Widget for Latency
        latency_widget = cloudwatch.GraphWidget(
            title="Website Latency (ms)",
            left=[
                cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Latency",
                    dimensions_map={"Website": "https://www.google.com/"},
                    statistic="Average",
                    period=Duration.minutes(5),
                ),
                cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Latency",
                    dimensions_map={"Website": "https://www.github.com/"},
                    statistic="Average",
                    period=Duration.minutes(5)
                ),
                cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Latency",
                    dimensions_map={"Website": "https://aws.amazon.com/"},
                    statistic="Average",
                    period=Duration.minutes(5)
                ),
                cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Latency",
                    dimensions_map={"Website": "https://www.westernsydney.edu.au/"},
                    statistic="Average",
                    period=Duration.minutes(5)
                ),
                cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Latency",
                    dimensions_map={"Website": "https://this-website-does-not-exist-12345.com/"},
                    statistic="Average",
                    period=Duration.minutes(5)
                )
            ],
            width=12
        )

        # Widget for Availability
        availability_widget = cloudwatch.GraphWidget(
            title="Website Availability",
            left=[
                cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Availability",
                    dimensions_map={"Website": "https://www.google.com/"},
                    statistic="Average",
                    period=Duration.minutes(5),
                ),
                cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Availability",
                    dimensions_map={"Website": "https://www.github.com/"},
                    statistic="Average",
                    period=Duration.minutes(5)
                ),
                cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Availability",
                    dimensions_map={"Website": "https://aws.amazon.com/"},
                    statistic="Average",
                    period=Duration.minutes(5)
                ),
                cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Availability",
                    dimensions_map={"Website": "https://www.westernsydney.edu.au/"},
                    statistic="Average",
                    period=Duration.minutes(5)
                ),
                cloudwatch.Metric(
                    namespace="WebHealth",
                    metric_name="Availability",
                    dimensions_map={"Website": "https://this-website-does-not-exist-12345.com/"},
                    statistic="Average",
                    period=Duration.minutes(5)
                )
            ],
            width=12
        )

               # Alarm for fake website - Availability
        fake_availability_alarm = cloudwatch.Alarm(
            self, "FakeWebsiteAvailabilityAlarm",
            metric=cloudwatch.Metric(
                namespace="WebHealth",
                metric_name="Availability",
                dimensions_map={"Website": "https://this-website-does-not-exist-12345.com/"},
                statistic="Average",
                period=Duration.minutes(5)
            ),
            threshold=1.0,
            evaluation_periods=1,
            comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
            alarm_description="Availability dropped for fake website"
        )
        fake_availability_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))

        # Alarm for fake website - Latency
        fake_latency_alarm = cloudwatch.Alarm(
            self, "FakeWebsiteLatencyAlarm",
            metric=cloudwatch.Metric(
                namespace="WebHealth",
                metric_name="Latency",
                dimensions_map={"Website": "https://this-website-does-not-exist-12345.com/"},
                statistic="Average",
                period=Duration.minutes(5)
            ),
            threshold=2000,
            evaluation_periods=1,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            alarm_description="Latency too high for fake website"
        )
        fake_latency_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))


        # Add 2 widget into Dashboard
        dashboard.add_widgets(latency_widget, availability_widget)