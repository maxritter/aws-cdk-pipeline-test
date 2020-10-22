from aws_cdk import core
from os import path

import aws_cdk.aws_lambda as lmb
import aws_cdk.aws_apigateway as apigw

class AwsCdkPipelineTestStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        this_dir = path.dirname(__file__)

        handler = lmb.Function(self, 'Handler',
            runtime=lmb.Runtime.PYTHON_3_8,
            handler='handler.handler',
            code=lmb.Code.from_asset(path.join(this_dir, 'lambda')))

        gw = apigw.LambdaRestApi(self, 'Gateway',
            description='Endpoint for a simple Lambda-powered web service',
            handler=handler.current_version)

        self.url_output = core.CfnOutput(self, 'Url',
            value=gw.url)