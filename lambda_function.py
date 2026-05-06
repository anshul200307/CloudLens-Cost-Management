import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ce = boto3.client('ce', region_name='us-east-1')
    sns = boto3.client('sns', region_name='ap-south-1')
    s3 = boto3.client('s3')
    
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='DAILY',
        Metrics=['BlendedCost'],
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )
    
    report = f"""
====================================
CloudLens — AWS Cost Report
====================================
Period: {start_date} to {end_date}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
====================================

SERVICE WISE BREAKDOWN:
"""
    
    total_cost = 0
    service_costs = {}
    
    for result in response['ResultsByTime']:
        for group in result['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics']['BlendedCost']['Amount'])
            if service not in service_costs:
                service_costs[service] = 0
            service_costs[service] += cost
            total_cost += cost
    
    for service, cost in sorted(service_costs.items(),
                                key=lambda x: x[1],
                                reverse=True):
        if cost > 0:
            report += f"\n{service}: ${cost:.4f}"
    
    report += f"""

====================================
TOTAL (7 days): ${total_cost:.4f}
====================================
"""
    
    if total_cost > 1.0:
        report += "\n⚠️ ALERT: Cost exceeded $1!"
    
    s3.put_object(
        Bucket='cost-reports-anshul',
        Key=f'reports/cost-report-{end_date}.txt',
        Body=report
    )
    
    sns.publish(
        TopicArn='arn:aws:sns:ap-south-1:891612580748:cost-management-alert',
        Message=report,
        Subject=f'CloudLens — Daily Cost Report {end_date}'
    )
    
    return {
        'statusCode': 200,
        'body': 'Report generated!'
    }