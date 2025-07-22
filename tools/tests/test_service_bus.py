import time
import threading
import asyncio
import pytest

from tools.ThreadedServiceBus import ThreadedServiceBus
from tools.AsyncServiceBus import AsyncServiceBus

def test_threaded_service_bus_basic():
    bus = ThreadedServiceBus()
    received = []

    def callback(msg_id, data):
        received.append((msg_id, data))

    bus.subscribe("group1", "serviceA", callback)
    msg_id = bus.publish("group1", "hello")
    time.sleep(0.1)
    assert received and received[0][1] == "hello"
    assert bus.pending_count() == 0

def test_threaded_service_bus_unsubscribe():
    bus = ThreadedServiceBus()
    received = []

    def callback(msg_id, data):
        received.append(data)

    bus.subscribe("group1", "serviceA", callback)
    bus.unsubscribe("group1", "serviceA")
    bus.publish("group1", "should not be received")
    time.sleep(0.1)
    assert not received

def test_threaded_service_bus_broadcast():
    bus = ThreadedServiceBus()
    received = []

    def cb1(msg_id, data):
        received.append(("cb1", data))

    def cb2(msg_id, data):
        received.append(("cb2", data))

    bus.subscribe("group1", "serviceA", cb1)
    bus.subscribe("group2", "serviceB", cb2)
    bus.publish("group1", "broadcasted", broadcast=True)
    time.sleep(0.1)
    assert ("cb1", "broadcasted") in received
    assert ("cb2", "broadcasted") in received

def test_threaded_service_bus_ttl_expiry():
    bus = ThreadedServiceBus()
    received = []

    def callback(msg_id, data):
        received.append(data)

    bus.subscribe("group1", "serviceA", callback)
    bus.publish("group1", "short-lived", ttl=0.01)
    time.sleep(0.05)
    assert bus.get_metrics()["expired"] >= 1

def test_threaded_service_bus_get_unread_services():
    bus = ThreadedServiceBus()
    received = []

    def callback(msg_id, data):
        received.append(data)

    bus.subscribe("group1", "serviceA", callback)
    msg_id = bus.publish("group1", "msg")
    time.sleep(0.1)
    assert bus.get_unread_services(msg_id) == set()

@pytest.mark.asyncio
async def test_async_service_bus_basic():
    bus = AsyncServiceBus()
    received = []

    async def callback(msg_id, data):
        received.append((msg_id, data))

    await bus.subscribe("group1", "serviceA", callback)
    msg_id = await bus.publish("group1", "hello")
    await asyncio.sleep(0.1)
    assert received and received[0][1] == "hello"
    assert await bus.pending_count() == 0

@pytest.mark.asyncio
async def test_async_service_bus_unsubscribe():
    bus = AsyncServiceBus()
    received = []

    async def callback(msg_id, data):
        received.append(data)

    await bus.subscribe("group1", "serviceA", callback)
    await bus.unsubscribe("group1", "serviceA")
    await bus.publish("group1", "should not be received")
    await asyncio.sleep(0.1)
    assert not received

@pytest.mark.asyncio
async def test_async_service_bus_broadcast():
    bus = AsyncServiceBus()
    received = []

    async def cb1(msg_id, data):
        received.append(("cb1", data))

    async def cb2(msg_id, data):
        received.append(("cb2", data))

    await bus.subscribe("group1", "serviceA", cb1)
    await bus.subscribe("group2", "serviceB", cb2)
    await bus.publish("group1", "broadcasted", broadcast=True)
    await asyncio.sleep(0.1)
    assert ("cb1", "broadcasted") in received
    assert ("cb2", "broadcasted") in received

@pytest.mark.asyncio
async def test_async_service_bus_ttl_expiry():
    bus = AsyncServiceBus()
    received = []

    async def callback(msg_id, data):
        received.append(data)

    await bus.subscribe("group1", "serviceA", callback)
    await bus.publish("group1", "short-lived", ttl=0.01)
    await asyncio.sleep(0.05)
    assert bus.get_metrics()["expired"] >= 1

@pytest.mark.asyncio
async def test_async_service_bus_get_unread_services():
    bus = AsyncServiceBus()
    received = []

    async def callback(msg_id, data):
        received.append(data)

    await bus.subscribe("group1", "serviceA", callback)
    msg_id = await bus.publish("group1", "msg")
    await asyncio.sleep(0.1)
    assert await bus.get_unread_services(msg_id) == set()
