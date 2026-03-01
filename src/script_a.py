from resonate import Resonate, Context
import uuid


app_node_group = "script_a"

resonate = Resonate.remote(
    group=app_node_group,
)


@resonate.register
def bar(context: Context, arg: str):
    # ...
    result = f"hello from bar with arg: {arg}"
    return result


def foo():
    try:
        result = bar.run(str(uuid.uuid4()), arg="hello from foo")
        print(result)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    foo()
