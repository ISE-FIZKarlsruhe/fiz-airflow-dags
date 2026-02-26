from datetime import datetime

from airflow.sdk import dag, Param
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.hitl import HITLEntryOperator, HITLBranchOperator
from airflow.task.trigger_rule import TriggerRule


@dag(
    dag_id="demo2",
    start_date=datetime(2022, 1, 1),
    schedule="0 0 * * *",
    catchup=False,
    tags=["demo", "hitl"],
)
def demo2():
    start = EmptyOperator(task_id="start")

    # "Form" step: dropdown + free-text field
    form = HITLEntryOperator(
        task_id="form",
        subject="Fill in fields",
        params={
            "env": Param("dev", type="string", enum=["dev", "staging", "prod"], title="Environment"),
            "note": Param("", type="string", title="Note"),
        },
    )

    # "Branch" step: dropdown to pick which task runs
    choose = HITLBranchOperator(
        task_id="choose",
        subject="Pick what to run",
        options=["Say hello", "Say bye"],
        options_mapping={
            "Say hello": "hello",
            "Say bye": "bye",
        },
        multiple=False,
    )

    # Read the form values from XCom of `form` using the cross-communications
    hello = BashOperator(
        task_id="hello",
        bash_command="""
echo "hello env={{ ti.xcom_pull(task_ids='form')['params_input']['env'] }} \
note={{ ti.xcom_pull(task_ids='form')['params_input']['note'] }}"
""".strip(),
    )

    bye = BashOperator(
        task_id="bye",
        bash_command="""
echo "bye env={{ ti.xcom_pull(task_ids='form')['params_input']['env'] }} \
note={{ ti.xcom_pull(task_ids='form')['params_input']['note'] }}"
""".strip(),
    )

    end = EmptyOperator(task_id="end", trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS)

    start >> form >> choose >> [hello, bye] >> end


dag = demo2()
