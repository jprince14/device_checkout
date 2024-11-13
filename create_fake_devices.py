import random
import sys
from faker import Faker
from deviceCheckout import db, Device


def create_fake_devices(n):
    """Generate fake users."""
    faker = Faker()
    for i in range(n):
        device = Device(devName=faker.text(20),
                    devIp=faker.text(20),
                    oemVer=faker.text(20),
                    ver=faker.text(20),
                    location=faker.text(20),
                    user=faker.text(20),
                    note=faker.text(20),)
        db.session.add(device)
    db.session.commit()
    print(f'Added {n} fake devices to the database.')
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Pass the number of devices you want to create as an argument.')
        sys.exit(1)
    create_fake_devices(int(sys.argv[1]))
