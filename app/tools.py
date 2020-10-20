import click
from . import orm, schemas
from fastapi.encoders import jsonable_encoder


# users group

@click.group()
def users():
    pass

@click.command()
@click.argument('full_name')
@click.argument('email')
@click.argument('password')
@click.option('--superuser', is_flag=True, default=False)
def create_user(full_name, email, password, superuser):
    user = schemas.UserCreate(
       full_name=full_name,
       email=email,
       password=password,
       is_superuser=superuser
    )
    session = orm.SessionLocal()
    try:
        orm.users.create(session, obj_in=user)
    except:
        session.rollback()
        raise


@click.command()
@click.argument('email')
@click.argument('password')
def update_user(email, password):
    session = orm.SessionLocal()
    user = orm.users.get_by_email(session, email=email)
    user_data = jsonable_encoder(user)
    user_in = schemas.UserUpdate(**user_data)
    user_in.password = password
    user = orm.users.update(session, db_obj=user, obj_in=user_in)


users.add_command(create_user, 'create')
users.add_command(update_user, 'update')

# main cli group

@click.group()
def cli():
    pass

cli.add_command(users)


if __name__ == '__main__':
    cli()



