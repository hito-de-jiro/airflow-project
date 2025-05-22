import os

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "#alerts"

def send_or_update_slack_message(**context):
    client = WebClient(token=SLACK_BOT_TOKEN)
    ti = context["ti"]
    new_message = context["params"]["message"]

    # Read previous message and ts from XCom
    last_message = ti.xcom_pull(task_ids="send_message_task", key="last_message") or ""
    last_ts = ti.xcom_pull(task_ids="send_message_task", key="last_ts")

    try:
        if new_message == last_message and last_ts:
            # Update previous message
            response = client.chat_update(
                channel=SLACK_CHANNEL,
                ts=last_ts,
                text=f"{new_message} (оновлено: повтор)"
            )
            print(f"Updated Slack message: {response['ts']}")
        else:
            # New message
            response = client.chat_postMessage(
                channel=SLACK_CHANNEL,
                text=new_message
            )
            print(f"Sent new Slack message: {response['ts']}")
            # Save message and ts
            ti.xcom_push(key="last_message", value=new_message)
            ti.xcom_push(key="last_ts", value=response["ts"])
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")


with DAG(
    dag_id="slack_sdk_update_message_dag",
    start_date=days_ago(1),
    schedule_interval=None,
    catchup=False,
    tags=["slack", "alerts"],
) as dag:

    send_message = PythonOperator(
        task_id="send_message_task",
        python_callable=send_or_update_slack_message,
        provide_context=True,
        params={
            "message": ":warning: Error 404"  # Dynamic message
        },
    )