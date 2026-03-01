from resonate import Resonate, Context
from threading import Event

app_node_group = "service_b"

resonate = Resonate().remote(
    group=app_node_group,
)


@resonate.register
def baz(context: Context, arg: str):
    # ...
    result = f"hello from baz with arg: {arg}"
    return result


def main():
    resonate.start()
    print("service b is running")
    Event().wait()


if __name__ == "__main__":
    main()
