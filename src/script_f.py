from resonate import Resonate, Context
import uuid


app_node_group = "script_f"

resonate = Resonate.remote(
    group=app_node_group,
)


@resonate.register
def bar(context: Context, arg: str):
    promise = yield context.begin_rpc(func="baz", arg=arg).options(
        target="poll://any@service_b"
    )
    result = yield promise
    result = f"hello from bar with arg: {result}"
    return result


def foo():
    try:
        result = bar.run(str(uuid.uuid4()), arg="hello from foo")
        print(result)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    foo()
