import click
from . import orm, schemas


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

users.add_command(create_user, 'create')

# main cli group

@click.group()
def cli():
    pass

cli.add_command(users)


if __name__ == '__main__':
    cli()



