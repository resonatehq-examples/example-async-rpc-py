from resonate import Resonate, Context
import uuid


app_node_group = "script_d"

resonate = Resonate.remote(
    group=app_node_group,
)


def foo():
    try:
        handle = resonate.options(target="poll://any@service_a").begin_rpc(
            str(uuid.uuid4()), func="bar", arg="hello from foo"
        )
        result = handle.result()
        print(result)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    foo()
