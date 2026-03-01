from resonate import Resonate, Context
import uuid


app_node_group = "script_e"

resonate = Resonate.remote(
    group=app_node_group,
)


def baz(context: Context, arg: str):
    # ...
    result = f"hello from baz with arg: {arg}"
    return result


@resonate.register
def bar(context: Context, arg: str):
    promise = yield context.begin_run(func=baz, arg=arg)
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
