import sqlalchemy as sa
from core.db import Base, get_engine, get_session

## Import models so the Base object can find the metadata it needs to create
from domain.models.demo import models as demo_models

## Create custom database engine
engine = get_engine(connection="db/demo.sqlite", echo=True)

try:
    Base.metadata.create_all(bind=engine)
except Exception as exc:
    raise Exception(f"Unhandled exception creating Base metadata. Details: {exc}")

## Create custom database session
SessionLocal = get_session(engine=engine)
print(f"SessionLocal: {type(SessionLocal)}")


def demo_add_users():
    """
    Demo function, creates static users on the fly and
    commits them to the database.
    """

    try:
        with SessionLocal() as sess:
            ## User1, all fields with single address
            spongebob = demo_models.User(
                name="spongebob",
                fullname="Spongebob Squarepants",
                addresses=[
                    demo_models.Address(email_address="spongebob@sqlalchemy.org")
                ],
            )

            ## User 2, all fields with multiple addressess
            sandy = demo_models.User(
                name="sandy",
                fullname="Sandy Cheeks",
                addresses=[
                    demo_models.Address(email_address="sandy@sqlalchemy.org"),
                    demo_models.Address(email_address="sandy@squirrelpower.org"),
                ],
            )

            ## User 3, naame & fullname, no address
            patrick = demo_models.User(name="patrick", fullname="Patrick Star")

            ## Build list of users to pass to add_all()
            _users: list[demo_models.User] = [spongebob, sandy, patrick]
            add_users: list[demo_models.User] = []

            for _user in _users:
                ## Check if _user already exists
                if (
                    not sess.query(demo_models.User)
                    .filter(demo_models.User.name == _user.name)
                    .count()
                ):
                    ## _user does not exist, add to add_users list
                    add_users.append(_user)
                else:
                    print(f"User '{_user.name}' already exists.")
                    pass

            print(f"Add users: {add_users}")

            ## Add all users to session
            sess.add_all(add_users)

            ## Commit to database
            sess.commit()

    except Exception as exc:
        raise Exception(f"Unhandled exception starting session. Details: {exc}")


def demo_select(
    user_names: list[str] = ["spongebob", "sandy"]
) -> list[demo_models.User]:
    ## Build select statement
    statement: sa.sql.Select = sa.select(demo_models.User).where(
        demo_models.User.name.in_(user_names)
    )

    with SessionLocal() as sess:
        all_users = sess.scalars(statement)

        users: list[demo_models.User] = all_users.all()

    return users


def demo_select_with_join(
    name: str = "sandy", email_address: str = "sandy@sqlalchemy.org"
):
    ## Build select statement
    statement: sa.sql.Select = (
        sa.select(demo_models.Address)
        .join(demo_models.Address.user)
        .where(demo_models.User.name == name)
        .where(demo_models.Address.email_address == email_address)
    )

    with SessionLocal() as sess:
        ## Take first/one instance
        #  Result will be an Address instance
        _join_select = sess.scalars(statement).one()

    return _join_select


def demo_update_email(
    name: str = "patrick", email_address: str = "patrickstar@sqlalchemy.org"
):
    sel_user_stmt: sa.sql.Select = sa.select(demo_models.User).where(
        demo_models.User.name == name
    )

    with SessionLocal() as sess:
        try:
            user: demo_models.User = sess.scalars(sel_user_stmt).one()

            update_addr: demo_models.Address = demo_models.Address(
                email_address=email_address
            )

            if not update_addr in user.addresses:
                ## Append an address to user
                user.addresses.append(update_addr)

            else:
                print(
                    f"Address '{update_addr.email_address}' already exists on User {name}"
                )
        except Exception as exc:
            raise Exception(
                f"Unhandled exception updating User address. Details: {exc}"
            )


if __name__ == "__main__":
    add_users = demo_add_users()
    select_users = demo_select()
    # print(f"Users: {select_users}")

    select_join = demo_select_with_join()
    # print(f"Result of select join: {select_join}")

    update_email = demo_update_email()
