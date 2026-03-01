from resonate import Resonate, Context
import uuid


app_node_group = "script_c"

resonate = Resonate.remote(
    group=app_node_group,
)


def foo():
    try:
        result = resonate.options(target="poll://any@service_a").rpc(
            str(uuid.uuid4()), func="bar", arg="hello from foo"
        )
        print(result)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    foo()
