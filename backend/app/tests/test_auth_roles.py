import pytest

pytestmark = pytest.mark.asyncio


async def test_register_manager_role(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "manager@example.com",
            "password": "ManagerPass123!",
            "full_name": "Manager One",
            "role": "manager",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["role"] == "manager"


async def test_register_defaults_to_employee_role(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "employee@example.com",
            "password": "EmployeePass123!",
            "full_name": "Employee One",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["role"] == "employee"
