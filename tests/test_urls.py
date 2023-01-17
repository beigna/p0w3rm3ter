import pytest
from rest_framework.test import APIClient
from datetime import datetime
from core.models import Device, Metering

BASE_URL = '/api/v1'


@pytest.fixture
def cli():
    return APIClient()


@pytest.mark.django_db
def test_create_device(cli):
    res = cli.post(
        f'{BASE_URL}/devices/',
        {
            'key': 'asd123',
            'name': 'Medidor Galpón'
        },
        format='json'
    )

    assert res.status_code == 201


@pytest.mark.django_db
def test_avoid_duplicated_devices(cli):
    Device(key='asd123', name='No importa').save()

    res = cli.post(
        f'{BASE_URL}/devices/',
        {
            'key': 'asd123',
            'name': 'Medidor Galpón'
        },
        format='json'
    )

    assert res.status_code == 400


@pytest.mark.django_db
def test_create_metering(cli):
    device = Device(key='asd123', name='No importa')
    device.save()

    res = cli.post(
        f'{BASE_URL}/meterings/',
        {
            'device': device.id,
            'consumption': 50,
            'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00')
        },
        format='json'
    )

    assert res.status_code == 201


@pytest.mark.django_db
def test_avoid_negative_consumption(cli):
    device = Device(key='asd123', name='No importa')
    device.save()

    res = cli.post(
        f'{BASE_URL}/meterings/',
        {
            'device': device.id,
            'consumption': -50,
            'timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00')
        },
        format='json'
    )

    assert res.status_code == 204
    assert Metering.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize('endpoint,data,result', [
    ('max_consumption', [1, 2, 3, 4], 4),
    ('min_consumption', [1, 2, 3, 4], 1),
    ('total_consumption', [1, 2, 3, 4], 10),
    ('avg_consumption', [1, 2, 3, 4], 2.5)
])
def test_device_meterings(cli, endpoint, data, result):
    device = Device(key='asd123', name='No importa')
    device.save()

    for e in data:
        Metering(
            device=device,
            consumption=e,
            timestamp=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00')
        ).save()

    res = cli.get(
        f'{BASE_URL}/devices/{device.id}/{endpoint}/',
        format='json'
    )

    if endpoint == 'total_consumption':
        assert res.data.get('consumption__sum') == result

    elif endpoint == 'avg_consumption':
        assert res.data.get('consumption__avg') == result

    else:
        assert res.data.get('consumption') == result
